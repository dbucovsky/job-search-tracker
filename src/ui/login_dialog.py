"""
Login and registration dialog for user authentication.
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QWidget
from PyQt5.QtCore import pyqtSignal
from src.database.db_manager import DatabaseManager


class LoginDialog(QDialog):
    """Dialog for user login and registration."""
    
    user_logged_in = pyqtSignal(int, str)  # Signal: (user_id, username)
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Job Search Tracker - Login")
        self.setGeometry(300, 300, 420, 320)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        """Initialize login/register UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        # Title
        title = QLabel("Job Search Tracker")
        title.setProperty("heading", True)
        layout.addWidget(title)

        subtitle = QLabel("Sign in to keep tracking your applications.")
        subtitle.setProperty("subheading", True)
        layout.addWidget(subtitle)
        layout.addSpacing(6)

        # Tabs for Login and Register
        tab_widget = QTabWidget()

        # Login tab
        login_widget = QWidget()
        login_layout = QVBoxLayout()
        login_layout.setSpacing(8)

        login_layout.addWidget(QLabel("Username:"))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        login_layout.addWidget(self.login_username)

        login_layout.addWidget(QLabel("Password:"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.on_login)
        login_layout.addWidget(self.login_password)

        login_layout.addSpacing(6)
        login_btn = QPushButton("Login")
        login_btn.setProperty("variant", "primary")
        login_btn.clicked.connect(self.on_login)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()

        login_widget.setLayout(login_layout)
        tab_widget.addTab(login_widget, "Login")

        # Register tab
        register_widget = QWidget()
        register_layout = QVBoxLayout()
        register_layout.setSpacing(8)

        register_layout.addWidget(QLabel("New Username:"))
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        register_layout.addWidget(self.register_username)

        register_layout.addWidget(QLabel("Password:"))
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("At least 4 characters")
        register_layout.addWidget(self.register_password)

        register_layout.addWidget(QLabel("Confirm Password:"))
        self.register_confirm = QLineEdit()
        self.register_confirm.setEchoMode(QLineEdit.Password)
        self.register_confirm.setPlaceholderText("Re-enter your password")
        self.register_confirm.returnPressed.connect(self.on_register)
        register_layout.addWidget(self.register_confirm)

        register_layout.addSpacing(6)
        register_btn = QPushButton("Register")
        register_btn.setProperty("variant", "primary")
        register_btn.clicked.connect(self.on_register)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()

        register_widget.setLayout(register_layout)
        tab_widget.addTab(register_widget, "Register")

        layout.addWidget(tab_widget)
        self.setLayout(layout)
    
    def on_login(self):
        """Handle login."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            self.show_error("Please enter username and password")
            return
        
        user = self.db_manager.get_user_by_username(username)
        if user and self.db_manager.verify_password(username, password):
            self.user_logged_in.emit(user['id'], user['username'])
            self.accept()
        else:
            self.show_error("Invalid username or password")
            self.login_password.clear()

    def on_register(self):
        """Handle registration."""
        username = self.register_username.text().strip()
        password = self.register_password.text()
        confirm = self.register_confirm.text()
        
        if not username or not password or not confirm:
            self.show_error("Please fill in all fields")
            return
        
        if password != confirm:
            self.show_error("Passwords do not match")
            self.register_password.clear()
            self.register_confirm.clear()
            return
        
        if len(password) < 4:
            self.show_error("Password must be at least 4 characters")
            return
        
        if self.db_manager.get_user_by_username(username):
            self.show_error("Username already exists")
            return
        
        user = self.db_manager.create_user(username, password)
        self.user_logged_in.emit(user['id'], user['username'])
        self.accept()
    
    def show_error(self, message):
        """Show error message."""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Error", message)
