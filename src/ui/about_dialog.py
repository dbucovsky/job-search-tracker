"""
About dialog showing app information.
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from datetime import datetime


class AboutDialog(QDialog):
    """Display information about the Job Search Tracker application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Job Search Tracker")
        self.setGeometry(200, 200, 500, 500)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize About dialog UI."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Job Search Tracker")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Version and date info
        version_info = QLabel("Version: 0.7.5")
        layout.addWidget(version_info)

        last_updated = QLabel("Last Updated: 2026-07-21")
        layout.addWidget(last_updated)
        
        # Description
        description = QLabel("A Python desktop application for tracking job applications with multiple views and local SQLite database storage.")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Features section
        features_label = QLabel("Features:")
        features_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(features_label)
        
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setMaximumHeight(250)
        features_content = """• Table View: Sortable table with inline editing, archive filtering, and status dropdown
• Calendar View: Date-based application tracking with visual highlighting
• Kanban Board: Drag-and-drop status management organized by application stage
• Job Details: Comprehensive form for viewing and editing application information
• Database: Local SQLite storage with 15 data fields per application
• Archive: Mark applications as archived and filter visibility
• New Records: Create new applications from any view
• Multiple Status States: Identified, Applied, Interviewing, Offer, Rejected
• Git Integration: Automatic version tracking and GitHub synchronization"""
        features_text.setText(features_content)
        layout.addWidget(features_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
