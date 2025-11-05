"""Tasks API routes"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from database import get_db, Task

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str
    project_id: Optional[int] = None
    priority: int = 5
    autonomous: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    task_type: str
    status: str
    priority: int
    autonomous: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new task"""
    new_task = Task(
        title=task.title,
        description=task.description,
        task_type=task.task_type,
        project_id=task.project_id,
        priority=task.priority,
        autonomous=task.autonomous,
        status="pending"
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    return new_task


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List tasks"""
    stmt = select(Task)
    
    if status:
        stmt = stmt.where(Task.status == status)
    if project_id:
        stmt = stmt.where(Task.project_id == project_id)
    
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific task"""
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: int,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    """Update task status"""
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    
    if status == "in_progress" and not task.started_at:
        task.started_at = datetime.utcnow()
    elif status == "completed":
        task.completed_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "Task status updated", "status": status}






