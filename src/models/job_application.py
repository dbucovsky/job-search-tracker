"""
Job Application model for tracking job applications.
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ApplicationStatus(Enum):
    """Enum for application status."""
    IDENTIFIED = "Identified"
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"


class JobApplication(Base):
    """Model for job applications."""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Associate application with user
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    job_url = Column(String(500), nullable=True)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.IDENTIFIED, nullable=False)
    date_applied = Column(DateTime, nullable=True)
    date_created = Column(DateTime, default=datetime.now, nullable=False)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    salary_range = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    is_archived = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<JobApplication(id={self.id}, company={self.company_name}, title={self.job_title}, status={self.status.value})>"
    
    @staticmethod
    def get_status_color(status):
        """Get color for status."""
        color_map = {
            ApplicationStatus.IDENTIFIED: "#FFEB3B",  # Yellow
            ApplicationStatus.APPLIED: "#4CAF50",     # Green
            ApplicationStatus.INTERVIEWING: "#FF9800", # Orange
            ApplicationStatus.OFFER: "#4CAF50",       # Green
            ApplicationStatus.REJECTED: "#F44336",    # Red
        }
        return color_map.get(status, "#FFFFFF")
