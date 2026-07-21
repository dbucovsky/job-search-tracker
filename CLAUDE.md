# CLAUDE.md — Job Search Tracker (JSB)

Guidance for Claude Code when working in this repository. Continues the development
previously assisted by GitHub Copilot Pro (see `.github/copilot-instructions.md` for the
original scaffold notes).

## What this project is

A **Python 3.11 / PyQt5 desktop app** for tracking job applications, backed by a local
**SQLite** database via **SQLAlchemy 2.0**. Multi-user with local username/password auth.
Data lives in `data/job_tracker.db` (git-ignored).

## Run / test

```bash
# from repo root, with the venv active (.venv/)
python main.py            # launch the app (opens login dialog first)
python test_startup.py    # smoke test that imports + DB init work
pip install -r requirements.txt
```

There is no automated test suite beyond `test_startup.py`. Verify UI changes by running the app.

## Architecture

```
main.py                       # entry point: DB init -> LoginDialog -> MainWindow
src/
  database/db_manager.py      # DatabaseManager: all CRUD, session-per-call pattern
  models/
    job_application.py        # JobApplication ORM model + ApplicationStatus enum + Base
    user.py                   # User ORM model (SHA-256 password hashing)
  ui/
    main_window.py            # QMainWindow: tabs + wiring of signals between views
    login_dialog.py           # login / register
    about_dialog.py
    views/
      table_view.py           # editable QTableWidget of applications
      calendar_view.py        # QCalendarWidget, highlights dates with applications
      kanban_view.py          # drag-and-drop board, one column per status
      job_detail_view.py      # modal QDialog form for add/edit/delete
```

### Key conventions

- **Session-per-operation**: every `DatabaseManager` method opens its own `Session` in a
  `try/finally` and closes it. Never return a live ORM object that will be read after the
  session closes — that raises `DetachedInstanceError`. User methods return plain dicts on
  purpose (see CHANGELOG 0.7.3). Prefer this pattern for any new query.
- **Status is an enum** (`ApplicationStatus`), stored as `SQLEnum`. Compare/assign enum
  members, not raw strings. The detail-view combobox carries the enum in item *data*, while
  the table stores the enum *value* string in the cell — convert carefully.
- **Signals drive the UI.** Views emit `application_selected`, `application_updated`,
  `new_record_requested`, etc.; `MainWindow` wires them. `application_selected` is special:
  it opens the **modal** detail dialog (`job_detail_view.exec_()`). Emitting it from a view
  therefore *pops a dialog* — don't emit it just to refresh data (use `application_updated`).
- **User scoping**: every query that lists applications takes `user_id` and must filter on
  it. All views receive `user_id` at construction (CHANGELOG 0.7.4).

## Known issues / active work

Track detailed status in `CHANGELOG.md` (versioned, newest first). As of 0.7.5, the Kanban
drag-and-drop popup bug, the table-refresh signal storm, the delete/stale-form bug, the
new-application missing-date bug, the calendar cross-year highlight bug, and unsalted
password hashing have all been fixed — see the 0.7.5 entry for details. No open bugs are
currently tracked; treat `CHANGELOG.md`'s latest entry as the source of truth going forward.

## Working agreements

- **Keep `CHANGELOG.md` updated** with a new version entry for user-visible changes, matching
  the existing format (Features Added / Bug Fixes / Known Issues / Notes). Bump the version
  string in `main.py`/docs the way recent commits do.
- Match the existing code style: module docstrings, method docstrings, broad `try/except`
  with `print(...)` diagnostics in UI code.
- Windows is the primary dev environment (PowerShell). Use forward slashes / `os.path` for
  paths.
- Don't commit `data/job_tracker.db` or `.venv/` (already git-ignored).
