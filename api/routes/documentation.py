"""Documentation API routes"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.ai_agent import AIAgent
from core.documentation_generator import DocumentationGenerator

router = APIRouter()


class GenerateReadmeRequest(BaseModel):
    project_path: str
    project_info: dict
    output_path: Optional[str] = None


class GenerateApiDocsRequest(BaseModel):
    code: str
    language: str
    project_id: Optional[int] = None
    output_path: Optional[str] = None


@router.post("/readme")
async def generate_readme(
    request: GenerateReadmeRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate README.md"""
    agent = AIAgent(session_id="documentation")
    doc_generator = DocumentationGenerator(agent)
    
    readme = await doc_generator.generate_readme(
        db=db,
        project_path=request.project_path,
        project_info=request.project_info,
        output_path=request.output_path
    )
    
    return {"readme": readme}


@router.post("/api-docs")
async def generate_api_docs(
    request: GenerateApiDocsRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate API documentation"""
    agent = AIAgent(session_id="documentation")
    doc_generator = DocumentationGenerator(agent)
    
    docs = await doc_generator.generate_api_docs(
        db=db,
        code=request.code,
        language=request.language,
        project_id=request.project_id,
        output_path=request.output_path
    )
    
    return {"documentation": docs}


@router.post("/inline-docs")
async def generate_inline_docs(
    code: str,
    language: str
):
    """Add inline documentation to code"""
    agent = AIAgent(session_id="documentation")
    doc_generator = DocumentationGenerator(agent)
    
    documented_code = await doc_generator.generate_inline_docs(
        code=code,
        language=language
    )
    
    return {"documented_code": documented_code}






