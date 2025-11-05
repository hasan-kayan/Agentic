"""Terminal API routes"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, get_personalization_db
from core.terminal_executor import TerminalExecutor

router = APIRouter()


class CommandExecute(BaseModel):
    command: str
    use_sudo: bool = False
    cwd: Optional[str] = None
    timeout: int = 300


class CommandResponse(BaseModel):
    success: bool
    stdout: str
    stderr: str


@router.post("/execute", response_model=CommandResponse)
async def execute_command(
    cmd: CommandExecute,
    db: AsyncSession = Depends(get_db),
    personalization_db: AsyncSession = Depends(get_personalization_db)
):
    """Execute a terminal command"""
    terminal = TerminalExecutor()
    
    success, stdout, stderr = await terminal.execute(
        command=cmd.command,
        db=db,
        personalization_db=personalization_db,
        use_sudo=cmd.use_sudo,
        timeout=cmd.timeout,
        cwd=cmd.cwd
    )
    
    return {
        "success": success,
        "stdout": stdout,
        "stderr": stderr
    }


@router.get("/system-info")
async def get_system_info():
    """Get system information"""
    terminal = TerminalExecutor()
    info = await terminal.get_system_info()
    return info


@router.post("/install-package")
async def install_package(
    package: str,
    package_manager: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    personalization_db: AsyncSession = Depends(get_personalization_db)
):
    """Install a package"""
    terminal = TerminalExecutor()
    
    success = await terminal.install_package(
        package=package,
        db=db,
        personalization_db=personalization_db,
        package_manager=package_manager
    )
    
    return {
        "success": success,
        "message": f"Package {package} {'installed successfully' if success else 'installation failed'}"
    }

