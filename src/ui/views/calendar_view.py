"""
Calendar view for displaying job applications by date.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QTextCharFormat, QColor
from datetime import datetime
from src.ui import theme

JOB_DATE_BG = QColor("#FDE68A")   # Soft amber - a date with an application
JOB_DATE_FG = QColor("#78350F")   # Dark amber text for contrast
TODAY_COLOR = QColor(theme.ACCENT)


class CalendarView(QWidget):
    """Display job applications in calendar format."""

    date_selected = pyqtSignal(QDate)
    application_selected = pyqtSignal(int)  # Signal when an application is selected
    deselect_requested = pyqtSignal()  # Signal to deselect current application

    def __init__(self, db_manager, user_id=None):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = user_id
        self.marked_dates = {}  # Track marked dates for highlighting
        self.init_ui()

    def init_ui(self):
        """Initialize calendar view UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.on_date_selected)

        # Today will be highlighted with underline and bold - no background to avoid conflicts

        layout.addWidget(self.calendar)

        # Date info
        self.date_info_label = QLabel("Select a date to view applications")
        self.date_info_label.setProperty("subheading", True)
        layout.addWidget(self.date_info_label)

        # List widget for applications on selected date
        self.applications_list = QListWidget()
        self.applications_list.itemClicked.connect(self.on_application_clicked)
        self.applications_list.itemDoubleClicked.connect(self.on_application_clicked)
        layout.addWidget(self.applications_list)

        # Deselect button
        button_layout = QHBoxLayout()
        self.deselect_btn = QPushButton("Deselect Job")
        self.deselect_btn.clicked.connect(self.deselect_requested.emit)
        button_layout.addStretch()
        button_layout.addWidget(self.deselect_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.refresh_highlighting()
    
    def refresh_highlighting(self):
        """Refresh highlights without clearing list (internal use only)."""
        try:
            applications = self.db_manager.get_all_applications(user_id=self.user_id)
            today_date = QDate.currentDate()
            self.marked_dates = {}  # Reset marked dates
            
            # Create format for job dates - soft amber background
            job_format = QTextCharFormat()
            job_format.setBackground(JOB_DATE_BG)
            job_format.setForeground(JOB_DATE_FG)

            # Create format for today - bold and underlined in the accent color
            today_format = QTextCharFormat()
            today_format.setFontWeight(900)  # Extra bold
            today_format.setUnderlineStyle(1)  # Underline
            today_format.setUnderlineColor(TODAY_COLOR)
            today_format.setForeground(TODAY_COLOR)
            
            # Collect all job dates
            for app in applications:
                if app.date_applied:
                    try:
                        qdate = QDate(app.date_applied.year, app.date_applied.month, app.date_applied.day)
                        if qdate.isValid():
                            date_key = qdate.toString("yyyy-MM-dd")
                            if date_key not in self.marked_dates:
                                self.marked_dates[date_key] = []
                            self.marked_dates[date_key].append(app)
                    except Exception as e:
                        print(f"Error processing app date: {e}")
                        continue
            
            # Apply highlighting: job dates in yellow
            for date_key in self.marked_dates:
                try:
                    parts = date_key.split('-')
                    if len(parts) == 3:
                        qdate = QDate(int(parts[0]), int(parts[1]), int(parts[2]))
                        if qdate.isValid():
                            # If it's today, combine today and job formatting
                            if qdate == today_date:
                                combined_format = QTextCharFormat()
                                combined_format.setBackground(JOB_DATE_BG)
                                combined_format.setForeground(JOB_DATE_FG)
                                combined_format.setFontWeight(900)  # Bold from today format
                                combined_format.setUnderlineStyle(1)  # Underline from today format
                                combined_format.setUnderlineColor(TODAY_COLOR)
                                self.calendar.setDateTextFormat(qdate, combined_format)
                            else:
                                self.calendar.setDateTextFormat(qdate, job_format)
                except Exception as e:
                    print(f"Error applying highlight: {e}")
            
            # Set today's format if today doesn't have a job
            if today_date.toString("yyyy-MM-dd") not in self.marked_dates:
                self.calendar.setDateTextFormat(today_date, today_format)
        except Exception as e:
            print(f"Error refreshing highlighting: {e}")
    
    def on_date_selected(self, qdate):
        """Handle date selection."""
        try:
            date_key = qdate.toString("yyyy-MM-dd")
            self.applications_list.clear()
            
            if date_key in self.marked_dates:
                apps = self.marked_dates[date_key]
                self.date_info_label.setText(f"Applications on {date_key}: ({len(apps)} found)")
                
                for app in apps:
                    item_text = f"{app.company_name} - {app.job_title} ({app.status.value})"
                    item = QListWidgetItem(item_text)
                    item.app_id = app.id
                    self.applications_list.addItem(item)
            else:
                self.date_info_label.setText(f"No applications on {date_key}")
            
            self.date_selected.emit(qdate)
        except Exception as e:
            print(f"Error in on_date_selected: {e}")
    
    def on_application_clicked(self, item):
        """Handle application selection from list."""
        try:
            if hasattr(item, 'app_id'):
                self.application_selected.emit(item.app_id)
        except Exception as e:
            print(f"Error in on_application_clicked: {e}")
    
    def refresh(self):
        """Refresh calendar with updated applications."""
        try:
            # Clear formatting only for dates we actually marked last time
            # (previously this brute-forced every day of the current year,
            # which missed highlights left over on dates in other years).
            clear_format = QTextCharFormat()
            for date_key in self.marked_dates:
                try:
                    parts = date_key.split('-')
                    if len(parts) == 3:
                        qdate = QDate(int(parts[0]), int(parts[1]), int(parts[2]))
                        if qdate.isValid():
                            self.calendar.setDateTextFormat(qdate, clear_format)
                except Exception as e:
                    print(f"Error clearing highlight: {e}")
            # Also clear today's format in case it had no job application
            self.calendar.setDateTextFormat(QDate.currentDate(), clear_format)

            # Refresh highlighting
            self.refresh_highlighting()
            
            # Preserve current selection if it exists
            current_item = self.applications_list.currentItem()
            if current_item and hasattr(current_item, 'app_id'):
                self.applications_list.clear()
                self.date_info_label.setText("Select a date to view applications")
            else:
                self.applications_list.clear()
                self.date_info_label.setText("Select a date to view applications")
        except Exception as e:
            print(f"Error in refresh: {e}")

