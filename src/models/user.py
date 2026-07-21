"""
User model for authentication and user management.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
import hashlib
import os
from src.models.job_application import Base

PBKDF2_ITERATIONS = 200_000


class User(Base):
    """Model for users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    date_created = Column(DateTime, default=datetime.now, nullable=False)

    @staticmethod
    def hash_password(password, salt=None):
        """Hash a password with a random per-user salt using PBKDF2-HMAC-SHA256.

        Stored as "salt_hex$derived_hex" so verify_password can recover the salt.
        """
        if salt is None:
            salt = os.urandom(16).hex()
        derived = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS)
        return f"{salt}${derived.hex()}"

    def verify_password(self, password):
        """Verify a password against the stored hash.

        Accounts created before salted hashing was added stored a plain
        unsalted SHA-256 hex digest (no "$"). Those still verify here, and
        are transparently upgraded to the salted format in-place so the
        caller just needs to commit the session afterwards.
        """
        stored = self.password_hash
        if '$' in stored:
            salt, _ = stored.split('$', 1)
            return stored == User.hash_password(password, salt)

        # Legacy unsalted SHA-256 hash
        if stored == hashlib.sha256(password.encode()).hexdigest():
            self.password_hash = User.hash_password(password)
            return True
        return False
