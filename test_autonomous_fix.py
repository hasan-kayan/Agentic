"""
Quick test to verify autonomous agent fixes
"""
import asyncio
from core.autonomous_agent import AutonomousAgent
from database.database import init_db, get_db, get_personalization_db
from rich.console import Console

console = Console()


async def test_autonomous_fix():
    """Test that agent makes actual function calls"""
    
    console.print("\n[bold cyan]Testing Autonomous Agent Fix[/bold cyan]\n")
    
    # Initialize
    await init_db()
    
    # Create agent
    agent = AutonomousAgent(
        session_id="test_fix",
        max_iterations=10
    )
    
    # Simple task
    task = "Create a simple React app called 'test-counter' with a counter button"
    
    console.print(f"[bold]Task:[/bold] {task}\n")
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            try:
                result = await agent.execute_autonomous_task(
                    task=task,
                    db=db,
                    personalization_db=p_db
                )
                
                console.print("\n[bold green]Test Results:[/bold green]")
                console.print(f"Success: {result['success']}")
                console.print(f"Iterations: {result['iterations']}")
                console.print(f"Files Created: {result['files_created']}")
                console.print(f"Commands Executed: {result['commands_executed']}")
                
                if result['files_created'] > 0:
                    console.print("\n[bold green]✅ FIXED! Agent is making function calls![/bold green]")
                else:
                    console.print("\n[bold red]❌ Still broken - no files created[/bold red]")
                
                return result
                
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                import traceback
                traceback.print_exc()
                return None


if __name__ == "__main__":
    asyncio.run(test_autonomous_fix())

