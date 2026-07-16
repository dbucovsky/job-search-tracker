"""
Database manager for job tracking application.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.job_application import Base, JobApplication
from src.models.user import User


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path="data/job_tracker.db"):
        """Initialize database manager with SQLite database."""
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        self.db_url = f"sqlite:///{os.path.abspath(db_path)}"
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.init_db()
    
    def init_db(self):
        """Initialize database schema."""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    def add_application(self, company_name, job_title, job_url=None, status=None, 
                       salary_range=None, location=None, contact_name=None, 
                       contact_email=None, contact_phone=None, notes=None, user_id=None):
        """Add a new job application."""
        session = self.get_session()
        try:
            from src.models.job_application import ApplicationStatus
            app = JobApplication(
                company_name=company_name,
                job_title=job_title,
                job_url=job_url,
                status=status or ApplicationStatus.IDENTIFIED,
                salary_range=salary_range,
                location=location,
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                notes=notes,
                user_id=user_id
            )
            session.add(app)
            session.commit()
            return app
        finally:
            session.close()
    
    def get_all_applications(self, user_id=None):
        """Get all job applications (including archived)."""
        session = self.get_session()
        try:
            query = session.query(JobApplication)
            if user_id is not None:
                query = query.filter(JobApplication.user_id == user_id)
            return query.all()
        finally:
            session.close()
    
    def get_active_applications(self, user_id=None):
        """Get only active (non-archived) job applications."""
        session = self.get_session()
        try:
            query = session.query(JobApplication).filter(JobApplication.is_archived == False)
            if user_id is not None:
                query = query.filter(JobApplication.user_id == user_id)
            return query.all()
        finally:
            session.close()
    
    def get_application_by_id(self, app_id):
        """Get a specific job application by ID."""
        session = self.get_session()
        try:
            return session.query(JobApplication).filter(JobApplication.id == app_id).first()
        finally:
            session.close()
    
    def update_application(self, app_id, **kwargs):
        """Update a job application."""
        session = self.get_session()
        try:
            app = session.query(JobApplication).filter(JobApplication.id == app_id).first()
            if app:
                for key, value in kwargs.items():
                    if hasattr(app, key):
                        setattr(app, key, value)
                session.commit()
            return app
        finally:
            session.close()
    
    def delete_application(self, app_id):
        """Delete a job application."""
        session = self.get_session()
        try:
            app = session.query(JobApplication).filter(JobApplication.id == app_id).first()
            if app:
                session.delete(app)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_applications_by_status(self, status, archived=False, user_id=None):
        """Get applications filtered by status and archive status."""
        session = self.get_session()
        try:
            query = session.query(JobApplication).filter(
                JobApplication.status == status,
                JobApplication.is_archived == archived
            )
            if user_id is not None:
                query = query.filter(JobApplication.user_id == user_id)
            return query.all()
        finally:
            session.close()
    
    # User authentication methods
    def create_user(self, username, password):
        """Create a new user account."""
        session = self.get_session()
        try:
            user = User(
                username=username,
                password_hash=User.hash_password(password)
            )
            session.add(user)
            session.commit()
            # Access attributes before closing session
            user_id = user.id
            user_username = user.username
            session.expunge(user)
            return {'id': user_id, 'username': user_username}
        finally:
            session.close()
    
    def get_user_by_username(self, username):
        """Get user by username."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            if user:
                # Access attributes before closing session
                user_id = user.id
                user_username = user.username
                return {'id': user_id, 'username': user_username}
            return None
        finally:
            session.close()
    
    def get_user_by_id(self, user_id):
        """Get user by ID."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                # Access attributes before closing session
                uid = user.id
                uname = user.username
                return {'id': uid, 'username': uname}
            return None
        finally:
            session.close()
