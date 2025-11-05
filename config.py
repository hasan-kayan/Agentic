"""
Configuration management for the AI Agent system
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    openai_api_key: str = "sk-test-placeholder"
    openai_model: str = "gpt-4-turbo-preview"
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./ai_agent.db"
    personalization_db_url: str = "sqlite+aiosqlite:///./personalization.db"
    
    # Security
    secret_key: str = "test-secret-key"
    encryption_key: str = "test-encryption-key"
    
    # Agent Configuration
    autonomous_mode: bool = False
    max_autonomous_actions: int = 100
    require_confirmation: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/ai_agent.log"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Paths
    base_dir: Path = Path(__file__).parent
    data_dir: Path = base_dir / "data"
    logs_dir: Path = base_dir / "logs"
    projects_dir: Path = base_dir / "generated_projects"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create necessary directories
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()


