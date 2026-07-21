"""
Job detail panel for viewing and editing a single job application.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                             QTextEdit, QComboBox, QPushButton, QDateEdit, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from src.models.job_application import ApplicationStatus


def _section_label(text):
    """A small bold section heading used to break up the form."""
    label = QLabel(text)
    label.setProperty("section", True)
    return label


class JobDetailView(QWidget):
    """Display and edit details of a single job application.

    This is a persistent side panel (not a modal dialog) - it stays visible
    at all times and updates in place as the user selects different
    applications, rather than popping up and interrupting whatever view
    they're working in.
    """

    application_updated = pyqtSignal()

    def __init__(self, db_manager, user_id=None):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = user_id
        self.current_app_id = None
        self.setObjectName("detailPanel")
        self.init_ui()

    def init_ui(self):
        """Initialize job detail panel UI."""
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(16, 16, 16, 16)
        outer_layout.setSpacing(4)

        # Header - reflects whether we're creating new or editing an
        # existing application.
        self.header_label = QLabel("New Application")
        self.header_label.setProperty("heading", True)
        outer_layout.addWidget(self.header_label)

        self.subheader_label = QLabel("Fill in the details below and click Save.")
        self.subheader_label.setProperty("subheading", True)
        self.subheader_label.setWordWrap(True)
        outer_layout.addWidget(self.subheader_label)

        outer_layout.addSpacing(8)

        # Position section
        outer_layout.addWidget(_section_label("POSITION"))
        position_form = QFormLayout()
        position_form.setSpacing(8)

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("e.g. Google")
        position_form.addRow("Company:", self.company_input)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g. Software Engineer")
        position_form.addRow("Job Title:", self.title_input)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://company.com/careers/123")
        position_form.addRow("Job URL:", self.url_input)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("City, State or Remote")
        position_form.addRow("Location:", self.location_input)

        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("e.g. $90,000 - $110,000")
        position_form.addRow("Salary Range:", self.salary_input)

        outer_layout.addLayout(position_form)

        # Status & dates section
        outer_layout.addWidget(_section_label("STATUS & DATES"))
        status_form = QFormLayout()
        status_form.setSpacing(8)

        self.status_combo = QComboBox()
        for status in ApplicationStatus:
            self.status_combo.addItem(status.value, status)
        status_form.addRow("Status:", self.status_combo)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        status_form.addRow("Date Applied:", self.date_input)

        outer_layout.addLayout(status_form)

        # Contact section
        outer_layout.addWidget(_section_label("CONTACT"))
        contact_form = QFormLayout()
        contact_form.setSpacing(8)

        self.contact_name_input = QLineEdit()
        self.contact_name_input.setPlaceholderText("e.g. Jane Smith")
        contact_form.addRow("Name:", self.contact_name_input)

        self.contact_email_input = QLineEdit()
        self.contact_email_input.setPlaceholderText("e.g. jane@company.com")
        contact_form.addRow("Email:", self.contact_email_input)

        self.contact_phone_input = QLineEdit()
        self.contact_phone_input.setPlaceholderText("e.g. (555) 123-4567")
        contact_form.addRow("Phone:", self.contact_phone_input)

        outer_layout.addLayout(contact_form)

        # Notes section
        outer_layout.addWidget(_section_label("NOTES"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Anything worth remembering about this application...")
        self.notes_input.setMaximumHeight(90)
        outer_layout.addWidget(self.notes_input)

        # Archive checkbox
        self.archive_checkbox = QCheckBox("Archived (hide from active views)")
        outer_layout.addWidget(self.archive_checkbox)

        outer_layout.addSpacing(8)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save")
        self.save_btn.setProperty("variant", "primary")
        self.save_btn.clicked.connect(self.save_application)
        button_layout.addWidget(self.save_btn)

        self.new_btn = QPushButton("New")
        self.new_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.new_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setProperty("variant", "danger")
        self.delete_btn.clicked.connect(self.delete_application)
        button_layout.addWidget(self.delete_btn)

        outer_layout.addLayout(button_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)
        self.clear_form()

    def focus_first_field(self):
        """Move keyboard focus to the first field - used when starting a new entry."""
        self.company_input.setFocus()

    def load_application(self, app_id):
        """Load an application for editing."""
        self.current_app_id = app_id
        app = self.db_manager.get_application_by_id(app_id)

        if app:
            self.header_label.setText(app.company_name or "Untitled Application")
            self.subheader_label.setText(f"{app.job_title or 'No title'} - {app.status.value}")

            self.company_input.setText(app.company_name)
            self.title_input.setText(app.job_title)
            self.url_input.setText(app.job_url or "")
            self.status_combo.setCurrentText(app.status.value)

            if app.date_applied:
                qdate = QDate(app.date_applied.year, app.date_applied.month, app.date_applied.day)
                self.date_input.setDate(qdate)
            else:
                self.date_input.setDate(QDate.currentDate())

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
            new_app_id = self.db_manager.add_application(
                company_name=self.company_input.text(),
                job_title=self.title_input.text(),
                job_url=self.url_input.text(),
                status=status,
                date_applied=self.date_input.date().toPyDate(),
                salary_range=self.salary_input.text(),
                location=self.location_input.text(),
                contact_name=self.contact_name_input.text(),
                contact_email=self.contact_email_input.text(),
                contact_phone=self.contact_phone_input.text(),
                notes=self.notes_input.toPlainText(),
                user_id=self.user_id
            )
            self.current_app_id = new_app_id

        self.application_updated.emit()
        # Reload the application to keep the panel showing the saved data
        self.load_application(self.current_app_id)

    def delete_application(self):
        """Delete the current application."""
        if self.current_app_id:
            confirm = QMessageBox.question(
                self, "Delete Application",
                "Are you sure you want to delete this application? This cannot be undone.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if confirm != QMessageBox.Yes:
                return

            self.db_manager.delete_application(self.current_app_id)
            self.application_updated.emit()
            # The record is gone - clear the panel instead of reloading it
            self.clear_form()

    def clear_form(self):
        """Clear the form for a new entry."""
        self.current_app_id = None
        self.header_label.setText("New Application")
        self.subheader_label.setText("Fill in the details below and click Save.")
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
