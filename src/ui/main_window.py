"""
Main window for the Job Search Tracker application.
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTabWidget, QMenuBar, QMenu
from PyQt5.QtCore import Qt
from src.ui.views.table_view import TableView
from src.ui.views.calendar_view import CalendarView
from src.ui.views.kanban_view import KanbanView
from src.ui.views.job_detail_view import JobDetailView
from src.ui.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, db_manager, user_id=None, username=None):
        super().__init__()
        self.db_manager = db_manager
        self.current_app_id = None  # Track currently selected application
        self.user_id = user_id
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        """Initialize main window UI."""
        title = f"Job Search Tracker - {self.username}" if self.username else "Job Search Tracker"
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1000, 800)
        
        # Create menu bar
        menubar = self.menuBar()
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.on_about)
        
        # User menu
        user_menu = menubar.addMenu(f"User: {self.username}")
        logout_action = user_menu.addAction("Logout")
        logout_action.triggered.connect(self.on_logout)
        
        # Central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # View tabs
        tab_widget = QTabWidget()
        
        # Table View
        self.table_view = TableView(self.db_manager)
        self.table_view.application_selected.connect(self.on_application_selected)
        self.table_view.deselect_requested.connect(self.on_deselect_requested)
        self.table_view.application_updated.connect(self.refresh_all_views)
        self.table_view.new_record_requested.connect(self.on_new_record_requested)
        tab_widget.addTab(self.table_view, "Table View")
        
        # Calendar View
        self.calendar_view = CalendarView(self.db_manager)
        self.calendar_view.application_selected.connect(self.on_application_selected)
        self.calendar_view.deselect_requested.connect(self.on_deselect_requested)
        self.calendar_view.new_record_requested.connect(self.on_new_record_requested)
        tab_widget.addTab(self.calendar_view, "Calendar View")
        
        # Kanban View
        self.kanban_view = KanbanView(self.db_manager)
        self.kanban_view.application_selected.connect(self.on_application_selected)
        self.kanban_view.application_updated.connect(self.refresh_all_views)
        self.kanban_view.new_record_requested.connect(self.on_new_record_requested)
        tab_widget.addTab(self.kanban_view, "Kanban Board")
        
        main_layout.addWidget(tab_widget)
        
        # Create Job Detail Dialog
        self.job_detail_view = JobDetailView(self.db_manager)
        self.job_detail_view.application_updated.connect(self.on_detail_updated)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def on_application_selected(self, app_id):
        """Handle application selection from table view."""
        self.current_app_id = app_id  # Track current selection
        self.job_detail_view.load_application(app_id)
        self.job_detail_view.exec_()  # Show as modal dialog
    
    def on_deselect_requested(self):
        """Handle deselect request."""
        self.current_app_id = None  # Clear current selection
    
    def on_new_record_requested(self):
        """Handle new record request from any view."""
        self.current_app_id = None  # Clear current selection to create new record
        self.job_detail_view.clear_form()  # Clear form for new entry
        self.job_detail_view.exec_()  # Show as modal dialog
    
    def on_detail_updated(self):
        """Handle updates from detail dialog."""
        self.refresh_all_views()
    
    def refresh_all_views(self):
        """Refresh all views after data changes."""
        try:
            self.table_view.refresh_table()
        except Exception as e:
            print(f"Error refreshing table view: {e}")
        
        try:
            self.calendar_view.refresh()
        except Exception as e:
            print(f"Error refreshing calendar view: {e}")
        
        try:
            self.kanban_view.refresh()
        except Exception as e:
            print(f"Error refreshing kanban view: {e}")
    
    def on_about(self):
        """Handle About menu action."""
        about_dialog = AboutDialog(self)
        about_dialog.exec_()
    
    def on_logout(self):
        """Handle logout - close application."""
        import sys
        sys.exit(0)
