"""
Automatic error detection and fixing system
"""
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import ErrorLog
from core.ai_agent import AIAgent


class ErrorHandler:
    """Detects and automatically fixes errors"""
    
    def __init__(self, agent: AIAgent):
        self.agent = agent
        self.error_patterns = self._load_error_patterns()
    
    def _load_error_patterns(self) -> Dict:
        """Load common error patterns and their solutions"""
        return {
            "python": {
                r"ModuleNotFoundError: No module named '(\w+)'": "missing_module",
                r"ImportError: cannot import name '(\w+)'": "import_error",
                r"SyntaxError: (.+)": "syntax_error",
                r"IndentationError: (.+)": "indentation_error",
                r"TypeError: (.+)": "type_error",
                r"ValueError: (.+)": "value_error",
                r"AttributeError: '(\w+)' object has no attribute '(\w+)'": "attribute_error",
                r"KeyError: '(\w+)'": "key_error",
                r"FileNotFoundError: (.+)": "file_not_found",
            },
            "javascript": {
                r"Cannot find module '(.+)'": "missing_module",
                r"ReferenceError: (.+) is not defined": "undefined_reference",
                r"TypeError: (.+)": "type_error",
                r"SyntaxError: (.+)": "syntax_error",
                r"RangeError: (.+)": "range_error",
            },
            "typescript": {
                r"Cannot find module '(.+)'": "missing_module",
                r"Property '(\w+)' does not exist": "property_error",
                r"Type '(.+)' is not assignable to type '(.+)'": "type_mismatch",
            },
            "go": {
                r"undefined: (\w+)": "undefined_symbol",
                r"cannot find package \"(.+)\"": "missing_package",
                r"syntax error: (.+)": "syntax_error",
            },
            "rust": {
                r"cannot find value `(\w+)` in this scope": "undefined_value",
                r"cannot find type `(\w+)` in this scope": "undefined_type",
                r"mismatched types": "type_mismatch",
            }
        }
    
    async def detect_error(
        self,
        output: str,
        language: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Detect error from output
        
        Returns:
            Dict with error info or None if no error detected
        """
        if not output:
            return None
        
        # Try to identify language if not provided
        if not language:
            language = self._identify_language(output)
        
        # Get patterns for language
        patterns = self.error_patterns.get(language, {})
        
        # Try to match error patterns
        for pattern, error_type in patterns.items():
            match = re.search(pattern, output, re.MULTILINE)
            if match:
                return {
                    "error_type": error_type,
                    "error_message": match.group(0),
                    "matched_groups": match.groups(),
                    "language": language,
                    "full_output": output
                }
        
        # Check for generic error indicators
        error_indicators = ["error:", "exception:", "failed:", "fatal:"]
        lower_output = output.lower()
        
        for indicator in error_indicators:
            if indicator in lower_output:
                # Extract error message
                lines = output.split('\n')
                error_lines = [line for line in lines if indicator in line.lower()]
                if error_lines:
                    return {
                        "error_type": "generic_error",
                        "error_message": error_lines[0],
                        "language": language or "unknown",
                        "full_output": output
                    }
        
        return None
    
    def _identify_language(self, output: str) -> str:
        """Try to identify programming language from error output"""
        if "python" in output.lower() or "pip" in output.lower():
            return "python"
        elif "node" in output.lower() or "npm" in output.lower():
            return "javascript"
        elif "typescript" in output.lower() or "tsc" in output.lower():
            return "typescript"
        elif "cargo" in output.lower() or "rustc" in output.lower():
            return "rust"
        elif "go build" in output.lower() or "go run" in output.lower():
            return "go"
        return "unknown"
    
    async def fix_error(
        self,
        db: AsyncSession,
        error_info: Dict,
        code: Optional[str] = None,
        context: Optional[Dict] = None,
        auto_apply: bool = False
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Attempt to fix an error
        
        Args:
            db: Database session
            error_info: Error information from detect_error
            code: Source code that caused the error
            context: Additional context
            auto_apply: Whether to automatically apply the fix
            
        Returns:
            Tuple of (success, fix_description, fixed_code)
        """
        # Log the error
        error_log = ErrorLog(
            error_type=error_info["error_type"],
            error_message=error_info["error_message"],
            stack_trace=error_info.get("full_output"),
            context=code,
            auto_fixed=auto_apply,
            created_at=datetime.utcnow(),
            metadata={
                "language": error_info.get("language"),
                "matched_groups": error_info.get("matched_groups", [])
            }
        )
        db.add(error_log)
        await db.commit()
        await db.refresh(error_log)
        
        # Try automated fix first
        automated_fix = await self._try_automated_fix(error_info, code)
        if automated_fix:
            success, fix_desc, fixed_code = automated_fix
            if success:
                error_log.fix_applied = fix_desc
                error_log.fix_successful = True
                error_log.fixed_at = datetime.utcnow()
                await db.commit()
                logger.info(f"Automated fix applied for {error_info['error_type']}")
                return True, fix_desc, fixed_code
        
        # Use AI agent for complex fixes
        fix_result = await self.agent.fix_error(
            error_message=error_info["error_message"],
            code=code,
            context=str(context) if context else None
        )
        
        fix_description = fix_result.get("fix", "")
        
        # Extract fixed code from AI response
        fixed_code = self._extract_code_from_response(fix_description, error_info.get("language"))
        
        if fixed_code:
            error_log.fix_applied = fix_description
            error_log.fix_successful = auto_apply  # Mark as successful if auto-applied
            if auto_apply:
                error_log.fixed_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"AI-generated fix for {error_info['error_type']}")
            return True, fix_description, fixed_code
        
        # Update error log with fix attempt
        error_log.fix_applied = fix_description
        error_log.fix_successful = False
        await db.commit()
        
        return False, fix_description, None
    
    async def _try_automated_fix(
        self,
        error_info: Dict,
        code: Optional[str]
    ) -> Optional[Tuple[bool, str, str]]:
        """Try simple automated fixes for common errors"""
        error_type = error_info["error_type"]
        
        # Missing module fixes
        if error_type == "missing_module":
            matched = error_info.get("matched_groups", [])
            if matched:
                module_name = matched[0]
                fix_desc = f"Install missing module: {module_name}"
                return True, fix_desc, None
        
        # Indentation errors
        elif error_type == "indentation_error" and code:
            # Try to fix indentation
            lines = code.split('\n')
            fixed_lines = [line.replace('\t', '    ') for line in lines]
            fixed_code = '\n'.join(fixed_lines)
            return True, "Fixed indentation (converted tabs to spaces)", fixed_code
        
        return None
    
    def _extract_code_from_response(
        self,
        response: str,
        language: Optional[str]
    ) -> Optional[str]:
        """Extract code blocks from AI response"""
        # Look for code blocks
        pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        return None
    
    async def get_error_history(
        self,
        db: AsyncSession,
        error_type: Optional[str] = None,
        limit: int = 10
    ) -> List[ErrorLog]:
        """Get error history"""
        stmt = select(ErrorLog).order_by(ErrorLog.created_at.desc())
        
        if error_type:
            stmt = stmt.where(ErrorLog.error_type == error_type)
        
        stmt = stmt.limit(limit)
        
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_fix_success_rate(
        self,
        db: AsyncSession,
        error_type: Optional[str] = None
    ) -> Dict:
        """Calculate fix success rate"""
        from sqlalchemy import func, case
        
        stmt = select(
            func.count(ErrorLog.id).label("total"),
            func.sum(case((ErrorLog.fix_successful == True, 1), else_=0)).label("successful")
        )
        
        if error_type:
            stmt = stmt.where(ErrorLog.error_type == error_type)
        
        result = await db.execute(stmt)
        row = result.first()
        
        total = row.total or 0
        successful = row.successful or 0
        
        return {
            "total_errors": total,
            "fixed_successfully": successful,
            "success_rate": (successful / total * 100) if total > 0 else 0
        }



