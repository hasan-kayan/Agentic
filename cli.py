"""
Command-line interface for AI Agent
"""
import asyncio
import uuid
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from loguru import logger

from config import settings
from database import init_db, get_db, get_personalization_db
from core.ai_agent import AIAgent
from core.terminal_executor import TerminalExecutor
from core.project_generator import ProjectGenerator
from core.credential_manager import CredentialManager
from core.autonomous_manager import AutonomousManager
from core.test_generator import TestGenerator
from core.documentation_generator import DocumentationGenerator
from core.tool_installer import ToolInstaller

app = typer.Typer(help="AI Agent - Autonomous system control and project generation")
console = Console()


@app.command()
def chat(
    message: Optional[str] = typer.Argument(None, help="Message to send to AI"),
    session_id: Optional[str] = typer.Option(None, help="Session ID for conversation"),
    stream: bool = typer.Option(False, help="Stream the response")
):
    """Chat with the AI agent"""
    if not session_id:
        session_id = str(uuid.uuid4())
    
    asyncio.run(_chat(message, session_id, stream))


async def _chat(message: Optional[str], session_id: str, stream: bool):
    """Async chat implementation"""
    await init_db()
    
    agent = AIAgent(session_id)
    
    if not message:
        # Interactive mode
        console.print("[bold green]AI Agent Interactive Mode[/bold green]")
        console.print("Type 'exit' to quit\n")
        
        async for db in get_db():
            while True:
                user_input = console.input("[bold blue]You:[/bold blue] ")
                
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if stream:
                    console.print("[bold green]AI:[/bold green] ", end="")
                    async for chunk in agent.chat(user_input, db, stream=True):
                        console.print(chunk, end="")
                    console.print()
                else:
                    with console.status("[bold green]Thinking..."):
                        response = await agent.chat(user_input, db, stream=False)
                    console.print(f"[bold green]AI:[/bold green] {response}\n")
    else:
        # Single message mode
        async for db in get_db():
            with console.status("[bold green]Thinking..."):
                response = await agent.chat(message, db, stream=False)
            console.print("[bold green]Response:[/bold green]")
            console.print(Markdown(response))


@app.command()
def create_project(
    name: str = typer.Argument(..., help="Project name"),
    project_type: str = typer.Option(..., help="Project type (backend, frontend, fullstack, cli)"),
    language: str = typer.Option(..., help="Programming language"),
    framework: Optional[str] = typer.Option(None, help="Framework to use"),
    description: Optional[str] = typer.Option(None, help="Project description"),
    output_dir: Optional[str] = typer.Option(None, help="Output directory")
):
    """Create a new project"""
    asyncio.run(_create_project(name, project_type, language, framework, description, output_dir))


async def _create_project(name, project_type, language, framework, description, output_dir):
    """Async project creation"""
    await init_db()
    
    console.print(f"[bold green]Creating {project_type} project: {name}[/bold green]")
    
    agent = AIAgent(session_id="cli_project")
    terminal = TerminalExecutor()
    generator = ProjectGenerator(agent, terminal)
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            with console.status("[bold green]Generating project..."):
                project = await generator.create_project(
                    db=db,
                    personalization_db=p_db,
                    name=name,
                    project_type=project_type,
                    language=language,
                    framework=framework,
                    description=description,
                    output_dir=output_dir
                )
            
            console.print(f"[bold green]✓[/bold green] Project created at: {project.path}")


@app.command()
def execute(
    command: str = typer.Argument(..., help="Command to execute"),
    sudo: bool = typer.Option(False, help="Execute with sudo"),
    cwd: Optional[str] = typer.Option(None, help="Working directory")
):
    """Execute a terminal command"""
    asyncio.run(_execute(command, sudo, cwd))


async def _execute(command, sudo, cwd):
    """Async command execution"""
    await init_db()
    
    console.print(f"[bold yellow]Executing:[/bold yellow] {command}")
    
    terminal = TerminalExecutor()
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            with console.status("[bold green]Running..."):
                success, stdout, stderr = await terminal.execute(
                    command=command,
                    db=db,
                    personalization_db=p_db,
                    use_sudo=sudo,
                    cwd=cwd
                )
            
            if success:
                console.print("[bold green]✓ Success[/bold green]")
                if stdout:
                    console.print(stdout)
            else:
                console.print("[bold red]✗ Failed[/bold red]")
                if stderr:
                    console.print(f"[red]{stderr}[/red]")


@app.command()
def store_credential(
    credential_type: str = typer.Argument(..., help="Credential type"),
    identifier: str = typer.Argument(..., help="Identifier (username, service name, etc.)"),
    value: str = typer.Argument(..., help="Credential value"),
    description: Optional[str] = typer.Option(None, "--description", help="Description")
):
    """Store a credential securely"""
    asyncio.run(_store_credential(credential_type, identifier, value, description))


async def _store_credential(credential_type, identifier, value, description):
    """Async credential storage"""
    await init_db()
    
    async for p_db in get_personalization_db():
        await CredentialManager.store_credential(
            db=p_db,
            credential_type=credential_type,
            identifier=identifier,
            value=value,
            description=description
        )
    
    console.print("[bold green]✓[/bold green] Credential stored securely")


@app.command()
def autonomous(
    action: str = typer.Argument(..., help="Action: enable, disable, status")
):
    """Manage autonomous mode"""
    asyncio.run(_autonomous(action))


async def _autonomous(action):
    """Async autonomous management"""
    await init_db()
    
    manager = AutonomousManager()
    
    if action == "enable":
        manager.enable_autonomous_mode()
        console.print("[bold green]✓[/bold green] Autonomous mode enabled")
    elif action == "disable":
        manager.disable_autonomous_mode()
        console.print("[bold yellow]✓[/bold yellow] Autonomous mode disabled")
    elif action == "status":
        status_table = Table(title="Autonomous Mode Status")
        status_table.add_column("Setting", style="cyan")
        status_table.add_column("Value", style="green")
        
        status_table.add_row("Enabled", str(manager.autonomous_mode))
        status_table.add_row("Actions", f"{manager.action_count}/{manager.max_actions}")
        status_table.add_row("Require Confirmation", str(manager.require_confirmation))
        
        console.print(status_table)


@app.command()
def generate_tests(
    file_path: str = typer.Argument(..., help="Path to code file"),
    language: str = typer.Option(..., help="Programming language"),
    output: Optional[str] = typer.Option(None, help="Output file")
):
    """Generate unit tests for code"""
    asyncio.run(_generate_tests(file_path, language, output))


async def _generate_tests(file_path, language, output):
    """Async test generation"""
    await init_db()
    
    # Read the code file
    with open(file_path, 'r') as f:
        code = f.read()
    
    agent = AIAgent(session_id="test_generation")
    test_gen = TestGenerator(agent)
    
    with console.status("[bold green]Generating tests..."):
        tests = await test_gen.generate_tests(
            code=code,
            language=language,
            output_file=output
        )
    
    if output:
        console.print(f"[bold green]✓[/bold green] Tests saved to: {output}")
    else:
        console.print("[bold green]Generated Tests:[/bold green]")
        console.print(tests)


@app.command()
def generate_docs(
    project_path: str = typer.Argument(..., help="Project path"),
    doc_type: str = typer.Option("readme", help="Documentation type")
):
    """Generate documentation"""
    asyncio.run(_generate_docs(project_path, doc_type))


async def _generate_docs(project_path, doc_type):
    """Async documentation generation"""
    await init_db()
    
    agent = AIAgent(session_id="documentation")
    doc_gen = DocumentationGenerator(agent)
    
    async for db in get_db():
        with console.status(f"[bold green]Generating {doc_type}..."):
            if doc_type == "readme":
                project_info = {"name": project_path.split('/')[-1], "path": project_path}
                output_path = f"{project_path}/README.md"
                await doc_gen.generate_readme(
                    db=db,
                    project_path=project_path,
                    project_info=project_info,
                    output_path=output_path
                )
                console.print(f"[bold green]✓[/bold green] README generated at: {output_path}")


@app.command()
def install_tool(
    tool: str = typer.Argument(..., help="Tool name to install")
):
    """Install a development tool"""
    asyncio.run(_install_tool(tool))


async def _install_tool(tool):
    """Async tool installation"""
    await init_db()
    
    terminal = TerminalExecutor()
    installer = ToolInstaller(terminal)
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            with console.status(f"[bold green]Installing {tool}..."):
                success = await installer.ensure_tool_installed(
                    tool=tool,
                    db=db,
                    personalization_db=p_db
                )
            
            if success:
                console.print(f"[bold green]✓[/bold green] {tool} is ready")
            else:
                console.print(f"[bold red]✗[/bold red] Failed to install {tool}")


@app.command()
def init():
    """Initialize the AI Agent system"""
    asyncio.run(_init())


async def _init():
    """Initialize database and configuration"""
    console.print("[bold green]Initializing AI Agent...[/bold green]")
    
    await init_db()
    
    console.print("[bold green]✓[/bold green] Database initialized")
    console.print(f"[bold green]✓[/bold green] Configuration loaded from: {settings.base_dir}")
    console.print("\n[bold yellow]Next steps:[/bold yellow]")
    console.print("1. Store your sudo password: [cyan]ai-agent store-credential sudo_password <username> <password>[/cyan]")
    console.print("2. Store your OpenAI API key in .env file")
    console.print("3. Start chatting: [cyan]ai-agent chat[/cyan]")
    console.print("4. Or create a project: [cyan]ai-agent create-project <name> -t backend -l python[/cyan]")


if __name__ == "__main__":
    app()


