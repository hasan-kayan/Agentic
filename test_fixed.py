"""
Test the fixed autonomous agent
"""
import asyncio
from rich.console import Console
from database import init_db, get_db, get_personalization_db
from core.autonomous_agent import AutonomousAgent

console = Console()

async def test():
    console.print("[cyan]Testing Fixed Autonomous Agent...[/cyan]\n")
    
    await init_db()
    
    agent = AutonomousAgent("test", max_iterations=10)
    
    task = "Create a file called test_output.txt with the content 'Autonomous AI is working!' and verify it by reading it back"
    
    console.print(f"[yellow]Task:[/yellow] {task}\n")
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            result = await agent.execute_autonomous_task(
                task=task,
                db=db,
                personalization_db=p_db
            )
    
    console.print(f"\n[bold]Success:[/bold] {result['success']}")
    console.print(f"[bold]Iterations:[/bold] {result['iterations']}")
    
    if result['success']:
        console.print("[green]✅ FIXED! Agent is working![/green]")
    else:
        console.print(f"[red]Issue: {result.get('summary')}[/red]")

if __name__ == "__main__":
    asyncio.run(test())





