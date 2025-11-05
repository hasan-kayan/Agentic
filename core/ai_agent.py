"""
AI Agent for autonomous system control
"""
from typing import List, Dict, Optional, Any
from loguru import logger
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings


class AIAgent:
    """AI Agent powered by OpenAI GPT"""
    
    def __init__(self, session_id: str):
        """
        Initialize AI Agent
        
        Args:
            session_id: Unique session identifier
        """
        self.session_id = session_id
        self.conversation_history: List[Dict[str, str]] = []
        self.client = None
        
    async def _ensure_client(self):
        """Ensure OpenAI client is initialized"""
        if self.client is None:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def chat(
        self,
        message: str,
        db: Optional[AsyncSession] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Chat with the AI agent
        
        Args:
            message: User message
            db: Database session
            context: Additional context
            
        Returns:
            AI response
        """
        await self._ensure_client()
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            raise
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.debug(f"Cleared conversation history for session {self.session_id}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    async def close(self):
        """Close the AI agent and cleanup resources"""
        if self.client:
            await self.client.close()
            self.client = None

