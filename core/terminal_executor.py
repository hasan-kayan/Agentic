"""
Terminal command executor with permission controls
"""
import os
import platform
import subprocess
import asyncio
from typing import Optional, Dict, Tuple
from loguru import logger


class TerminalExecutor:
    """Execute terminal commands with security controls"""
    
    def __init__(self):
        """Initialize terminal executor"""
        self.os_type = platform.system().lower()
        
        # Determine shell based on OS
        if self.os_type == "windows":
            self.shell = "cmd.exe"
        else:
            self.shell = os.environ.get("SHELL", "/bin/bash")
        
        logger.info(f"Terminal executor initialized: OS={self.os_type}, Shell={self.shell}")
    
    async def execute(
        self,
        command: str,
        use_sudo: bool = False,
        timeout: int = 60,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Tuple[int, str, str]:
        """
        Execute a terminal command
        
        Args:
            command: Command to execute
            use_sudo: Whether to use sudo
            timeout: Command timeout in seconds
            cwd: Working directory
            env: Environment variables
            
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        if use_sudo and self.os_type != "windows":
            command = f"sudo {command}"
        
        logger.info(f"Executing command: {command}")
        
        try:
            # Execute command asynchronously
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise TimeoutError(f"Command timed out after {timeout} seconds")
            
            exit_code = process.returncode
            stdout_str = stdout.decode('utf-8') if stdout else ""
            stderr_str = stderr.decode('utf-8') if stderr else ""
            
            logger.debug(f"Command exit code: {exit_code}")
            
            return exit_code, stdout_str, stderr_str
            
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            raise
    
    async def check_command_exists(self, command: str) -> bool:
        """
        Check if a command exists on the system
        
        Args:
            command: Command name to check
            
        Returns:
            True if command exists
        """
        if self.os_type == "windows":
            check_cmd = f"where {command}"
        else:
            check_cmd = f"command -v {command}"
        
        try:
            exit_code, stdout, stderr = await self.execute(
                check_cmd,
                timeout=5
            )
            return exit_code == 0
        except Exception:
            return False
    
    async def get_os_info(self) -> Dict[str, str]:
        """Get operating system information"""
        return {
            "os_type": self.os_type,
            "shell": self.shell,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python_version": platform.python_version()
        }

