"""
Credential manager for secure storage of sensitive data
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.security import encrypt_data, decrypt_data
from database.personalization_models import Credential


class CredentialManager:
    """Manages encrypted storage of credentials"""
    
    @staticmethod
    async def store_credential(
        db: AsyncSession,
        credential_type: str,
        identifier: str,
        value: str,
        description: Optional[str] = None
    ) -> Credential:
        """
        Store a credential securely
        
        Args:
            db: Database session
            credential_type: Type of credential (sudo_password, api_key, etc.)
            identifier: Identifier (username, service name, etc.)
            value: Credential value to encrypt
            description: Optional description
            
        Returns:
            Created credential record
        """
        logger.info(f"Storing credential: {credential_type} for {identifier}")
        
        # Encrypt the value
        encrypted_value = encrypt_data(value)
        
        # Check if credential already exists
        result = await db.execute(
            select(Credential).filter_by(
                credential_type=credential_type,
                identifier=identifier
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing credential
            existing.encrypted_value = encrypted_value
            existing.description = description
            existing.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing)
            logger.info(f"Updated existing credential for {identifier}")
            return existing
        else:
            # Create new credential
            credential = Credential(
                credential_type=credential_type,
                identifier=identifier,
                encrypted_value=encrypted_value,
                description=description
            )
            db.add(credential)
            await db.commit()
            await db.refresh(credential)
            logger.info(f"Created new credential for {identifier}")
            return credential
    
    @staticmethod
    async def get_credential(
        db: AsyncSession,
        credential_type: str,
        identifier: str
    ) -> Optional[str]:
        """
        Retrieve and decrypt a credential
        
        Args:
            db: Database session
            credential_type: Type of credential
            identifier: Identifier
            
        Returns:
            Decrypted credential value or None
        """
        result = await db.execute(
            select(Credential).filter_by(
                credential_type=credential_type,
                identifier=identifier
            )
        )
        credential = result.scalar_one_or_none()
        
        if credential:
            # Update last used timestamp
            credential.last_used = datetime.utcnow()
            await db.commit()
            
            # Decrypt and return value
            return decrypt_data(credential.encrypted_value)
        
        return None
    
    @staticmethod
    async def delete_credential(
        db: AsyncSession,
        credential_type: str,
        identifier: str
    ) -> bool:
        """
        Delete a credential
        
        Args:
            db: Database session
            credential_type: Type of credential
            identifier: Identifier
            
        Returns:
            True if deleted, False if not found
        """
        result = await db.execute(
            select(Credential).filter_by(
                credential_type=credential_type,
                identifier=identifier
            )
        )
        credential = result.scalar_one_or_none()
        
        if credential:
            await db.delete(credential)
            await db.commit()
            logger.info(f"Deleted credential: {credential_type} for {identifier}")
            return True
        
        return False
    
    @staticmethod
    async def list_credentials(
        db: AsyncSession,
        credential_type: Optional[str] = None
    ) -> list:
        """
        List all credentials (without values)
        
        Args:
            db: Database session
            credential_type: Optional filter by type
            
        Returns:
            List of credential records (without encrypted values)
        """
        if credential_type:
            result = await db.execute(
                select(Credential).filter_by(credential_type=credential_type)
            )
        else:
            result = await db.execute(select(Credential))
        
        credentials = result.scalars().all()
        
        # Return list without encrypted values
        return [
            {
                "id": cred.id,
                "credential_type": cred.credential_type,
                "identifier": cred.identifier,
                "description": cred.description,
                "last_used": cred.last_used,
                "created_at": cred.created_at
            }
            for cred in credentials
        ]

