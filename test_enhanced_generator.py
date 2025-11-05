"""
Test script for the enhanced project generator
"""
import asyncio
from pathlib import Path
from core.ai_agent import AIAgent
from core.project_generator import ProjectGenerator
from core.terminal_executor import TerminalExecutor
from database.database import init_db, get_db, get_personalization_db
from rich.console import Console

console = Console()


async def test_cli_project():
    """Test creating a CLI project"""
    console.print("\n[bold cyan]════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]Testing Enhanced Project Generator[/bold cyan]")
    console.print("[bold cyan]════════════════════════════════════════[/bold cyan]\n")
    
    # Initialize database
    await init_db()
    
    # Create instances
    ai_agent = AIAgent(session_id="test_session")
    terminal = TerminalExecutor()
    generator = ProjectGenerator(ai_agent, terminal)
    
    # Test directory
    test_dir = Path("/Users/hasankayan/Desktop/ai_creates_ai/generated_projects/test_cli_app")
    
    # Remove test directory if it exists
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
        console.print(f"[yellow]Cleaned up existing test directory[/yellow]")
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            try:
                # Create a CLI project
                console.print("\n[bold green]Creating CLI Project...[/bold green]\n")
                
                project = await generator.create_project(
                    db=db,
                    personalization_db=p_db,
                    name="test_cli_app",
                    project_type="cli",
                    language="python",
                    framework=None,
                    description="A test CLI application with rich output",
                    output_dir=str(test_dir)
                )
                
                console.print(f"\n[bold green]✅ Test Completed Successfully![/bold green]")
                console.print(f"Project ID: {project.id}")
                console.print(f"Project Path: {project.path}")
                
                # List created files
                console.print("\n[bold cyan]Created Files:[/bold cyan]")
                for file in sorted(test_dir.rglob("*")):
                    if file.is_file():
                        console.print(f"  • {file.relative_to(test_dir)}")
                
                return True
                
            except Exception as e:
                console.print(f"\n[bold red]❌ Test Failed: {str(e)}[/bold red]")
                import traceback
                traceback.print_exc()
                return False


async def test_backend_project():
    """Test creating a backend project"""
    console.print("\n[bold cyan]════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]Testing FastAPI Backend Generator[/bold cyan]")
    console.print("[bold cyan]════════════════════════════════════════[/bold cyan]\n")
    
    # Initialize database
    await init_db()
    
    # Create instances
    ai_agent = AIAgent(session_id="test_session_backend")
    terminal = TerminalExecutor()
    generator = ProjectGenerator(ai_agent, terminal)
    
    # Test directory
    test_dir = Path("/Users/hasankayan/Desktop/ai_creates_ai/generated_projects/test_fastapi_backend")
    
    # Remove test directory if it exists
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
        console.print(f"[yellow]Cleaned up existing test directory[/yellow]")
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            try:
                # Create a FastAPI backend project
                console.print("\n[bold green]Creating FastAPI Backend Project...[/bold green]\n")
                
                project = await generator.create_project(
                    db=db,
                    personalization_db=p_db,
                    name="test_fastapi_backend",
                    project_type="backend",
                    language="python",
                    framework="fastapi",
                    description="A test FastAPI backend with user management",
                    output_dir=str(test_dir)
                )
                
                console.print(f"\n[bold green]✅ Test Completed Successfully![/bold green]")
                console.print(f"Project ID: {project.id}")
                console.print(f"Project Path: {project.path}")
                
                # List created files
                console.print("\n[bold cyan]Created Files:[/bold cyan]")
                for file in sorted(test_dir.rglob("*.py")):
                    if file.is_file():
                        console.print(f"  • {file.relative_to(test_dir)}")
                
                return True
                
            except Exception as e:
                console.print(f"\n[bold red]❌ Test Failed: {str(e)}[/bold red]")
                import traceback
                traceback.print_exc()
                return False


async def main():
    """Run all tests"""
    console.print("\n[bold magenta]╔══════════════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║   Enhanced Project Generator Test Suite     ║[/bold magenta]")
    console.print("[bold magenta]╚══════════════════════════════════════════════╝[/bold magenta]\n")
    
    results = []
    
    # Test 1: CLI Project
    console.print("[bold]Test 1: CLI Project Generation[/bold]")
    result1 = await test_cli_project()
    results.append(("CLI Project", result1))
    
    await asyncio.sleep(2)
    
    # Test 2: Backend Project
    console.print("\n[bold]Test 2: FastAPI Backend Project Generation[/bold]")
    result2 = await test_backend_project()
    results.append(("Backend Project", result2))
    
    # Print summary
    console.print("\n[bold cyan]═══════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]Test Summary[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════[/bold cyan]\n")
    
    for test_name, passed in results:
        status = "[bold green]✅ PASS[/bold green]" if passed else "[bold red]❌ FAIL[/bold red]"
        console.print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    console.print(f"\n[bold]Total: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[bold green]🎉 All tests passed! The enhanced system is working perfectly![/bold green]")
    else:
        console.print("\n[bold red]Some tests failed. Please review the errors above.[/bold red]")


if __name__ == "__main__":
    asyncio.run(main())

