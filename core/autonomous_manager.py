"""
Autonomous operation manager with permission controls
"""
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.personalization_models import PermissionGrant
from config import settings


class AutonomousManager:
    """Manages autonomous AI operations with permission controls"""
    
    def __init__(self):
        self.autonomous_mode = settings.autonomous_mode
        self.max_actions = settings.max_autonomous_actions
        self.require_confirmation = settings.require_confirmation
        self.action_count = 0
        self.permission_cache: Dict[str, bool] = {}
    
    async def can_execute(
        self,
        db: AsyncSession,
        action_type: str,
        scope: Optional[str] = None,
        requires_sudo: bool = False
    ) -> bool:
        """
        Check if an action can be executed autonomously
        
        Args:
            db: Personalization database session
            action_type: Type of action (terminal, file_system, network, sudo)
            scope: Specific scope (directory, command pattern, etc.)
            requires_sudo: Whether action requires sudo
            
        Returns:
            True if action can be executed
        """
        # Check if autonomous mode is enabled
        if not self.autonomous_mode:
            return False
        
        # Check action count limit
        if self.action_count >= self.max_actions:
            logger.warning(f"Max autonomous actions reached: {self.max_actions}")
            return False
        
        # If confirmation is required globally, return False
        if self.require_confirmation:
            return False
        
        # Check permission cache first
        cache_key = f"{action_type}:{scope}:{requires_sudo}"
        if cache_key in self.permission_cache:
            return self.permission_cache[cache_key]
        
        # Check database for permission
        has_permission = await self._check_permission(
            db, action_type, scope, requires_sudo
        )
        
        # Cache the result
        self.permission_cache[cache_key] = has_permission
        
        return has_permission
    
    async def _check_permission(
        self,
        db: AsyncSession,
        action_type: str,
        scope: Optional[str],
        requires_sudo: bool
    ) -> bool:
        """Check permission in database"""
        # If sudo is required, check for sudo permission
        if requires_sudo:
            stmt = select(PermissionGrant).where(
                PermissionGrant.permission_type == "sudo",
                PermissionGrant.granted == True,
                PermissionGrant.revoked_at.is_(None)
            )
            result = await db.execute(stmt)
            sudo_permission = result.scalar_one_or_none()
            
            if not sudo_permission:
                return False
            
            # Check if permission has expired
            if sudo_permission.expires_at and sudo_permission.expires_at < datetime.utcnow():
                return False
        
        # Check for specific action type permission
        stmt = select(PermissionGrant).where(
            PermissionGrant.permission_type == action_type,
            PermissionGrant.granted == True,
            PermissionGrant.revoked_at.is_(None)
        )
        
        if scope:
            stmt = stmt.where(PermissionGrant.scope == scope)
        
        result = await db.execute(stmt)
        permission = result.scalar_one_or_none()
        
        if not permission:
            return False
        
        # Check expiration
        if permission.expires_at and permission.expires_at < datetime.utcnow():
            return False
        
        # Check confirmation requirement
        if permission.requires_confirmation:
            return False
        
        return True
    
    async def grant_permission(
        self,
        db: AsyncSession,
        permission_type: str,
        scope: Optional[str] = None,
        grant_level: str = "limited",
        duration_hours: Optional[int] = None,
        requires_confirmation: bool = False
    ) -> PermissionGrant:
        """
        Grant a permission
        
        Args:
            db: Personalization database session
            permission_type: Type (terminal, file_system, network, sudo)
            scope: Specific scope
            grant_level: Grant level (limited, moderate, full)
            duration_hours: How long permission lasts (None = indefinite)
            requires_confirmation: Whether to require confirmation
        """
        expires_at = None
        if duration_hours:
            expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        
        # Check if permission already exists
        stmt = select(PermissionGrant).where(
            PermissionGrant.permission_type == permission_type,
            PermissionGrant.scope == scope,
            PermissionGrant.revoked_at.is_(None)
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing permission
            existing.granted = True
            existing.grant_level = grant_level
            existing.expires_at = expires_at
            existing.requires_confirmation = requires_confirmation
            existing.granted_at = datetime.utcnow()
            permission = existing
        else:
            # Create new permission
            permission = PermissionGrant(
                permission_type=permission_type,
                scope=scope,
                granted=True,
                grant_level=grant_level,
                expires_at=expires_at,
                requires_confirmation=requires_confirmation,
                granted_at=datetime.utcnow()
            )
            db.add(permission)
        
        await db.commit()
        await db.refresh(permission)
        
        # Clear cache
        self.permission_cache.clear()
        
        logger.info(f"Permission granted: {permission_type} ({grant_level})")
        return permission
    
    async def revoke_permission(
        self,
        db: AsyncSession,
        permission_type: str,
        scope: Optional[str] = None
    ) -> bool:
        """Revoke a permission"""
        stmt = select(PermissionGrant).where(
            PermissionGrant.permission_type == permission_type,
            PermissionGrant.revoked_at.is_(None)
        )
        
        if scope:
            stmt = stmt.where(PermissionGrant.scope == scope)
        
        result = await db.execute(stmt)
        permission = result.scalar_one_or_none()
        
        if permission:
            permission.granted = False
            permission.revoked_at = datetime.utcnow()
            await db.commit()
            
            # Clear cache
            self.permission_cache.clear()
            
            logger.info(f"Permission revoked: {permission_type}")
            return True
        
        return False
    
    async def list_permissions(
        self,
        db: AsyncSession,
        active_only: bool = True
    ) -> List[PermissionGrant]:
        """List all permissions"""
        stmt = select(PermissionGrant)
        
        if active_only:
            stmt = stmt.where(
                PermissionGrant.granted == True,
                PermissionGrant.revoked_at.is_(None)
            )
        
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def request_confirmation(
        self,
        action_description: str,
        action_type: str,
        details: Optional[Dict] = None
    ) -> bool:
        """
        Request user confirmation for an action
        
        In a real implementation, this would:
        - Display the action to the user
        - Wait for user input
        - Return True if approved, False if denied
        
        For now, returns False (no automatic approval)
        """
        logger.info(f"Confirmation requested: {action_description}")
        logger.info(f"Type: {action_type}")
        if details:
            logger.info(f"Details: {details}")
        
        # In production, this would integrate with a UI or CLI prompt
        return False
    
    def increment_action_count(self):
        """Increment the autonomous action counter"""
        self.action_count += 1
        logger.debug(f"Autonomous actions: {self.action_count}/{self.max_actions}")
    
    def reset_action_count(self):
        """Reset the action counter"""
        self.action_count = 0
        logger.info("Autonomous action counter reset")
    
    def enable_autonomous_mode(self, max_actions: Optional[int] = None):
        """Enable autonomous mode"""
        self.autonomous_mode = True
        if max_actions:
            self.max_actions = max_actions
        self.reset_action_count()
        logger.info(f"Autonomous mode enabled (max actions: {self.max_actions})")
    
    def disable_autonomous_mode(self):
        """Disable autonomous mode"""
        self.autonomous_mode = False
        logger.info("Autonomous mode disabled")
    
    def set_confirmation_requirement(self, required: bool):
        """Set whether confirmation is required"""
        self.require_confirmation = required
        logger.info(f"Confirmation requirement: {required}")
    
    async def execute_with_permission(
        self,
        db: AsyncSession,
        action_type: str,
        action_func: Callable,
        *args,
        scope: Optional[str] = None,
        requires_sudo: bool = False,
        **kwargs
    ) -> Any:
        """
        Execute an action with permission check
        
        Args:
            db: Personalization database session
            action_type: Type of action
            action_func: Function to execute
            scope: Action scope
            requires_sudo: Whether sudo is required
            *args, **kwargs: Arguments for action_func
        """
        # Check permission
        can_execute = await self.can_execute(
            db, action_type, scope, requires_sudo
        )
        
        if not can_execute:
            if not self.autonomous_mode:
                logger.warning("Autonomous mode is disabled")
            else:
                logger.warning(f"Permission denied for {action_type}")
            return None
        
        # Execute the action
        try:
            result = await action_func(*args, **kwargs)
            self.increment_action_count()
            return result
        except Exception as e:
            logger.error(f"Action execution failed: {str(e)}")
            raise



