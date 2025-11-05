"""Projects API routes"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, get_personalization_db, Project
from core.ai_agent import AIAgent
from core.terminal_executor import TerminalExecutor
from core.project_generator import ProjectGenerator

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    project_type: str
    language: str
    framework: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    output_dir: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    path: str
    description: Optional[str]
    project_type: str
    language: str
    framework: Optional[str]
    status: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    personalization_db: AsyncSession = Depends(get_personalization_db)
):
    """Create a new project"""
    agent = AIAgent(session_id="project_creation")
    terminal = TerminalExecutor()
    generator = ProjectGenerator(agent, terminal)
    
    new_project = await generator.create_project(
        db=db,
        personalization_db=personalization_db,
        name=project.name,
        project_type=project.project_type,
        language=project.language,
        framework=project.framework,
        description=project.description,
        features=project.features,
        output_dir=project.output_dir
    )
    
    return new_project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all projects"""
    stmt = select(Project)
    
    if status:
        stmt = stmt.where(Project.status == status)
    
    result = await db.execute(stmt)
    projects = result.scalars().all()
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific project"""
    stmt = select(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project"""
    stmt = select(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}






