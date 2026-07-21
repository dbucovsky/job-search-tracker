"""
Main entry point for Job Search Tracker application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow
from src.ui.login_dialog import LoginDialog
from src.ui.theme import apply_theme


def main():
    """Run the application."""
    # Initialize database
    db_manager = DatabaseManager("data/job_tracker.db")

    # Create Qt application
    app = QApplication(sys.argv)
    apply_theme(app)

    # Loop so that "Logout" returns to the login screen instead of quitting
    # the whole application.
    while True:
        # Create login dialog
        login_dialog = LoginDialog(db_manager)

        # Store user info from signal
        user_id = None
        username = None

        def on_user_logged_in(uid, uname):
            nonlocal user_id, username
            user_id = uid
            username = uname

        # Connect signal BEFORE showing dialog
        login_dialog.user_logged_in.connect(on_user_logged_in)

        # Show login dialog and wait for response
        if login_dialog.exec_() != LoginDialog.Accepted:
            # User cancelled login
            sys.exit(0)

        # Create main window with user context
        window = MainWindow(db_manager, user_id, username)

        logged_out = False

        def on_logout_requested():
            nonlocal logged_out
            logged_out = True

        window.logout_requested.connect(on_logout_requested)
        window.show()

        # Run application until the window closes (via logout or the user
        # closing it directly)
        app.exec_()

        if not logged_out:
            sys.exit(0)


if __name__ == "__main__":
    main()
