"""
Web search integration for code research
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from duckduckgo_search import DDGS

from database.models import SearchQuery


class WebSearcher:
    """Handles web searches for code examples and documentation"""
    
    def __init__(self):
        self.ddg = DDGS()
    
    async def search(
        self,
        query: str,
        db: Optional[AsyncSession] = None,
        search_type: str = "web",
        max_results: int = 5
    ) -> List[Dict]:
        """
        Search the web for information
        
        Args:
            query: Search query
            db: Database session (optional)
            search_type: Type of search (web, documentation, code_example)
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        logger.info(f"Searching for: {query}")
        
        try:
            # Run synchronous search in thread pool
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                self._do_search,
                query,
                max_results
            )
            
            # Store search query in database
            if db:
                search_query = SearchQuery(
                    query=query,
                    search_type=search_type,
                    results=results,
                    created_at=datetime.utcnow()
                )
                db.add(search_query)
                await db.commit()
            
            logger.info(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def _do_search(self, query: str, max_results: int) -> List[Dict]:
        """Perform the actual search (synchronous)"""
        try:
            results = list(self.ddg.text(query, max_results=max_results))
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return []
    
    async def search_code_examples(
        self,
        language: str,
        topic: str,
        db: Optional[AsyncSession] = None
    ) -> List[Dict]:
        """Search for code examples"""
        query = f"{language} {topic} code example"
        return await self.search(query, db, "code_example")
    
    async def search_documentation(
        self,
        technology: str,
        topic: str,
        db: Optional[AsyncSession] = None
    ) -> List[Dict]:
        """Search for documentation"""
        query = f"{technology} {topic} documentation"
        return await self.search(query, db, "documentation")
    
    async def search_error_solution(
        self,
        error_message: str,
        language: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> List[Dict]:
        """Search for error solutions"""
        query = f"{language + ' ' if language else ''}{error_message} solution"
        return await self.search(query, db, "web")
    
    async def search_best_practices(
        self,
        language: str,
        topic: str,
        db: Optional[AsyncSession] = None
    ) -> List[Dict]:
        """Search for best practices"""
        query = f"{language} {topic} best practices"
        return await self.search(query, db, "web")
    
    async def get_search_history(
        self,
        db: AsyncSession,
        search_type: Optional[str] = None,
        limit: int = 10
    ) -> List[SearchQuery]:
        """Get search history"""
        from sqlalchemy import select
        
        stmt = select(SearchQuery).order_by(SearchQuery.created_at.desc())
        
        if search_type:
            stmt = stmt.where(SearchQuery.search_type == search_type)
        
        stmt = stmt.limit(limit)
        
        result = await db.execute(stmt)
        return list(result.scalars().all())






