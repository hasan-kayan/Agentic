"""
Tests for Terminal Executor
"""
import pytest
from core.terminal_executor import TerminalExecutor


@pytest.mark.asyncio
async def test_terminal_executor_initialization():
    """Test terminal executor initialization"""
    terminal = TerminalExecutor()
    
    assert terminal.os_type in ["darwin", "linux", "windows"]
    assert terminal.shell is not None


@pytest.mark.asyncio
async def test_check_command_exists():
    """Test checking if a command exists"""
    terminal = TerminalExecutor()
    
    # Test with a command that should exist
    exists = await terminal.check_command_exists("echo")
    assert exists is True
    
    # Test with a command that shouldn't exist
    exists = await terminal.check_command_exists("nonexistent_command_12345")
    assert exists is False






