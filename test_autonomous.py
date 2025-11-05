"""
Quick test of the autonomous agent
"""
import asyncio
from rich.console import Console
from database import init_db, get_db, get_personalization_db
from core.autonomous_agent import AutonomousAgent

console = Console()

async def test_simple_task():
    """Test with a simple task"""
    console.print("[cyan]🧪 Testing Autonomous Agent[/cyan]\n")
    
    await init_db()
    
    agent = AutonomousAgent("test_session")
    
    # Simple task
    task = "Create a Python file called 'hello.py' that prints 'Hello from Autonomous AI!' and then run it to verify it works."
    
    console.print(f"[yellow]Task:[/yellow] {task}\n")
    console.print("[cyan]Executing autonomously...[/cyan]\n")
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            result = await agent.execute_autonomous_task(
                task=task,
                db=db,
                personalization_db=p_db
            )
    
    console.print("\n" + "="*60)
    console.print(f"[bold]Result:[/bold]")
    console.print(f"  Success: {result['success']}")
    console.print(f"  Iterations: {result['iterations']}")
    console.print(f"  Summary: {result.get('summary', 'N/A')}")
    
    if result['success']:
        console.print("\n[green]✅ Test PASSED![/green]")
    else:
        console.print("\n[red]❌ Test FAILED[/red]")

if __name__ == "__main__":
    asyncio.run(test_simple_task())

