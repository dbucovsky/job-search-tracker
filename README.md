# Job Search Tracker

A Python desktop application for tracking your job application progress. Monitor applications, interviews, and offers all in one place with multiple intuitive views.

## Features

- **Table View**: See all applications in a spreadsheet-like format
- **Calendar View**: Track application dates on an interactive calendar
- **Kanban Board**: Organize applications by status (Not Started, Applied, Under Review, Interview Scheduled, Interviewing, Offer Received, Offer Accepted, Rejected, Withdrawn)
- **Job Detail View**: Add, edit, and view detailed information about each application
- **Local Database**: All data stored locally in SQLite database

## Requirements

- Python 3.8+
- PyQt5
- SQLAlchemy

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

## Project Structure

```
JSB/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Database storage
│   └── job_tracker.db    # SQLite database (created on first run)
└── src/
    ├── database/
    │   └── db_manager.py # Database operations
    ├── models/
    │   └── job_application.py # Data models
    └── ui/
        ├── main_window.py # Main application window
        └── views/
            ├── table_view.py       # Table view component
            ├── calendar_view.py    # Calendar view component
            ├── kanban_view.py      # Kanban board component
            └── job_detail_view.py  # Job detail form component
```

## Usage

1. **Add a New Application**: Fill out the form on the right side and click "Save"
2. **View Applications**: Switch between Table, Calendar, and Kanban views to see your applications
3. **Edit an Application**: Click on a row in the table view to load it in the detail form
4. **Delete an Application**: Load an application and click "Delete"
5. **Filter by Status**: Use the Kanban board to see applications grouped by status

## Database Schema

The application uses SQLite with a single main table:

- **job_applications**
  - id (Primary Key)
  - company_name (String)
  - job_title (String)
  - job_url (String, optional)
  - status (Enum: Not Started, Applied, Under Review, Interview Scheduled, Interviewing, Offer Received, Offer Accepted, Rejected, Withdrawn)
  - date_applied (DateTime, optional)
  - date_created (DateTime)
  - date_updated (DateTime)
  - salary_range (String, optional)
  - location (String, optional)
  - contact_name (String, optional)
  - contact_email (String, optional)
  - contact_phone (String, optional)
  - notes (Text, optional)

## Future Enhancements

- Interview tracking and scheduling
- Email template management
- Resume version tracking
- Analytics and statistics
- Export to CSV
- Dark mode
- Application sync across devices
