"""
Tests for AI Agent
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from core.ai_agent import AIAgent


@pytest.mark.asyncio
async def test_ai_agent_initialization():
    """Test AI agent initialization"""
    agent = AIAgent(session_id="test_session")
    
    assert agent.session_id == "test_session"
    assert agent.conversation_history == []


@pytest.mark.asyncio
async def test_clear_history():
    """Test clearing conversation history"""
    agent = AIAgent(session_id="test_session")
    agent.conversation_history = [{"role": "user", "content": "test"}]
    
    agent.clear_history()
    
    assert agent.conversation_history == []






