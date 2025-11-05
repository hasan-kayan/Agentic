"""
Tool installer and package manager
"""
import platform
from typing import Dict, List, Optional
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.terminal_executor import TerminalExecutor


class ToolInstaller:
    """Manages installation of development tools and packages"""
    
    def __init__(self, terminal: TerminalExecutor):
        self.terminal = terminal
        self.os_type = platform.system().lower()
        self.installed_tools: Dict[str, bool] = {}
    
    async def ensure_tool_installed(
        self,
        tool: str,
        db: AsyncSession,
        personalization_db: AsyncSession,
        task_id: Optional[int] = None
    ) -> bool:
        """
        Ensure a tool is installed, install if necessary
        
        Args:
            tool: Tool name
            db: Main database session
            personalization_db: Personalization database session
            task_id: Associated task ID
            
        Returns:
            True if tool is available
        """
        # Check cache first
        if tool in self.installed_tools:
            return self.installed_tools[tool]
        
        # Check if tool is installed
        is_installed = await self.terminal.check_command_exists(tool)
        
        if is_installed:
            logger.info(f"Tool already installed: {tool}")
            self.installed_tools[tool] = True
            return True
        
        # Try to install
        logger.info(f"Installing tool: {tool}")
        success = await self.install_tool(
            tool, db, personalization_db, task_id
        )
        
        self.installed_tools[tool] = success
        return success
    
    async def install_tool(
        self,
        tool: str,
        db: AsyncSession,
        personalization_db: AsyncSession,
        task_id: Optional[int] = None
    ) -> bool:
        """Install a specific tool"""
        # Get installation command for the tool
        install_cmd = self._get_install_command(tool)
        
        if not install_cmd:
            logger.error(f"No installation method found for {tool}")
            return False
        
        logger.info(f"Installing {tool} with command: {install_cmd}")
        
        # Execute installation
        success, stdout, stderr = await self.terminal.execute(
            install_cmd,
            db,
            personalization_db,
            task_id=task_id,
            use_sudo=self._requires_sudo(tool),
            timeout=600
        )
        
        if success:
            logger.info(f"Successfully installed {tool}")
            return True
        else:
            logger.error(f"Failed to install {tool}: {stderr}")
            return False
    
    def _get_install_command(self, tool: str) -> Optional[str]:
        """Get installation command for a tool"""
        # Tool-specific installation commands
        install_commands = {
            # macOS/Linux common tools
            "git": self._get_package_install_cmd("git"),
            "docker": self._get_docker_install_cmd(),
            "docker-compose": self._get_package_install_cmd("docker-compose"),
            "node": self._get_node_install_cmd(),
            "npm": self._get_node_install_cmd(),
            "yarn": "npm install -g yarn",
            "python3": self._get_package_install_cmd("python3"),
            "pip": self._get_package_install_cmd("python3-pip"),
            "go": self._get_go_install_cmd(),
            "rust": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
            "cargo": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
            "kubectl": self._get_kubectl_install_cmd(),
            "terraform": self._get_terraform_install_cmd(),
            "aws": self._get_aws_cli_install_cmd(),
            "gcloud": self._get_gcloud_install_cmd(),
            "psql": self._get_package_install_cmd("postgresql"),
            "mysql": self._get_package_install_cmd("mysql"),
            "redis-cli": self._get_package_install_cmd("redis"),
            "mongodb": self._get_mongodb_install_cmd(),
        }
        
        return install_commands.get(tool)
    
    def _get_package_install_cmd(self, package: str) -> str:
        """Get generic package install command based on OS"""
        if self.os_type == "darwin":
            return f"brew install {package}"
        elif self.os_type == "linux":
            return f"apt-get install -y {package}"
        return ""
    
    def _get_docker_install_cmd(self) -> str:
        """Get Docker installation command"""
        if self.os_type == "darwin":
            return "brew install --cask docker"
        elif self.os_type == "linux":
            return """curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"""
        return ""
    
    def _get_node_install_cmd(self) -> str:
        """Get Node.js installation command"""
        if self.os_type == "darwin":
            return "brew install node"
        elif self.os_type == "linux":
            return """curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get install -y nodejs"""
        return ""
    
    def _get_go_install_cmd(self) -> str:
        """Get Go installation command"""
        if self.os_type == "darwin":
            return "brew install go"
        elif self.os_type == "linux":
            return "wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz"
        return ""
    
    def _get_kubectl_install_cmd(self) -> str:
        """Get kubectl installation command"""
        if self.os_type == "darwin":
            return "brew install kubectl"
        elif self.os_type == "linux":
            return """curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl"""
        return ""
    
    def _get_terraform_install_cmd(self) -> str:
        """Get Terraform installation command"""
        if self.os_type == "darwin":
            return "brew install terraform"
        elif self.os_type == "linux":
            return """wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && apt update && apt install terraform"""
        return ""
    
    def _get_aws_cli_install_cmd(self) -> str:
        """Get AWS CLI installation command"""
        if self.os_type == "darwin":
            return "brew install awscli"
        elif self.os_type == "linux":
            return """curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install"""
        return ""
    
    def _get_gcloud_install_cmd(self) -> str:
        """Get Google Cloud SDK installation command"""
        if self.os_type == "darwin":
            return "brew install --cask google-cloud-sdk"
        elif self.os_type == "linux":
            return """echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && apt-get update && apt-get install google-cloud-sdk"""
        return ""
    
    def _get_mongodb_install_cmd(self) -> str:
        """Get MongoDB installation command"""
        if self.os_type == "darwin":
            return "brew tap mongodb/brew && brew install mongodb-community"
        elif self.os_type == "linux":
            return """curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor && echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && apt-get update && apt-get install -y mongodb-org"""
        return ""
    
    def _requires_sudo(self, tool: str) -> bool:
        """Check if tool installation requires sudo"""
        # On Linux, most system packages require sudo
        if self.os_type == "linux":
            # Tools installed via package managers need sudo
            sudo_tools = [
                "git", "docker", "python3", "pip", "postgresql", "mysql",
                "redis", "mongodb", "kubectl", "terraform", "aws", "gcloud"
            ]
            return tool in sudo_tools
        
        # On macOS with Homebrew, typically no sudo needed
        return False
    
    async def install_python_package(
        self,
        package: str,
        db: AsyncSession,
        personalization_db: AsyncSession,
        version: Optional[str] = None,
        task_id: Optional[int] = None
    ) -> bool:
        """Install a Python package with pip"""
        package_spec = f"{package}=={version}" if version else package
        command = f"pip install {package_spec}"
        
        success, _, stderr = await self.terminal.execute(
            command, db, personalization_db, task_id=task_id, timeout=300
        )
        
        if success:
            logger.info(f"Installed Python package: {package_spec}")
        else:
            logger.error(f"Failed to install {package_spec}: {stderr}")
        
        return success
    
    async def install_npm_package(
        self,
        package: str,
        db: AsyncSession,
        personalization_db: AsyncSession,
        global_install: bool = True,
        task_id: Optional[int] = None
    ) -> bool:
        """Install an npm package"""
        flag = "-g" if global_install else ""
        command = f"npm install {flag} {package}"
        
        success, _, stderr = await self.terminal.execute(
            command, db, personalization_db, task_id=task_id, timeout=300
        )
        
        if success:
            logger.info(f"Installed npm package: {package}")
        else:
            logger.error(f"Failed to install {package}: {stderr}")
        
        return success
    
    async def check_system_requirements(
        self,
        requirements: List[str]
    ) -> Dict[str, bool]:
        """Check if system requirements are met"""
        results = {}
        
        for tool in requirements:
            is_installed = await self.terminal.check_command_exists(tool)
            results[tool] = is_installed
            self.installed_tools[tool] = is_installed
        
        return results






