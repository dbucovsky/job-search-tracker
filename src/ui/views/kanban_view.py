"""
Kanban board view for job applications organized by status.
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QTimer
from PyQt5.QtGui import QDrag, QCursor
from src.models.job_application import ApplicationStatus


class KanbanCard(QFrame):
    """A draggable card in the Kanban board."""
    
    clicked = pyqtSignal(int)  # Signal when card is clicked
    
    def __init__(self, app_id, company_name, job_title, location=None):
        super().__init__()
        self.app_id = app_id
        self.company_name = company_name
        self.job_title = job_title
        self.location = location
        self.press_pos = None  # Position where mouse was pressed
        self.in_drag_cooldown = False  # Flag to prevent clicks right after drag
        self.drag_cooldown_timer = QTimer()  # Timer for post-drag protection
        self.drag_cooldown_timer.setSingleShot(True)
        self.drag_cooldown_timer.timeout.connect(self.on_drag_cooldown_timeout)
        self.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; padding: 8px; margin: 4px; background-color: #f9f9f9;")
        self.setCursor(Qt.OpenHandCursor)
        self.init_ui()
    
    def init_ui(self):
        """Initialize card UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        company_label = QLabel(self.company_name)
        company_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        layout.addWidget(company_label)
        
        title_label = QLabel(self.job_title)
        title_label.setStyleSheet("font-size: 10px; color: #333;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        if self.location:
            location_label = QLabel(f"📍 {self.location}")
            location_label.setStyleSheet("font-size: 9px; color: #666;")
            layout.addWidget(location_label)
        
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        """Handle mouse press - record position for later comparison."""
        if event.button() == Qt.LeftButton:
            self.press_pos = event.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if not (event.buttons() & Qt.LeftButton) or self.press_pos is None:
            return
        
        # Check if movement is large enough to be a drag
        movement = (event.pos() - self.press_pos).manhattanLength()
        if movement < 5:
            return
        
        # Large movement detected - perform drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.app_id))
        mime_data.setData("application/x-app-id", str(self.app_id).encode())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        
        # After drag completes, set cooldown to prevent synthetic click events
        self.in_drag_cooldown = True
        self.drag_cooldown_timer.start(150)  # 150ms cooldown after drag
        self.press_pos = None
    
    def on_drag_cooldown_timeout(self):
        """Called when drag cooldown expires."""
        self.in_drag_cooldown = False
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - emit signal only if not in drag cooldown."""
        if event.button() == Qt.LeftButton:
            # Don't emit click if we're in post-drag cooldown period
            if not self.in_drag_cooldown and self.press_pos is not None:
                # Check if release happened at approximately same position as press
                movement = (event.pos() - self.press_pos).manhattanLength()
                if movement < 10:
                    self.clicked.emit(self.app_id)
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
        self.setAcceptDrops(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize column UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Column header
        header = QLabel(f"{self.status.value}")
        header.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px; background-color: #e0e0e0; border-radius: 3px;")
        layout.addWidget(header)
        
        # Count label
        count_label = QLabel(f"({len(self.applications)} items)")
        count_label.setStyleSheet("font-size: 10px; color: #666;")
        layout.addWidget(count_label)
        
        # Application cards
        for app in self.applications:
            card = KanbanCard(app.id, app.company_name, app.job_title, app.location)
            card.clicked.connect(self.application_selected.emit)
            layout.addWidget(card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def dragEnterEvent(self, event):
        """Handle drag enter."""
        if event.mimeData().hasFormat("application/x-app-id"):
            event.acceptProposedAction()
            self.setStyleSheet("border: 2px solid #4CAF50; border-radius: 4px; background-color: #f0f8f0;")
    
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
    new_record_requested = pyqtSignal()  # Signal to create new record
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
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
                self.setLayout(main_layout)
            else:
                while main_layout.count():
                    main_layout.takeAt(0)
            
            # Add button bar
            button_layout = QHBoxLayout()
            new_btn = QPushButton("New Application")
            new_btn.clicked.connect(self.new_record_requested.emit)
            button_layout.addWidget(new_btn)
            button_layout.addStretch()
            main_layout.addLayout(button_layout)
            
            # Create scroll area for columns
            self.layout_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(10)
            
            # Create columns for each status
            for status in ApplicationStatus:
                try:
                    # Get active applications for this status (not archived)
                    applications = self.db_manager.get_applications_by_status(status, archived=False)
                    
                    # Create scroll area for column
                    scroll = QScrollArea()
                    scroll.setWidgetResizable(True)
                    scroll.setStyleSheet("QScrollArea { border: 1px solid #ddd; border-radius: 4px; background-color: #fafafa; }")
                    
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
            
            # Set main layout
            main_layout = self.layout()
            if main_layout is None:
                main_layout = QVBoxLayout()
                self.setLayout(main_layout)
            else:
                while main_layout.count():
                    main_layout.takeAt(0)
            
            main_layout.addWidget(self.layout_widget)
        except Exception as e:
            print(f"Error in Kanban init_ui: {e}")
    
    def on_status_changed(self, app_id, new_status):
        """Handle status change from drag and drop."""
        try:
            self.refresh()
            # Emit both signals: refresh other views AND update detail view
            self.application_updated.emit()
            # Also emit application_selected to update detail view with new data
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
