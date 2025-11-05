"""
Security utilities for encryption and credential management
"""
import base64
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import settings


class SecurityManager:
    """Handles encryption and decryption of sensitive data"""
    
    def __init__(self):
        self.cipher = self._init_cipher()
    
    def _init_cipher(self) -> Fernet:
        """Initialize Fernet cipher with encryption key"""
        # Derive a proper key from the encryption key in settings
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'ai_agent_salt_v1',  # In production, use a random salt stored securely
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(settings.encryption_key.encode())
        )
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not data:
            return ""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return ""
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    def hash_password(self, password: str) -> str:
        """Hash a password (one-way)"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)


# Global security manager instance
security_manager = SecurityManager()


# Convenience functions
def encrypt_data(data: str) -> str:
    """Encrypt data using the global security manager"""
    return security_manager.encrypt(data)


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data using the global security manager"""
    return security_manager.decrypt(encrypted_data)


def hash_password(password: str) -> str:
    """Hash a password using the global security manager"""
    return security_manager.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password using the global security manager"""
    return security_manager.verify_password(plain_password, hashed_password)


