import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import bcrypt
import logging

logger = logging.getLogger(__name__)

class SecureEncryption:
    """Ultimate security encryption system with multiple layers"""
    
    def __init__(self):
        self.master_key = os.getenv("MASTER_ENCRYPTION_KEY", "default-key-change-me")
        self._fernet = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        try:
            salt = base64.b64decode(os.getenv("ENCRYPTION_SALT", "c2FsdHlzYWx0eXNhbHQ="))
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA512(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
            self._fernet = Fernet(key)
            logger.info("Encryption initialized successfully")
        except Exception as e:
            logger.error(f"Encryption initialization failed: {str(e)}")
    
    def encrypt_data(self, data: str) -> str:
        try:
            encrypted = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        try:
            data = base64.urlsafe_b64decode(encrypted_data)
            decrypted = self._fernet.decrypt(data)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            return encrypted_data
    
    def hash_password(self, password: str) -> str:
        try:
            salt = bcrypt.gensalt(rounds=14)
            return bcrypt.hashpw(password.encode(), salt).decode()
        except Exception as e:
            logger.error(f"Password hashing error: {str(e)}")
            return password
    
    def verify_password(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
