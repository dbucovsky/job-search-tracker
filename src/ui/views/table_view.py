"""
Table view for displaying job applications in a table format.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QCheckBox, QComboBox, QStyledItemDelegate
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from datetime import datetime
from src.models.job_application import ApplicationStatus


class StatusDelegate(QStyledItemDelegate):
    """Custom delegate for status column with dropdown."""
    
    def createEditor(self, parent, option, index):
        """Create editor widget."""
        combobox = QComboBox(parent)
        for status in ApplicationStatus:
            combobox.addItem(status.value, status)
        return combobox
    
    def setEditorData(self, editor, index):
        """Set current value in editor."""
        value = index.model().data(index, Qt.DisplayRole)
        idx = editor.findText(value)
        if idx >= 0:
            editor.setCurrentIndex(idx)
    
    def setModelData(self, editor, model, index):
        """Set model data from editor."""
        model.setData(index, editor.currentText(), Qt.EditRole)


class TableView(QWidget):
    """Display job applications in table format."""
    
    application_selected = pyqtSignal(int)  # Signal when an application is selected
    deselect_requested = pyqtSignal()  # Signal to deselect current application
    application_updated = pyqtSignal()  # Signal when application data changes
    new_record_requested = pyqtSignal()  # Signal to create new record
    
    def __init__(self, db_manager, user_id=None):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = user_id
        self.show_archived = False  # Default to hiding archived
        self.updating_item = False  # Flag to prevent recursive updates
        self.init_ui()
    
    def init_ui(self):
        """Initialize table view UI."""
        layout = QVBoxLayout()
        
        # Filter controls
        filter_layout = QHBoxLayout()
        self.show_archived_checkbox = QCheckBox("Show Archived")
        self.show_archived_checkbox.stateChanged.connect(self.on_show_archived_toggled)
        filter_layout.addWidget(self.show_archived_checkbox)
        
        new_btn = QPushButton("New Application")
        new_btn.clicked.connect(self.new_record_requested.emit)
        filter_layout.addWidget(new_btn)
        
        deselect_btn = QPushButton("Deselect Job")
        deselect_btn.clicked.connect(self.deselect_requested.emit)
        filter_layout.addWidget(deselect_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Company", "Job Title", "Status", "Date Applied", "Location", "Salary", "Archived", "Actions"
        ])
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 80)
        
        # Set status column delegate to show dropdown
        self.table.setItemDelegateForColumn(2, StatusDelegate(self))
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        self.table.itemChanged.connect(self.on_item_changed)
        self.table.itemClicked.connect(self.on_row_clicked)
        self.table.itemDoubleClicked.connect(self.on_row_double_clicked)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.refresh_table()
    
    def on_show_archived_toggled(self, state):
        """Handle show archived checkbox toggle."""
        self.show_archived = state == Qt.Checked
        self.refresh_table()
    
    def refresh_table(self):
        """Refresh table with current applications."""
        # Get applications based on archive filter
        if self.show_archived:
            applications = self.db_manager.get_all_applications(user_id=self.user_id)
        else:
            applications = self.db_manager.get_active_applications(user_id=self.user_id)

        # Guard against on_item_changed firing (and writing back to the DB /
        # re-entering refresh) while we populate cells, and disable sorting
        # so Qt doesn't re-sort rows mid-insert and scramble the app_id
        # stored on column 0 relative to the other cells in that row.
        self.updating_item = True
        was_sorting_enabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        try:
            self.table.setRowCount(len(applications))

            for row, app in enumerate(applications):
                # Company
                self.table.setItem(row, 0, QTableWidgetItem(app.company_name))

                # Job Title
                self.table.setItem(row, 1, QTableWidgetItem(app.job_title))

                # Status with color
                status_item = QTableWidgetItem(app.status.value)
                status_color = app.get_status_color(app.status)
                status_item.setBackground(QColor(status_color))
                self.table.setItem(row, 2, status_item)

                # Date Applied
                date_str = app.date_applied.strftime("%Y-%m-%d") if app.date_applied else "N/A"
                self.table.setItem(row, 3, QTableWidgetItem(date_str))

                # Location
                self.table.setItem(row, 4, QTableWidgetItem(app.location or "N/A"))

                # Salary
                self.table.setItem(row, 5, QTableWidgetItem(app.salary_range or "N/A"))

                # Archived checkbox
                archived_item = QTableWidgetItem()
                archived_item.setCheckState(Qt.Checked if app.is_archived else Qt.Unchecked)
                archived_item.app_id = app.id
                self.table.setItem(row, 6, archived_item)

                # Store app ID in first column for identification
                self.table.item(row, 0).app_id = app.id
        finally:
            self.table.setSortingEnabled(was_sorting_enabled)
            self.updating_item = False
    
    def on_row_clicked(self, item):
        """Handle row click - do nothing, wait for double click."""
        pass
    
    def on_row_double_clicked(self, item):
        """Handle row double click to open detail popup."""
        app_id = self.table.item(item.row(), 0).app_id
        self.application_selected.emit(app_id)
    
    def on_item_changed(self, item):
        """Handle item change - for archive checkbox and editable fields."""
        if self.updating_item:
            return
        
        try:
            self.updating_item = True
            app_id_item = self.table.item(item.row(), 0)
            if not app_id_item or not hasattr(app_id_item, 'app_id'):
                self.updating_item = False
                return
            
            app_id = app_id_item.app_id
            column = item.column()
            
            # Handle archive checkbox (column 6)
            if column == 6 and hasattr(item, 'checkState'):
                is_archived = item.checkState() == Qt.Checked
                self.db_manager.update_application(app_id, is_archived=is_archived)
                self.application_updated.emit()
            
            # Handle editable fields
            elif column == 0:  # Company
                self.db_manager.update_application(app_id, company_name=item.text())
                self.application_updated.emit()
            elif column == 1:  # Job Title
                self.db_manager.update_application(app_id, job_title=item.text())
                self.application_updated.emit()
            elif column == 2:  # Status
                try:
                    status_text = item.text()
                    # Find matching ApplicationStatus enum value
                    for status in ApplicationStatus:
                        if status.value == status_text:
                            self.db_manager.update_application(app_id, status=status)
                            self.application_updated.emit()
                            break
                except Exception as e:
                    print(f"Invalid status: {item.text()}")
            elif column == 3:  # Date Applied
                try:
                    from datetime import datetime
                    date_obj = datetime.strptime(item.text(), "%Y-%m-%d").date()
                    self.db_manager.update_application(app_id, date_applied=date_obj)
                    self.application_updated.emit()
                except:
                    print(f"Invalid date format: {item.text()}. Use YYYY-MM-DD")
            elif column == 4:  # Location
                self.db_manager.update_application(app_id, location=item.text())
                self.application_updated.emit()
            elif column == 5:  # Salary
                self.db_manager.update_application(app_id, salary_range=item.text())
                self.application_updated.emit()
            
            self.updating_item = False
        except Exception as e:
            print(f"Error updating field: {e}")
            self.updating_item = False

