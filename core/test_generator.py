"""
Unit test generator
"""
from typing import Dict, Optional
from pathlib import Path
from loguru import logger

from core.ai_agent import AIAgent


class TestGenerator:
    """Generates unit tests for code"""
    
    def __init__(self, agent: AIAgent):
        self.agent = agent
    
    async def generate_tests(
        self,
        code: str,
        language: str,
        test_framework: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> str:
        """
        Generate unit tests for code
        
        Args:
            code: Source code to test
            language: Programming language
            test_framework: Testing framework (auto-detect if None)
            output_file: Where to save tests
            
        Returns:
            Generated test code
        """
        # Auto-detect test framework if not provided
        if not test_framework:
            test_framework = self._detect_test_framework(language)
        
        logger.info(f"Generating tests using {test_framework} for {language}")
        
        # Generate tests using AI agent
        test_code = await self.agent.generate_tests(
            code=code,
            language=language,
            test_framework=test_framework
        )
        
        # Save to file if specified
        if output_file:
            Path(output_file).write_text(test_code)
            logger.info(f"Tests saved to {output_file}")
        
        return test_code
    
    def _detect_test_framework(self, language: str) -> str:
        """Detect appropriate test framework for language"""
        frameworks = {
            "python": "pytest",
            "javascript": "jest",
            "typescript": "jest",
            "java": "junit",
            "go": "testing",
            "rust": "cargo test",
            "ruby": "rspec",
            "php": "phpunit",
            "csharp": "nunit",
        }
        return frameworks.get(language.lower(), "unittest")
    
    async def generate_integration_tests(
        self,
        api_spec: Dict,
        language: str,
        output_file: Optional[str] = None
    ) -> str:
        """Generate integration tests for API"""
        prompt = f"""Generate integration tests for the following API specification in {language}.

API Specification:
{api_spec}

Include:
1. Tests for all endpoints
2. Authentication tests
3. Error handling tests
4. Response validation
5. Setup and teardown

Generate complete, runnable test code."""
        
        test_code = await self.agent.chat(prompt, None)
        
        if output_file:
            Path(output_file).write_text(test_code)
            logger.info(f"Integration tests saved to {output_file}")
        
        return test_code
    
    async def generate_test_fixtures(
        self,
        models: str,
        language: str
    ) -> str:
        """Generate test fixtures/mock data"""
        prompt = f"""Generate test fixtures and mock data for the following models in {language}.

Models:
{models}

Include:
1. Valid test data
2. Edge cases
3. Invalid data for error testing
4. Factory functions/classes

Generate complete fixture code."""
        
        return await self.agent.chat(prompt, None)






