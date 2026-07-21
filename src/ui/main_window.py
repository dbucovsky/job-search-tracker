"""
Main window for the Job Search Tracker application.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QTabWidget, QSplitter,
                             QScrollArea, QToolBar, QStyle, QAction)
from PyQt5.QtCore import Qt, pyqtSignal
from src.ui.views.table_view import TableView
from src.ui.views.calendar_view import CalendarView
from src.ui.views.kanban_view import KanbanView
from src.ui.views.job_detail_view import JobDetailView
from src.ui.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main application window."""

    logout_requested = pyqtSignal()  # Signal when the user logs out (return to login screen)

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
        self.setGeometry(80, 80, 1300, 820)
        self.setMinimumSize(1000, 650)

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

        # Toolbar with quick actions (uses built-in Qt icons - no extra
        # icon assets required)
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        style = self.style()

        new_action = QAction(style.standardIcon(QStyle.SP_FileIcon), "New Application", self)
        new_action.triggered.connect(self.on_new_record_requested)
        toolbar.addAction(new_action)

        refresh_action = QAction(style.standardIcon(QStyle.SP_BrowserReload), "Refresh", self)
        refresh_action.triggered.connect(self.refresh_all_views)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        logout_toolbar_action = QAction(style.standardIcon(QStyle.SP_DialogCloseButton), "Logout", self)
        logout_toolbar_action.triggered.connect(self.on_logout)
        toolbar.addAction(logout_toolbar_action)

        # Central widget: a splitter with the view tabs on the left and a
        # persistent job detail panel on the right - editing a job no
        # longer pops up a dialog that interrupts the current view.
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)

        # View tabs
        tab_widget = QTabWidget()

        # Table View
        self.table_view = TableView(self.db_manager, self.user_id)
        self.table_view.application_selected.connect(self.on_application_selected)
        self.table_view.deselect_requested.connect(self.on_deselect_requested)
        self.table_view.application_updated.connect(self.refresh_all_views)
        tab_widget.addTab(self.table_view, "Table View")

        # Calendar View
        self.calendar_view = CalendarView(self.db_manager, self.user_id)
        self.calendar_view.application_selected.connect(self.on_application_selected)
        self.calendar_view.deselect_requested.connect(self.on_deselect_requested)
        tab_widget.addTab(self.calendar_view, "Calendar View")

        # Kanban View
        self.kanban_view = KanbanView(self.db_manager, self.user_id)
        self.kanban_view.application_selected.connect(self.on_application_selected)
        self.kanban_view.application_updated.connect(self.refresh_all_views)
        tab_widget.addTab(self.kanban_view, "Kanban Board")

        splitter.addWidget(tab_widget)

        # Job Detail panel (persistent, scrollable side panel)
        self.job_detail_view = JobDetailView(self.db_manager, self.user_id)
        self.job_detail_view.application_updated.connect(self.on_detail_updated)

        detail_scroll = QScrollArea()
        detail_scroll.setWidgetResizable(True)
        detail_scroll.setWidget(self.job_detail_view)
        detail_scroll.setMinimumWidth(320)
        detail_scroll.setMaximumWidth(460)
        splitter.addWidget(detail_scroll)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([850, 380])

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_application_selected(self, app_id):
        """Handle application selection from any view - load it into the
        persistent detail panel (no popup)."""
        self.current_app_id = app_id
        self.job_detail_view.load_application(app_id)

    def on_deselect_requested(self):
        """Handle deselect request."""
        self.current_app_id = None
        self.job_detail_view.clear_form()

    def on_new_record_requested(self):
        """Handle new record request from any view."""
        self.current_app_id = None  # Clear current selection to create new record
        self.job_detail_view.clear_form()  # Clear panel for new entry
        self.job_detail_view.focus_first_field()

    def on_detail_updated(self):
        """Handle updates from detail panel."""
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
        """Handle logout - close this window and return to the login screen."""
        self.logout_requested.emit()
        self.close()
