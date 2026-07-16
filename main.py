"""
Main entry point for Job Search Tracker application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow
from src.ui.login_dialog import LoginDialog


def main():
    """Run the application."""
    # Initialize database
    db_manager = DatabaseManager("data/job_tracker.db")
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Show login dialog
    login_dialog = LoginDialog(db_manager)
    if login_dialog.exec_() != LoginDialog.Accepted:
        # User cancelled login
        sys.exit(0)
    
    # Get logged in user info (emitted by login_dialog signal)
    # We need to store it from the signal
    user_id = None
    username = None
    
    def on_user_logged_in(uid, uname):
        nonlocal user_id, username
        user_id = uid
        username = uname
    
    login_dialog.user_logged_in.connect(on_user_logged_in)
    
    # Create main window with user context
    window = MainWindow(db_manager, user_id, username)
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
