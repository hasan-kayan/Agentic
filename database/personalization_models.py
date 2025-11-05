"""
Personalization database models for storing sensitive user data
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

PersonalizationBase = declarative_base()


class Credential(PersonalizationBase):
    """Stores encrypted user credentials"""
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    credential_type = Column(String(100), nullable=False)  # sudo_password, api_key, ssh_key, etc.
    identifier = Column(String(255), nullable=False)  # username, service name, etc.
    encrypted_value = Column(Text, nullable=False)
    description = Column(Text)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_metadata = Column(JSON)


class UserPreference(PersonalizationBase):
    """Stores user preferences and settings"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)  # coding_style, tools, behavior, etc.
    key = Column(String(255), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    value_type = Column(String(50), default="string")  # string, int, bool, json
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemInfo(PersonalizationBase):
    """Stores system configuration and environment information"""
    __tablename__ = "system_info"
    
    id = Column(Integer, primary_key=True, index=True)
    os_type = Column(String(50), nullable=False)  # macos, linux
    os_version = Column(String(100))
    hostname = Column(String(255))
    username = Column(String(255))
    shell = Column(String(100))
    home_directory = Column(String(512))
    installed_tools = Column(JSON)  # List of installed development tools
    environment_variables = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_metadata = Column(JSON)


class LearningData(PersonalizationBase):
    """Stores learned patterns and preferences from user interactions"""
    __tablename__ = "learning_data"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_type = Column(String(100), nullable=False)  # coding_pattern, workflow, preference
    pattern_name = Column(String(255), nullable=False)
    pattern_data = Column(JSON, nullable=False)
    confidence_score = Column(Integer, default=50)  # 0-100
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PermissionGrant(PersonalizationBase):
    """Stores user permission grants for autonomous operations"""
    __tablename__ = "permission_grants"
    
    id = Column(Integer, primary_key=True, index=True)
    permission_type = Column(String(100), nullable=False)  # terminal, file_system, network, sudo
    scope = Column(String(255))  # specific directory, command pattern, etc.
    granted = Column(Boolean, default=False)
    requires_confirmation = Column(Boolean, default=True)
    grant_level = Column(String(50), default="limited")  # limited, moderate, full
    expires_at = Column(DateTime, nullable=True)
    granted_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    extra_metadata = Column(JSON)


