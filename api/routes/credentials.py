"""Credentials API routes"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_personalization_db
from core.credential_manager import CredentialManager

router = APIRouter()


class CredentialCreate(BaseModel):
    credential_type: str
    identifier: str
    value: str
    description: Optional[str] = None


class CredentialResponse(BaseModel):
    id: int
    type: str
    identifier: str
    description: Optional[str]
    last_used: Optional[str]


@router.post("/")
async def store_credential(
    credential: CredentialCreate,
    db: AsyncSession = Depends(get_personalization_db)
):
    """Store a new credential"""
    stored = await CredentialManager.store_credential(
        db=db,
        credential_type=credential.credential_type,
        identifier=credential.identifier,
        value=credential.value,
        description=credential.description
    )
    
    return {
        "message": "Credential stored successfully",
        "id": stored.id
    }


@router.get("/", response_model=List[dict])
async def list_credentials(
    credential_type: Optional[str] = None,
    db: AsyncSession = Depends(get_personalization_db)
):
    """List all credentials (without values)"""
    credentials = await CredentialManager.list_credentials(
        db=db,
        credential_type=credential_type
    )
    return credentials


@router.delete("/{credential_type}/{identifier}")
async def delete_credential(
    credential_type: str,
    identifier: str,
    db: AsyncSession = Depends(get_personalization_db)
):
    """Delete a credential"""
    success = await CredentialManager.delete_credential(
        db=db,
        credential_type=credential_type,
        identifier=identifier
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    return {"message": "Credential deleted successfully"}


@router.post("/sudo-password")
async def store_sudo_password(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_personalization_db)
):
    """Store sudo password"""
    await CredentialManager.store_sudo_password(
        db=db,
        username=username,
        password=password
    )
    
    return {"message": "Sudo password stored successfully"}






