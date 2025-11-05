"""
Project session manager to track ongoing projects across multiple prompts
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger


class ProjectSession:
    """Manages project sessions for continuous development"""
    
    def __init__(self, session_dir: str = ".ai_sessions"):
        """Initialize project session manager"""
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.current_session: Optional[Dict] = None
        
    def create_session(
        self, 
        project_name: str, 
        project_path: str,
        initial_prompt: str
    ) -> str:
        """
        Create a new project session
        
        Returns:
            session_id
        """
        session_id = f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session_data = {
            "session_id": session_id,
            "project_name": project_name,
            "project_path": project_path,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "initial_prompt": initial_prompt,
            "prompts": [initial_prompt],
            "files_created": [],
            "commands_executed": [],
            "status": "active",
            "iterations": 0
        }
        
        self._save_session(session_id, session_data)
        self.current_session = session_data
        
        logger.info(f"Created session: {session_id}")
        return session_id
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load an existing session"""
        session_file = self.session_dir / f"{session_id}.json"
        
        if not session_file.exists():
            logger.warning(f"Session not found: {session_id}")
            return None
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            self.current_session = session_data
            logger.info(f"Loaded session: {session_id}")
            return session_data
        except Exception as e:
            logger.error(f"Failed to load session: {str(e)}")
            return None
    
    def update_session(
        self,
        session_id: str,
        new_prompt: Optional[str] = None,
        files_created: Optional[List[str]] = None,
        commands_executed: Optional[List[str]] = None,
        status: Optional[str] = None,
        iterations: Optional[int] = None
    ):
        """Update session data"""
        session_data = self.load_session(session_id)
        
        if not session_data:
            logger.error(f"Cannot update non-existent session: {session_id}")
            return
        
        session_data["updated_at"] = datetime.now().isoformat()
        
        if new_prompt:
            session_data["prompts"].append(new_prompt)
        
        if files_created:
            session_data["files_created"].extend(files_created)
            # Remove duplicates
            session_data["files_created"] = list(set(session_data["files_created"]))
        
        if commands_executed:
            session_data["commands_executed"].extend(commands_executed)
        
        if status:
            session_data["status"] = status
        
        if iterations is not None:
            session_data["iterations"] = iterations
        
        self._save_session(session_id, session_data)
        self.current_session = session_data
    
    def list_sessions(self, status: Optional[str] = None) -> List[Dict]:
        """List all sessions, optionally filtered by status"""
        sessions = []
        
        for session_file in self.session_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                if status is None or session_data.get("status") == status:
                    sessions.append({
                        "session_id": session_data["session_id"],
                        "project_name": session_data["project_name"],
                        "project_path": session_data["project_path"],
                        "created_at": session_data["created_at"],
                        "updated_at": session_data["updated_at"],
                        "status": session_data["status"],
                        "prompts_count": len(session_data.get("prompts", [])),
                        "files_count": len(session_data.get("files_created", []))
                    })
            except Exception as e:
                logger.error(f"Failed to read session {session_file}: {str(e)}")
        
        # Sort by updated_at
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
    
    def get_session_context(self, session_id: str) -> str:
        """Get formatted context for AI to continue working on a project"""
        session_data = self.load_session(session_id)
        
        if not session_data:
            return ""
        
        context = f"""
CONTINUING PROJECT SESSION: {session_data['project_name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Path: {session_data['project_path']}
Created: {session_data['created_at']}
Last Updated: {session_data['updated_at']}
Status: {session_data['status']}
Total Iterations: {session_data.get('iterations', 0)}

PREVIOUS PROMPTS:
{chr(10).join(f"{i+1}. {prompt}" for i, prompt in enumerate(session_data.get('prompts', [])))}

FILES CREATED ({len(session_data.get('files_created', []))}):
{chr(10).join(f"  - {file}" for file in session_data.get('files_created', [])[:20])}
{f"  ... and {len(session_data.get('files_created', [])) - 20} more" if len(session_data.get('files_created', [])) > 20 else ""}

RECENT COMMANDS ({len(session_data.get('commands_executed', []))}):
{chr(10).join(f"  $ {cmd}" for cmd in session_data.get('commands_executed', [])[-10:])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are CONTINUING to work on this project. Remember what you've built.
The user wants to make changes or improvements to the existing project.
"""
        return context
    
    def _save_session(self, session_id: str, session_data: Dict):
        """Save session to file"""
        session_file = self.session_dir / f"{session_id}.json"
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            logger.debug(f"Saved session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to save session: {str(e)}")
    
    def mark_complete(self, session_id: str):
        """Mark a session as complete"""
        self.update_session(session_id, status="complete")
    
    def mark_failed(self, session_id: str):
        """Mark a session as failed"""
        self.update_session(session_id, status="failed")





