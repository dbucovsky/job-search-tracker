"""
User model for authentication and user management.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import hashlib

Base = declarative_base()


class User(Base):
    """Model for users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return self.password_hash == User.hash_password(password)
