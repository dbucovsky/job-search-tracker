"""
Main entry point for Job Search Tracker application.
"""
import sys
from PyQt5.QtWidgets import QApplication
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow


def main():
    """Run the application."""
    # Initialize database
    db_manager = DatabaseManager("data/job_tracker.db")
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow(db_manager)
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
