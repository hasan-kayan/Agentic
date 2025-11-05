"""
FastAPI application for AI Agent web API
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import uuid

from config import settings
from database import init_db, get_db, get_personalization_db
from api.routes import projects, tasks, terminal, credentials, autonomous, documentation
from api.middleware import setup_logging

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="Autonomous AI Agent for system control and project generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
setup_logging()

# Include routers
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(terminal.router, prefix="/api/terminal", tags=["terminal"])
app.include_router(credentials.router, prefix="/api/credentials", tags=["credentials"])
app.include_router(autonomous.router, prefix="/api/autonomous", tags=["autonomous"])
app.include_router(documentation.router, prefix="/api/documentation", tags=["documentation"])


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting AI Agent API")
    await init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "autonomous_mode": settings.autonomous_mode,
        "version": "1.0.0"
    }


@app.post("/api/chat")
async def chat(
    message: str,
    session_id: str = None,
    stream: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Chat with the AI agent"""
    from core.ai_agent import AIAgent
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    agent = AIAgent(session_id)
    
    if stream:
        async def generate():
            async for chunk in agent.chat(message, db, stream=True):
                yield chunk
        
        return StreamingResponse(generate(), media_type="text/plain")
    else:
        response = await agent.chat(message, db, stream=False)
        return {"response": response, "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )



