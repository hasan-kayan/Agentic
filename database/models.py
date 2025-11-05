"""
Database models for the AI Agent system
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Project(Base):
    """Stores information about generated projects"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    path = Column(String(512), nullable=False, unique=True)
    description = Column(Text)
    project_type = Column(String(100))  # backend, frontend, fullstack, etc.
    language = Column(String(50))
    framework = Column(String(100))
    status = Column(String(50), default="active")  # active, archived, deleted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_metadata = Column(JSON)  # Store additional project metadata
    
    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    """Stores tasks and their execution history"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    task_type = Column(String(100))  # code_generation, test_writing, debugging, etc.
    status = Column(String(50), default="pending")  # pending, in_progress, completed, failed
    priority = Column(Integer, default=5)
    autonomous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    extra_metadata = Column(JSON)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    actions = relationship("Action", back_populates="task", cascade="all, delete-orphan")


class Action(Base):
    """Stores individual actions taken by the AI"""
    __tablename__ = "actions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    action_type = Column(String(100), nullable=False)  # terminal_command, file_write, api_call, etc.
    command = Column(Text)
    output = Column(Text)
    status = Column(String(50), default="pending")  # pending, running, success, failed
    requires_sudo = Column(Boolean, default=False)
    autonomous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    extra_metadata = Column(JSON)
    
    # Relationships
    task = relationship("Task", back_populates="actions")
    project = relationship("Project", back_populates="actions")


class Conversation(Base):
    """Stores conversation history with the AI"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column(JSON)


class ErrorLog(Base):
    """Stores errors and their automatic fixes"""
    __tablename__ = "error_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    context = Column(Text)  # Code or command that caused the error
    fix_applied = Column(Text, nullable=True)
    fix_successful = Column(Boolean, default=False)
    auto_fixed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    fixed_at = Column(DateTime, nullable=True)
    extra_metadata = Column(JSON)


class SearchQuery(Base):
    """Stores code search queries and results"""
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    search_type = Column(String(50))  # web, documentation, code_example
    results = Column(JSON)
    used_in_code = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column(JSON)


class Documentation(Base):
    """Stores generated documentation"""
    __tablename__ = "documentation"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=True)
    doc_type = Column(String(100))  # api, readme, inline, architecture
    title = Column(String(255))
    content = Column(Text, nullable=False)
    format = Column(String(50), default="markdown")  # markdown, html, pdf
    file_path = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_metadata = Column(JSON)


