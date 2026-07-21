"""
Kanban board view for job applications organized by status.
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QTimer
from PyQt5.QtGui import QDrag
from src.models.job_application import ApplicationStatus, JobApplication
from src.ui import theme


class KanbanCard(QFrame):
    """A draggable card in the Kanban board."""

    clicked = pyqtSignal(int)  # Signal when card is clicked

    # Card state machine
    STATE_IDLE = 0
    STATE_PRESSED = 1
    STATE_DRAGGING = 2

    def __init__(self, app_id, company_name, job_title, location=None, status_color=theme.BORDER_STRONG):
        super().__init__()
        self.app_id = app_id
        self.company_name = company_name
        self.job_title = job_title
        self.location = location
        self.state = self.STATE_IDLE
        self.press_pos = None
        self.block_clicks = False  # Aggressive flag: block ALL clicks when True
        self.click_blocker = QTimer()
        self.click_blocker.setSingleShot(True)
        self.click_blocker.timeout.connect(lambda: setattr(self, 'block_clicks', False))
        self.setObjectName("kanbanCard")
        # Base look comes from the app-wide "kanbanCard" style; the colored
        # left accent is per-instance since it's driven by application status.
        self.setStyleSheet(f"QFrame#kanbanCard {{ border-left: 4px solid {status_color}; }}")
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptDrops(False)
        self.init_ui()

    def init_ui(self):
        """Initialize card UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        company_label = QLabel(self.company_name)
        company_label.setStyleSheet(f"font-weight: 600; font-size: 11px; color: {theme.TEXT_PRIMARY}; border: none;")
        layout.addWidget(company_label)

        title_label = QLabel(self.job_title)
        title_label.setStyleSheet(f"font-size: 10px; color: {theme.TEXT_SECONDARY}; border: none;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        if self.location:
            location_label = QLabel(f"📍 {self.location}")
            location_label.setStyleSheet(f"font-size: 9px; color: {theme.TEXT_SECONDARY}; border: none;")
            layout.addWidget(location_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        """Handle mouse press - transition from IDLE to PRESSED."""
        if event.button() == Qt.LeftButton and self.state == self.STATE_IDLE:
            self.state = self.STATE_PRESSED
            self.press_pos = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move - transition from PRESSED to DRAGGING."""
        if not (event.buttons() & Qt.LeftButton):
            return

        # Only handle if we're in PRESSED state (haven't started drag yet)
        if self.state != self.STATE_PRESSED or self.press_pos is None:
            event.accept()
            return

        # Check if movement is large enough to be a drag
        movement = (event.pos() - self.press_pos).manhattanLength()
        if movement < 5:
            event.accept()
            return

        # DRAG DETECTED: Immediately block all clicks for 500ms
        self.block_clicks = True
        self.click_blocker.start(500)  # Aggressive 500ms block

        # Transition to DRAGGING state
        self.state = self.STATE_DRAGGING

        # Perform drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.app_id))
        mime_data.setData("application/x-app-id", str(self.app_id).encode())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)

        # After drag completes, reset state
        self.state = self.STATE_IDLE
        self.press_pos = None
        event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release - only emit click if block_clicks is False."""
        if event.button() == Qt.LeftButton:
            # NEVER emit click if block_clicks is set (during or after drag)
            if not self.block_clicks and self.state == self.STATE_PRESSED and self.press_pos is not None:
                # Verify position hasn't moved far
                movement = (event.pos() - self.press_pos).manhattanLength()
                if movement < 10:
                    self.clicked.emit(self.app_id)

            # Always reset to IDLE
            self.state = self.STATE_IDLE
            self.press_pos = None
        event.accept()

    def mouseDoubleClickEvent(self, event):
        """Handle double click - do nothing (use single-click instead)."""
        event.accept()


class KanbanColumn(QFrame):
    """A column in the Kanban board that accepts drops."""

    application_selected = pyqtSignal(int)  # Signal when an application card is clicked
    status_changed = pyqtSignal(int, object)  # Signal when card is dropped (app_id, new_status)

    def __init__(self, status, applications, db_manager):
        super().__init__()
        self.status = status
        self.applications = applications
        self.db_manager = db_manager
        self.status_color = JobApplication.get_status_color(status)
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        """Initialize column UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Column header: colored status dot + name + item-count pill
        header = QFrame()
        header.setObjectName("kanbanColumnHeader")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 8, 10, 8)

        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background-color: {self.status_color}; border-radius: 5px; border: none;")
        header_layout.addWidget(dot)

        title_label = QLabel(self.status.value)
        title_label.setStyleSheet(f"font-weight: 600; font-size: 11px; color: {theme.TEXT_PRIMARY}; border: none; margin-left: 4px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.count_label = QLabel(str(len(self.applications)))
        self.count_label.setStyleSheet(
            f"background-color: {theme.SURFACE_MUTED}; color: {theme.TEXT_SECONDARY}; "
            f"border: none; border-radius: 9px; padding: 1px 8px; font-size: 9px; font-weight: 600;"
        )
        header_layout.addWidget(self.count_label)

        header.setLayout(header_layout)
        layout.addWidget(header)

        # Application cards
        for app in self.applications:
            card = KanbanCard(app.id, app.company_name, app.job_title, app.location, self.status_color)
            card.clicked.connect(self.application_selected.emit)
            layout.addWidget(card)

        layout.addStretch()
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        """Handle drag enter."""
        if event.mimeData().hasFormat("application/x-app-id"):
            event.acceptProposedAction()
            self.setStyleSheet(
                f"QFrame {{ border: 2px solid {theme.ACCENT}; border-radius: 6px; background-color: {theme.ACCENT_SOFT}; }}"
            )

    def dragLeaveEvent(self, event):
        """Handle drag leave."""
        self.setStyleSheet("")

    def dropEvent(self, event):
        """Handle drop."""
        self.setStyleSheet("")  # Reset style

        if event.mimeData().hasFormat("application/x-app-id"):
            try:
                app_id = int(bytes(event.mimeData().data("application/x-app-id")).decode())
                # Update application status
                self.db_manager.update_application(app_id, status=self.status)
                self.status_changed.emit(app_id, self.status)
                event.acceptProposedAction()
            except Exception as e:
                print(f"Error dropping card: {e}")
                event.ignore()


class KanbanView(QWidget):
    """Kanban board view for job applications."""

    application_selected = pyqtSignal(int)  # Signal when an application is selected
    application_updated = pyqtSignal()  # Signal when application status changes

    def __init__(self, db_manager, user_id=None):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = user_id
        self.layout_widget = None
        self.columns = []  # Track column references
        self.init_ui()

    def init_ui(self):
        """Initialize Kanban view UI."""
        try:
            # Clear old layout if exists
            if self.layout_widget is not None:
                old_layout = self.layout_widget.layout()
                if old_layout is not None:
                    while old_layout.count():
                        item = old_layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()

            self.columns = []  # Reset columns list

            # Create main vertical layout
            main_layout = self.layout()
            if main_layout is None:
                main_layout = QVBoxLayout()
                main_layout.setContentsMargins(8, 8, 8, 8)
                self.setLayout(main_layout)
            else:
                while main_layout.count():
                    item = main_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

            # Create scroll area for columns
            self.layout_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            # Create columns for each status
            for status in ApplicationStatus:
                try:
                    # Get active applications for this status (not archived)
                    applications = self.db_manager.get_applications_by_status(status, archived=False, user_id=self.user_id)

                    # Create scroll area for column
                    scroll = QScrollArea()
                    scroll.setWidgetResizable(True)
                    scroll.setStyleSheet(
                        f"QScrollArea {{ border: 1px solid {theme.BORDER}; border-radius: 6px; background-color: {theme.SURFACE_MUTED}; }}"
                    )

                    # Create column
                    column = KanbanColumn(status, applications, self.db_manager)
                    column.application_selected.connect(self.application_selected.emit)
                    column.status_changed.connect(self.on_status_changed)
                    self.columns.append(column)

                    scroll.setWidget(column)
                    layout.addWidget(scroll, 1)
                except Exception as e:
                    print(f"Error creating Kanban column for {status}: {e}")
                    continue

            self.layout_widget.setLayout(layout)

            # Add layout_widget to main layout
            main_layout.addWidget(self.layout_widget)
        except Exception as e:
            print(f"Error in Kanban init_ui: {e}")

    def on_status_changed(self, app_id, new_status):
        """Handle status change from drag and drop."""
        try:
            self.refresh()
            self.application_updated.emit()
            # Show the moved card's details in the (non-modal) detail panel.
            # Safe now that application_selected just updates the panel in
            # place instead of popping a modal dialog.
            self.application_selected.emit(app_id)
        except Exception as e:
            print(f"Error handling status change: {e}")

    def refresh(self):
        """Refresh kanban board with updated applications."""
        try:
            # Reinitialize UI
            self.init_ui()
        except Exception as e:
            print(f"Error refreshing Kanban: {e}")
