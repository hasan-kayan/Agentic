"""
Autonomous AI Agent with full system access and tool use
This agent can execute commands, create files, test code, and fix errors autonomously
"""
import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from loguru import logger
from openai import AsyncOpenAI
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import settings
from core.terminal_executor import TerminalExecutor
from core.browser_tester import BrowserTester
from core.project_session import ProjectSession

console = Console()


class AutonomousAgent:
    """Autonomous AI agent with full tool access"""
    
    def __init__(self, session_id: str, max_iterations: int = 100, project_session_id: Optional[str] = None):
        """Initialize autonomous agent"""
        self.session_id = session_id
        self.client = None
        self.terminal = TerminalExecutor()
        self.browser_tester = BrowserTester()
        self.project_session = ProjectSession()
        self.project_session_id = project_session_id
        self.conversation_history = []
        self.max_iterations = max_iterations
        self.files_created = []
        self.commands_executed = []
        
    async def _ensure_client(self):
        """Ensure OpenAI client is initialized"""
        if self.client is None:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    def _get_tools_definition(self) -> List[Dict]:
        """Define available tools for the AI"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "execute_command",
                    "description": "Execute a terminal command. Use this to run shell commands, install packages, run tests, etc. Can use sudo if needed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "The command to execute"
                            },
                            "use_sudo": {
                                "type": "boolean",
                                "description": "Whether to use sudo privileges",
                                "default": False
                            },
                            "cwd": {
                                "type": "string",
                                "description": "Working directory for the command"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Create or overwrite a file with content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to create"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to read"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_directory",
                    "description": "Create a directory (including parent directories)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory_path": {
                                "type": "string",
                                "description": "Path to the directory to create"
                            }
                        },
                        "required": ["directory_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List files and directories in a path",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory_path": {
                                "type": "string",
                                "description": "Path to list contents of"
                            }
                        },
                        "required": ["directory_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_browser_console",
                    "description": "Test a web application by opening it in a browser and checking for console errors. Use this for React, Vue, or any web app to verify it works without errors.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to test (e.g., http://localhost:3000)"
                            },
                            "wait_time": {
                                "type": "integer",
                                "description": "Seconds to wait for page to load",
                                "default": 5
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "task_complete",
                    "description": "Call this when the task is fully complete and tested",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "Summary of what was accomplished"
                            },
                            "project_path": {
                                "type": "string",
                                "description": "Path to the created project (if applicable)"
                            }
                        },
                        "required": ["summary"]
                    }
                }
            }
        ]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for autonomous operation"""
        return """You are an autonomous AI agent. You MUST use function calls to perform ALL actions.

🚨 CRITICAL: You are FORCED to use functions. You CANNOT write explanations or markdown.

🔧 AVAILABLE FUNCTIONS:
- create_directory(directory_path)
- create_file(file_path, content)
- execute_command(command, cwd)
- check_browser_console(url)
- task_complete(summary, project_path)

❌ WRONG - DO NOT DO THIS:
```python
execute_command(command="pip install paramiko")
```
Explanation: "First, I'll install..."

✅ CORRECT - YOU MUST DO THIS:
Just call the function. No text. No markdown. No explanations.

🎯 WORKFLOW EXAMPLE (SSH Script Task):
1. create_directory("generated_projects/ssh-script")
2. create_file("generated_projects/ssh-script/ssh_connect.py", "import paramiko...")
3. create_file("generated_projects/ssh-script/requirements.txt", "paramiko")
4. execute_command("pip install -r requirements.txt", "generated_projects/ssh-script")
5. task_complete("SSH script created", "generated_projects/ssh-script")

💎 QUALITY: Create 10-15 files minimum with complete, professional implementations.

Remember: You can ONLY communicate through function calls. Start working immediately."""

    async def execute_command(self, command: str, use_sudo: bool = False, cwd: Optional[str] = None, db=None, personalization_db=None) -> str:
        """Execute a terminal command"""
        logger.info(f"Executing: {command} (sudo={use_sudo}, cwd={cwd})")
        try:
            # Increase timeout for long-running commands like npm installs
            timeout = 600 if 'npm' in command or 'npx' in command or 'install' in command else 60
            
            exit_code, stdout, stderr = await self.terminal.execute(
                command=command,
                use_sudo=use_sudo,
                cwd=cwd,
                timeout=timeout
            )
            
            result = f"Exit code: {exit_code}\n"
            if stdout:
                result += f"STDOUT:\n{stdout}\n"
            if stderr:
                result += f"STDERR:\n{stderr}\n"
            
            return result
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    async def create_file(self, file_path: str, content: str) -> str:
        """Create or overwrite a file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            logger.info(f"Created file: {file_path}")
            return f"Successfully created file: {file_path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    async def read_file(self, file_path: str) -> str:
        """Read a file"""
        try:
            path = Path(file_path)
            content = path.read_text()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def create_directory(self, directory_path: str) -> str:
        """Create a directory"""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory_path}")
            return f"Successfully created directory: {directory_path}"
        except Exception as e:
            return f"Error creating directory: {str(e)}"
    
    async def list_directory(self, directory_path: str) -> str:
        """List directory contents"""
        try:
            path = Path(directory_path)
            items = list(path.iterdir())
            result = f"Contents of {directory_path}:\n"
            for item in items:
                item_type = "DIR" if item.is_dir() else "FILE"
                result += f"  [{item_type}] {item.name}\n"
            return result
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    async def check_browser_console(self, url: str, wait_time: int = 5) -> str:
        """Check browser console for errors"""
        logger.info(f"Checking browser console at: {url}")
        try:
            result = await self.browser_tester.check_webapp_console(url, wait_time)
            
            if not result["success"]:
                return f"Failed to test: {result.get('error', 'Unknown error')}"
            
            response = f"Browser Test Results for {url}:\n"
            response += f"Title: {result.get('title', 'N/A')}\n"
            response += f"Screenshot: {result.get('screenshot', 'N/A')}\n\n"
            
            if result["has_errors"]:
                response += "❌ ERRORS FOUND:\n"
                for error in result["console_errors"]:
                    response += f"  - {error['message']}\n"
                
                if result["console_warnings"]:
                    response += "\n⚠️ WARNINGS:\n"
                    for warning in result["console_warnings"]:
                        response += f"  - {warning['message']}\n"
                
                if result["network_errors"]:
                    response += "\n🌐 NETWORK ERRORS:\n"
                    for net_err in result["network_errors"]:
                        response += f"  - {net_err['url']}: {net_err['error']}\n"
                
                response += "\nFIX THESE ERRORS and test again!"
            else:
                response += "✅ NO ERRORS! The web app is working perfectly!\n"
                if result["console_warnings"]:
                    response += f"\n⚠️ {len(result['console_warnings'])} warnings (non-critical)\n"
            
            return response
        except Exception as e:
            return f"Error checking browser: {str(e)}"
    
    async def _execute_tool(self, tool_name: str, tool_args: Dict, db=None, personalization_db=None) -> str:
        """Execute a tool call"""
        logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
        
        # Print what we're doing to console
        if tool_name == "create_file":
            console.print(f"[cyan]📝 Creating file:[/cyan] {tool_args.get('file_path')}")
            self.files_created.append(tool_args.get("file_path"))
        elif tool_name == "execute_command":
            console.print(f"[yellow]⚡ Running command:[/yellow] {tool_args.get('command')}")
            self.commands_executed.append(tool_args.get("command"))
        elif tool_name == "create_directory":
            console.print(f"[blue]📁 Creating directory:[/blue] {tool_args.get('directory_path')}")
        elif tool_name == "check_browser_console":
            console.print(f"[magenta]🌐 Testing in browser:[/magenta] {tool_args.get('url')}")
        elif tool_name == "read_file":
            console.print(f"[green]📖 Reading file:[/green] {tool_args.get('file_path')}")
        
        if tool_name == "execute_command":
            return await self.execute_command(
                command=tool_args.get("command"),
                use_sudo=tool_args.get("use_sudo", False),
                cwd=tool_args.get("cwd"),
                db=db,
                personalization_db=personalization_db
            )
        elif tool_name == "create_file":
            return await self.create_file(
                file_path=tool_args.get("file_path"),
                content=tool_args.get("content")
            )
        elif tool_name == "read_file":
            return await self.read_file(file_path=tool_args.get("file_path"))
        elif tool_name == "create_directory":
            return await self.create_directory(directory_path=tool_args.get("directory_path"))
        elif tool_name == "list_directory":
            return await self.list_directory(directory_path=tool_args.get("directory_path"))
        elif tool_name == "check_browser_console":
            return await self.check_browser_console(
                url=tool_args.get("url"),
                wait_time=tool_args.get("wait_time", 5)
            )
        elif tool_name == "task_complete":
            return "TASK_COMPLETE:" + json.dumps(tool_args)
        else:
            return f"Unknown tool: {tool_name}"
    
    async def execute_autonomous_task(self, task: str, db=None, personalization_db=None, continue_session: bool = False) -> Dict[str, Any]:
        """
        Execute a task autonomously with tool use
        
        Args:
            task: The task to execute
            db: Database session
            personalization_db: Personalization database
            continue_session: Whether to continue an existing project session
            
        Returns:
            Dict with 'success', 'summary', 'project_path', 'iterations', 'session_id'
        """
        # Print header
        console.print(Panel.fit(
            f"[bold cyan]🤖 Autonomous Agent Starting[/bold cyan]\n\n"
            f"[bold]Task:[/bold] {task}\n"
            f"[bold]Session ID:[/bold] {self.session_id}\n"
            f"[bold]Max Iterations:[/bold] {self.max_iterations}",
            border_style="cyan"
        ))
        
        await self._ensure_client()
        
        # If continuing a session, load context
        session_context = ""
        if continue_session and self.project_session_id:
            session_context = self.project_session.get_session_context(self.project_session_id)
            logger.info(f"Continuing session: {self.project_session_id}")
            console.print(f"[yellow]🔄 Continuing existing session[/yellow]")
        
        # Initialize conversation with system prompt and user task
        system_content = self._get_system_prompt()
        if session_context:
            system_content += f"\n\n{session_context}"
        
        self.conversation_history = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": task}
        ]
        
        iteration = 0
        task_complete = False
        completion_info = {}
        
        while iteration < self.max_iterations and not task_complete:
            iteration += 1
            console.print(f"\n[bold magenta]━━━ Iteration {iteration}/{self.max_iterations} ━━━[/bold magenta]")
            logger.info(f"Iteration {iteration}/{self.max_iterations}")
            
            try:
                # Call OpenAI with tools
                console.print("[dim]🤔 AI is thinking...[/dim]")
                
                # FORCE tool usage - no more explanations!
                tool_choice = "required"  # Always require tools
                
                response = await self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=self.conversation_history,
                    tools=self._get_tools_definition(),
                    tool_choice=tool_choice,  # FORCE tools
                    temperature=0.1,  # Very low for precision
                    max_tokens=4000
                )
                
                assistant_message = response.choices[0].message
                
                # Print AI's reasoning if present
                if assistant_message.content:
                    console.print(f"[bold blue]💭 AI:[/bold blue] {assistant_message.content}")
                    logger.info(f"AI response: {assistant_message.content}")
                
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in (assistant_message.tool_calls or [])
                    ] if assistant_message.tool_calls else None
                })
                
                # Check if there are tool calls
                if assistant_message.tool_calls:
                    console.print(f"[bold green]🔧 Executing {len(assistant_message.tool_calls)} tool call(s)...[/bold green]")
                    
                    # Execute each tool call
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        
                        # Execute the tool
                        tool_result = await self._execute_tool(
                            tool_name, 
                            tool_args,
                            db=db,
                            personalization_db=personalization_db
                        )
                        
                        # Print result summary
                        if tool_result.startswith("TASK_COMPLETE:"):
                            task_complete = True
                            completion_info = json.loads(tool_result.replace("TASK_COMPLETE:", ""))
                            console.print("[bold green]✅ Task marked as complete![/bold green]")
                        elif tool_result.startswith("Error"):
                            console.print(f"[red]⚠️  {tool_result[:100]}...[/red]")
                        else:
                            # Show brief result
                            result_preview = tool_result[:150].replace('\n', ' ')
                            console.print(f"[dim]  ↳ {result_preview}...[/dim]")
                        
                        # Add tool result to conversation
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result
                        })
                else:
                    # No tool calls - check if it's asking questions (OK) or just explaining (BAD)
                    if iteration == 1 and assistant_message.content:
                        # First iteration, asking questions is OK
                        console.print("[cyan]💬 AI is asking clarifying questions...[/cyan]")
                        # Wait for user response - exit loop and return control
                        break
                    else:
                        # Not first iteration, or no content - agent should be using tools
                        console.print("[yellow]⚠️  No tool calls made. Redirecting agent to use tools...[/yellow]")
                        
                        # Add a strong reminder to use actual function calls
                        self.conversation_history.append({
                            "role": "user",
                            "content": "❌ STOP! You MUST call the actual functions NOW. DO NOT write markdown code blocks. "
                                       "Use create_directory, create_file, execute_command functions. "
                                       "Start with: create_directory, then create_file for EACH file with FULL content (15+ files). "
                                       "NO MORE TEXT. ONLY FUNCTION CALLS."
                        })
                        
                        # Try one more time
                        if iteration < self.max_iterations:
                            continue
                        else:
                            break
                    
            except Exception as e:
                logger.error(f"Error in iteration {iteration}: {str(e)}")
                console.print(f"[bold red]❌ Error in iteration {iteration}: {str(e)}[/bold red]")
                return {
                    "success": False,
                    "error": str(e),
                    "iterations": iteration,
                    "session_id": self.project_session_id
                }
        
        # Save or update session
        if task_complete and completion_info.get("project_path"):
            if not self.project_session_id:
                # Create new session
                project_name = Path(completion_info["project_path"]).name
                self.project_session_id = self.project_session.create_session(
                    project_name=project_name,
                    project_path=completion_info["project_path"],
                    initial_prompt=task
                )
            
            # Update session
            self.project_session.update_session(
                session_id=self.project_session_id,
                files_created=self.files_created,
                commands_executed=self.commands_executed,
                status="complete" if task_complete else "in_progress",
                iterations=iteration
            )
        
        # Print final summary
        result = {
            "success": task_complete,
            "summary": completion_info.get("summary", "Task completed"),
            "project_path": completion_info.get("project_path"),
            "iterations": iteration,
            "max_iterations_reached": iteration >= self.max_iterations,
            "session_id": self.project_session_id,
            "files_created": len(self.files_created),
            "commands_executed": len(self.commands_executed)
        }
        
        if task_complete:
            console.print(Panel.fit(
                f"[bold green]✅ TASK COMPLETED SUCCESSFULLY![/bold green]\n\n"
                f"[bold]Summary:[/bold] {result['summary']}\n"
                f"[bold]Project Path:[/bold] {result.get('project_path', 'N/A')}\n"
                f"[bold]Iterations:[/bold] {iteration}\n"
                f"[bold]Files Created:[/bold] {len(self.files_created)}\n"
                f"[bold]Commands Executed:[/bold] {len(self.commands_executed)}\n"
                f"[bold]Session ID:[/bold] {self.project_session_id}",
                border_style="green"
            ))
        else:
            console.print(Panel.fit(
                f"[bold yellow]⚠️  Task Incomplete[/bold yellow]\n\n"
                f"[bold]Iterations:[/bold] {iteration}/{self.max_iterations}\n"
                f"[bold]Files Created:[/bold] {len(self.files_created)}\n"
                f"[bold]Commands Executed:[/bold] {len(self.commands_executed)}\n"
                f"[bold]Reason:[/bold] {'Max iterations reached' if iteration >= self.max_iterations else 'Agent stopped early'}",
                border_style="yellow"
            ))
        
        return result

