"""
Job detail view for viewing and editing a single job application.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QPushButton, QDateEdit, QCheckBox)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from src.models.job_application import ApplicationStatus


class JobDetailView(QDialog):
    """Display and edit details of a single job application."""
    
    application_updated = pyqtSignal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.current_app_id = None
        self.setWindowTitle("Job Details")
        self.setGeometry(100, 100, 500, 700)
        self.init_ui()
    
    def init_ui(self):
        """Initialize job detail view UI."""
        layout = QVBoxLayout()
        
        # Company Name
        layout.addWidget(QLabel("Company Name:"))
        self.company_input = QLineEdit()
        layout.addWidget(self.company_input)
        
        # Job Title
        layout.addWidget(QLabel("Job Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        
        # Job URL
        layout.addWidget(QLabel("Job URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)
        
        # Status
        layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        for status in ApplicationStatus:
            self.status_combo.addItem(status.value, status)
        layout.addWidget(self.status_combo)
        
        # Date Applied
        layout.addWidget(QLabel("Date Applied:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)
        
        # Location
        layout.addWidget(QLabel("Location:"))
        self.location_input = QLineEdit()
        layout.addWidget(self.location_input)
        
        # Salary Range
        layout.addWidget(QLabel("Salary Range:"))
        self.salary_input = QLineEdit()
        layout.addWidget(self.salary_input)
        
        # Contact Name
        layout.addWidget(QLabel("Contact Name:"))
        self.contact_name_input = QLineEdit()
        layout.addWidget(self.contact_name_input)
        
        # Contact Email
        layout.addWidget(QLabel("Contact Email:"))
        self.contact_email_input = QLineEdit()
        layout.addWidget(self.contact_email_input)
        
        # Contact Phone
        layout.addWidget(QLabel("Contact Phone:"))
        self.contact_phone_input = QLineEdit()
        layout.addWidget(self.contact_phone_input)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)
        
        # Archive checkbox
        layout.addWidget(QLabel("Archive:"))
        self.archive_checkbox = QCheckBox("Mark as archived")
        layout.addWidget(self.archive_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_application)
        button_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_application)
        button_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close_dialog)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.clear_form()
    
    def close_dialog(self):
        """Close the dialog and clear the form."""
        self.clear_form()
        self.close()
    
    def load_application(self, app_id):
        """Load an application for editing."""
        self.current_app_id = app_id
        app = self.db_manager.get_application_by_id(app_id)
        
        if app:
            self.company_input.setText(app.company_name)
            self.title_input.setText(app.job_title)
            self.url_input.setText(app.job_url or "")
            self.status_combo.setCurrentText(app.status.value)
            
            if app.date_applied:
                qdate = QDate(app.date_applied.year, app.date_applied.month, app.date_applied.day)
                self.date_input.setDate(qdate)
            
            self.location_input.setText(app.location or "")
            self.salary_input.setText(app.salary_range or "")
            self.contact_name_input.setText(app.contact_name or "")
            self.contact_email_input.setText(app.contact_email or "")
            self.contact_phone_input.setText(app.contact_phone or "")
            self.notes_input.setText(app.notes or "")
            self.archive_checkbox.setChecked(app.is_archived)
    
    def save_application(self):
        """Save application details."""
        if self.current_app_id:
            # Update existing
            status = self.status_combo.currentData()
            self.db_manager.update_application(
                self.current_app_id,
                company_name=self.company_input.text(),
                job_title=self.title_input.text(),
                job_url=self.url_input.text(),
                status=status,
                date_applied=self.date_input.date().toPyDate(),
                location=self.location_input.text(),
                salary_range=self.salary_input.text(),
                contact_name=self.contact_name_input.text(),
                contact_email=self.contact_email_input.text(),
                contact_phone=self.contact_phone_input.text(),
                notes=self.notes_input.toPlainText(),
                is_archived=self.archive_checkbox.isChecked()
            )
        else:
            # Create new
            status = self.status_combo.currentData()
            self.db_manager.add_application(
                company_name=self.company_input.text(),
                job_title=self.title_input.text(),
                job_url=self.url_input.text(),
                status=status,
                salary_range=self.salary_input.text(),
                location=self.location_input.text(),
                contact_name=self.contact_name_input.text(),
                contact_email=self.contact_email_input.text(),
                contact_phone=self.contact_phone_input.text(),
                notes=self.notes_input.toPlainText()
            )
        
        self.application_updated.emit()
        self.clear_form()
    
    def delete_application(self):
        """Delete the current application."""
        if self.current_app_id:
            self.db_manager.delete_application(self.current_app_id)
            self.application_updated.emit()
            self.clear_form()
    
    def clear_form(self):
        """Clear the form."""
        self.current_app_id = None
        self.company_input.clear()
        self.title_input.clear()
        self.url_input.clear()
        self.status_combo.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.location_input.clear()
        self.salary_input.clear()
        self.contact_name_input.clear()
        self.contact_email_input.clear()
        self.contact_phone_input.clear()
        self.notes_input.clear()
        self.archive_checkbox.setChecked(False)
