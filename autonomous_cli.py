"""
Autonomous AI Agent CLI - Like Cursor but in the terminal!
Give it any task and it will autonomously execute it
"""
import asyncio
import uuid
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt

from database import init_db, get_db, get_personalization_db
from core.autonomous_agent import AutonomousAgent
from core.project_session import ProjectSession

console = Console()
project_session_manager = ProjectSession()

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🤖 AUTONOMOUS AI CODING AGENT 🤖                            ║
║                                                               ║
║   Like Cursor AI, but in your terminal!                       ║
║   Give it any task - it will plan, code, test, and deploy    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

EXAMPLES = """
💡 Example Tasks:

SIMPLE:
  • "Create a hello world Python script"
  • "Write a function to sort a list"
  • "Make a quick test for my code.py file"

END-TO-END PROJECTS:
  • "Create a REST API for a todo app with FastAPI, SQLite, full CRUD, tests, and documentation"
  • "Build a web scraper that gets product prices from Amazon"
  • "Create a Discord bot that responds to commands"
  • "Make a Flask blog with user authentication and posts"

COMPLEX WORKFLOWS:
  • "Create a microservices architecture with user service, order service, and API gateway"
  • "Build a data pipeline that processes CSV files and generates reports"
  • "Create a full-stack app with React frontend and Python backend"
"""

async def run_autonomous_task():
    """Run the autonomous agent"""
    console.print(BANNER, style="cyan bold")
    console.print(EXAMPLES, style="yellow")
    
    # Initialize database
    console.print("\n[dim]Initializing...[/dim]")
    await init_db()
    
    console.print("[green]✓[/green] Ready!\n")
    
    # Show recent projects
    recent_sessions = project_session_manager.list_sessions()
    if recent_sessions:
        console.print("[bold]📂 Recent Projects:[/bold]")
        for i, session in enumerate(recent_sessions[:5], 1):
            status_color = "green" if session["status"] == "complete" else "yellow"
            console.print(f"  {i}. [{status_color}]{session['project_name']}[/{status_color}] - {session['prompts_count']} prompts, {session['files_count']} files")
        console.print()
    
    while True:
        # Get task from user
        console.print("[bold cyan]═" * 60 + "[/bold cyan]")
        
        # Ask if continuing or new project
        continue_project = False
        continue_session_id = None
        
        if recent_sessions:
            action = Prompt.ask(
                "\n[dim]New project or continue existing?[/dim]",
                choices=["new", "continue"],
                default="new"
            )
            
            if action == "continue":
                console.print("\n[bold]Select a project to continue:[/bold]")
                for i, session in enumerate(recent_sessions[:10], 1):
                    console.print(f"  {i}. {session['project_name']} ({session['project_path']})")
                
                project_num = Prompt.ask("Project number", default="1")
                try:
                    selected = recent_sessions[int(project_num) - 1]
                    continue_session_id = selected["session_id"]
                    continue_project = True
                    console.print(f"\n[green]✓[/green] Continuing: {selected['project_name']}\n")
                except:
                    console.print("[red]Invalid selection, starting new project[/red]")
        
        task = Prompt.ask(
            "\n[bold green]What do you want me to build/fix/improve?[/bold green]",
            default=""
        )
        
        if not task or task.lower() in ['exit', 'quit', 'q']:
            console.print("\n[yellow]👋 Goodbye![/yellow]")
            break
        
        # Create agent
        session_id = str(uuid.uuid4())
        agent = AutonomousAgent(session_id, project_session_id=continue_session_id)
        
        console.print(f"\n[cyan]🤖 Starting autonomous execution...[/cyan]\n")
        
        # Run task
        try:
            async for db in get_db():
                async for p_db in get_personalization_db():
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        console=console,
                    ) as progress:
                        task_progress = progress.add_task(
                            "[cyan]AI is working autonomously...",
                            total=None
                        )
                        
                        result = await agent.execute_autonomous_task(
                            task=task,
                            db=db,
                            personalization_db=p_db,
                            continue_session=continue_project
                        )
                        
                        progress.update(task_progress, completed=True)
            
            # Display results
            console.print("\n" + "=" * 60 + "\n")
            
            if result["success"]:
                project_path_line = f"[bold]Project Path:[/bold] {result['project_path']}\n" if result.get('project_path') else ""
                session_line = f"[bold]Session ID:[/bold] {result.get('session_id')}\n" if result.get('session_id') else ""
                stats_line = f"[bold]Created:[/bold] {result.get('files_created', 0)} files, Ran: {result.get('commands_executed', 0)} commands\n"
                console.print(Panel(
                    f"[green]✅ TASK COMPLETED SUCCESSFULLY![/green]\n\n"
                    f"[bold]Summary:[/bold]\n{result['summary']}\n\n"
                    f"[bold]Iterations:[/bold] {result['iterations']}\n"
                    f"{project_path_line}"
                    f"{stats_line}"
                    f"{session_line}"
                    f"\n[dim]You can continue working on this project in the next prompt![/dim]",
                    title="🎉 Success",
                    border_style="green"
                ))
            else:
                max_iter_msg = '[red]Max iterations reached - task may be too complex[/red]\n' if result.get('max_iterations_reached') else ''
                error_msg = f"[bold]Error:[/bold] {result.get('error')}\n" if result.get('error') else ''
                console.print(Panel(
                    f"[yellow]⚠️ Task did not complete[/yellow]\n\n"
                    f"[bold]Iterations:[/bold] {result['iterations']}\n"
                    f"{max_iter_msg}"
                    f"{error_msg}",
                    title="Status",
                    border_style="yellow"
                ))
            
            # Show conversation history
            if Prompt.ask("\n[dim]Show execution log?[/dim]", choices=["y", "n"], default="n") == "y":
                console.print("\n[bold]Execution Log:[/bold]\n")
                for msg in agent.conversation_history:
                    if msg["role"] == "assistant" and msg.get("content"):
                        console.print(f"[cyan]AI:[/cyan] {msg['content']}\n")
                    elif msg["role"] == "tool":
                        console.print(f"[yellow]Tool Result:[/yellow] {msg['content'][:200]}...\n")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Task interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        
        # Continue?
        console.print()
        if Prompt.ask("[dim]Another task?[/dim]", choices=["y", "n"], default="y") == "n":
            console.print("\n[yellow]👋 Goodbye![/yellow]")
            break

if __name__ == "__main__":
    try:
        asyncio.run(run_autonomous_task())
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)

