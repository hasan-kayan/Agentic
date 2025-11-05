"""
Documentation generator
"""
import os
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Documentation
from core.ai_agent import AIAgent


class DocumentationGenerator:
    """Generates various types of documentation"""
    
    def __init__(self, agent: AIAgent):
        self.agent = agent
    
    async def generate_readme(
        self,
        db: AsyncSession,
        project_path: str,
        project_info: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """Generate README.md for a project"""
        logger.info(f"Generating README for project: {project_info.get('name', 'Unknown')}")
        
        # Analyze project structure
        structure = self._analyze_project_structure(project_path)
        
        prompt = f"""Generate a comprehensive README.md for the following project:

Project Information:
{project_info}

Project Structure:
{structure}

Include:
1. Project title and description
2. Features
3. Installation instructions
4. Usage examples
5. Configuration
6. API documentation (if applicable)
7. Development setup
8. Testing instructions
9. Contributing guidelines
10. License information

Generate in proper Markdown format."""
        
        readme_content = await self.agent.chat(prompt, db)
        
        # Save to database
        doc = Documentation(
            project_id=project_info.get('id'),
            doc_type="readme",
            title=f"README - {project_info.get('name')}",
            content=readme_content,
            format="markdown",
            file_path=output_path,
            created_at=datetime.utcnow()
        )
        db.add(doc)
        await db.commit()
        
        # Save to file if path provided
        if output_path:
            Path(output_path).write_text(readme_content)
            logger.info(f"README saved to {output_path}")
        
        return readme_content
    
    async def generate_api_docs(
        self,
        db: AsyncSession,
        code: str,
        language: str,
        project_id: Optional[int] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Generate API documentation"""
        logger.info("Generating API documentation")
        
        api_docs = await self.agent.generate_documentation(
            code=code,
            doc_type="api"
        )
        
        # Save to database
        doc = Documentation(
            project_id=project_id,
            doc_type="api",
            title="API Documentation",
            content=api_docs,
            format="markdown",
            file_path=output_path,
            created_at=datetime.utcnow()
        )
        db.add(doc)
        await db.commit()
        
        if output_path:
            Path(output_path).write_text(api_docs)
            logger.info(f"API docs saved to {output_path}")
        
        return api_docs
    
    async def generate_inline_docs(
        self,
        code: str,
        language: str
    ) -> str:
        """Add inline documentation to code"""
        prompt = f"""Add comprehensive inline documentation to the following {language} code.

Include:
1. Function/method docstrings
2. Class documentation
3. Parameter descriptions
4. Return value descriptions
5. Example usage
6. Important notes

Code:
```{language}
{code}
```

Return the code with documentation added."""
        
        documented_code = await self.agent.chat(prompt, None)
        return documented_code
    
    async def generate_architecture_docs(
        self,
        db: AsyncSession,
        project_path: str,
        project_id: Optional[int] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Generate architecture documentation"""
        logger.info("Generating architecture documentation")
        
        structure = self._analyze_project_structure(project_path)
        
        prompt = f"""Generate architecture documentation for a project with the following structure:

{structure}

Include:
1. System overview
2. Component architecture
3. Data flow diagrams (in text/ASCII)
4. Database schema
5. API design
6. Security considerations
7. Scalability notes
8. Technology stack

Generate in Markdown format."""
        
        arch_docs = await self.agent.chat(prompt, db)
        
        # Save to database
        doc = Documentation(
            project_id=project_id,
            doc_type="architecture",
            title="Architecture Documentation",
            content=arch_docs,
            format="markdown",
            file_path=output_path,
            created_at=datetime.utcnow()
        )
        db.add(doc)
        await db.commit()
        
        if output_path:
            Path(output_path).write_text(arch_docs)
            logger.info(f"Architecture docs saved to {output_path}")
        
        return arch_docs
    
    async def generate_mkdocs_site(
        self,
        db: AsyncSession,
        project_path: str,
        project_info: Dict,
        docs_dir: Optional[str] = None
    ) -> bool:
        """Generate a complete MkDocs documentation site"""
        logger.info("Generating MkDocs site")
        
        docs_dir = docs_dir or os.path.join(project_path, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        # Generate various documentation pages
        await self.generate_readme(
            db,
            project_path,
            project_info,
            os.path.join(docs_dir, "index.md")
        )
        
        await self.generate_architecture_docs(
            db,
            project_path,
            project_info.get('id'),
            os.path.join(docs_dir, "architecture.md")
        )
        
        # Create mkdocs.yml
        mkdocs_config = f"""site_name: {project_info.get('name', 'Project')} Documentation
site_description: {project_info.get('description', 'Project documentation')}
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest

nav:
  - Home: index.md
  - Architecture: architecture.md
  - API Reference: api.md

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - admonition
  - codehilite
  - toc:
      permalink: true
"""
        
        mkdocs_path = os.path.join(project_path, "mkdocs.yml")
        Path(mkdocs_path).write_text(mkdocs_config)
        
        logger.info(f"MkDocs site generated at {docs_dir}")
        return True
    
    def _analyze_project_structure(self, project_path: str) -> str:
        """Analyze project directory structure"""
        structure = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip common directories
                dirs[:] = [d for d in dirs if d not in [
                    '.git', '__pycache__', 'node_modules', 'venv', '.venv',
                    'dist', 'build', '.pytest_cache'
                ]]
                
                level = root.replace(project_path, '').count(os.sep)
                indent = ' ' * 2 * level
                structure.append(f"{indent}{os.path.basename(root)}/")
                
                subindent = ' ' * 2 * (level + 1)
                for file in files[:10]:  # Limit files shown
                    structure.append(f"{subindent}{file}")
                
                if len(files) > 10:
                    structure.append(f"{subindent}... ({len(files) - 10} more files)")
        
        except Exception as e:
            logger.error(f"Error analyzing structure: {str(e)}")
            return "Unable to analyze project structure"
        
        return '\n'.join(structure[:50])  # Limit total lines
    
    async def generate_changelog(
        self,
        db: AsyncSession,
        project_id: int,
        version: str,
        changes: List[str],
        output_path: Optional[str] = None
    ) -> str:
        """Generate or update CHANGELOG.md"""
        changelog_entry = f"""## [{version}] - {datetime.utcnow().strftime('%Y-%m-%d')}

### Changes
{chr(10).join(f'- {change}' for change in changes)}

"""
        
        # Save to database
        doc = Documentation(
            project_id=project_id,
            doc_type="changelog",
            title=f"Changelog - {version}",
            content=changelog_entry,
            format="markdown",
            file_path=output_path,
            created_at=datetime.utcnow()
        )
        db.add(doc)
        await db.commit()
        
        if output_path:
            # Append to existing changelog or create new
            if os.path.exists(output_path):
                existing = Path(output_path).read_text()
                Path(output_path).write_text(changelog_entry + existing)
            else:
                Path(output_path).write_text(f"# Changelog\n\n{changelog_entry}")
            
            logger.info(f"Changelog updated at {output_path}")
        
        return changelog_entry






