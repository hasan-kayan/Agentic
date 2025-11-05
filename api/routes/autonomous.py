"""Autonomous mode API routes"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, get_personalization_db, PermissionGrant
from core.autonomous_manager import AutonomousManager
from core.autonomous_agent import AutonomousAgent

router = APIRouter()
autonomous_manager = AutonomousManager()


class PermissionGrantRequest(BaseModel):
    permission_type: str
    scope: Optional[str] = None
    grant_level: str = "limited"
    duration_hours: Optional[int] = None
    requires_confirmation: bool = False


class PermissionResponse(BaseModel):
    id: int
    permission_type: str
    scope: Optional[str]
    granted: bool
    grant_level: str
    requires_confirmation: bool
    
    class Config:
        from_attributes = True


@router.post("/enable")
async def enable_autonomous_mode(max_actions: Optional[int] = None):
    """Enable autonomous mode"""
    autonomous_manager.enable_autonomous_mode(max_actions)
    
    return {
        "message": "Autonomous mode enabled",
        "max_actions": autonomous_manager.max_actions
    }


@router.post("/disable")
async def disable_autonomous_mode():
    """Disable autonomous mode"""
    autonomous_manager.disable_autonomous_mode()
    
    return {"message": "Autonomous mode disabled"}


@router.get("/status")
async def get_autonomous_status():
    """Get autonomous mode status"""
    return {
        "autonomous_mode": autonomous_manager.autonomous_mode,
        "action_count": autonomous_manager.action_count,
        "max_actions": autonomous_manager.max_actions,
        "require_confirmation": autonomous_manager.require_confirmation
    }


@router.post("/permissions", response_model=PermissionResponse)
async def grant_permission(
    permission: PermissionGrantRequest,
    db: AsyncSession = Depends(get_personalization_db)
):
    """Grant a permission"""
    granted = await autonomous_manager.grant_permission(
        db=db,
        permission_type=permission.permission_type,
        scope=permission.scope,
        grant_level=permission.grant_level,
        duration_hours=permission.duration_hours,
        requires_confirmation=permission.requires_confirmation
    )
    
    return granted


@router.get("/permissions", response_model=List[PermissionResponse])
async def list_permissions(
    active_only: bool = True,
    db: AsyncSession = Depends(get_personalization_db)
):
    """List all permissions"""
    permissions = await autonomous_manager.list_permissions(
        db=db,
        active_only=active_only
    )
    
    return permissions


@router.delete("/permissions/{permission_type}")
async def revoke_permission(
    permission_type: str,
    scope: Optional[str] = None,
    db: AsyncSession = Depends(get_personalization_db)
):
    """Revoke a permission"""
    success = await autonomous_manager.revoke_permission(
        db=db,
        permission_type=permission_type,
        scope=scope
    )
    
    return {
        "success": success,
        "message": "Permission revoked" if success else "Permission not found"
    }


@router.post("/reset-counter")
async def reset_action_counter():
    """Reset the action counter"""
    autonomous_manager.reset_action_count()
    
    return {"message": "Action counter reset"}


@router.post("/confirmation-requirement")
async def set_confirmation_requirement(required: bool):
    """Set confirmation requirement"""
    autonomous_manager.set_confirmation_requirement(required)
    
    return {
        "message": f"Confirmation requirement set to {required}",
        "require_confirmation": required
    }


class ExecuteTaskRequest(BaseModel):
    task: str
    session_id: Optional[str] = None
    max_iterations: int = 50


@router.post("/execute")
async def execute_autonomous_task(
    request: ExecuteTaskRequest,
    db: AsyncSession = Depends(get_db),
    p_db: AsyncSession = Depends(get_personalization_db)
) -> Dict[str, Any]:
    """Execute an autonomous task"""
    
    # Create agent
    session_id = request.session_id or str(__import__('uuid').uuid4())
    agent = AutonomousAgent(
        session_id=session_id,
        max_iterations=request.max_iterations
    )
    
    # Execute task
    result = await agent.execute_autonomous_task(
        task=request.task,
        db=db,
        personalization_db=p_db
    )
    
    return result





