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
main.py                       # entry point: DB init -> apply_theme -> LoginDialog -> MainWindow
src/
  database/db_manager.py      # DatabaseManager: all CRUD, session-per-call pattern
  models/
    job_application.py        # JobApplication ORM model + ApplicationStatus enum + Base
    user.py                   # User ORM model (salted PBKDF2 password hashing)
  ui/
    theme.py                  # centralized light QSS theme + color constants (apply_theme(app))
    main_window.py             # QMainWindow: toolbar + tabs/detail-panel splitter + signal wiring
    login_dialog.py           # login / register
    about_dialog.py
    views/
      table_view.py           # editable QTableWidget of applications
      calendar_view.py        # QCalendarWidget, highlights dates with applications
      kanban_view.py          # drag-and-drop board, one column per status
      job_detail_view.py      # persistent (non-modal) side-panel form for add/edit/delete
```

### Key conventions

- **Session-per-operation**: every `DatabaseManager` method opens its own `Session` in a
  `try/finally` and closes it. Never return a live ORM object that will be read after the
  session closes — that raises `DetachedInstanceError`. `add_application` returns the new
  row's plain `id` (not the ORM object) for exactly this reason; user methods return plain
  dicts (see CHANGELOG 0.7.3). Prefer this pattern for any new query.
- **Status is an enum** (`ApplicationStatus`), stored as `SQLEnum`. Compare/assign enum
  members, not raw strings. The detail-panel combobox carries the enum in item *data*, while
  the table stores the enum *value* string in the cell — convert carefully. Status colors
  come from `JobApplication.get_status_color()` — one unique color per status; keep using
  that as the single source of truth rather than duplicating a palette elsewhere.
- **Signals drive the UI.** Views emit `application_selected`, `application_updated`, etc.;
  `MainWindow` wires them. `application_selected` loads the given application into the
  **persistent, non-modal** `JobDetailView` side panel (`main_window.py`'s
  `on_application_selected`) — it does not open anything. This changed in 0.8.0: the detail
  view used to be a modal `QDialog` (`.exec_()`), which is why older code/comments may refer
  to it "popping up" or "opening a popup" — that's no longer how it works.
- **Theming**: `src/ui/theme.py` holds the shared QSS stylesheet and color constants, applied
  once via `apply_theme(app)` in `main.py`, which also forces the Fusion style and an explicit
  light `QPalette` — this is required, not decorative: Qt's native Windows style otherwise
  inherits a dark palette from the OS's dark-mode setting for anything the stylesheet doesn't
  cover, which is unreadable against the app's light-mode text colors. Don't remove the
  `app.setStyle(...)`/`app.setPalette(...)` calls in `apply_theme()`. Prefer adding to/reusing
  the stylesheet over new inline `setStyleSheet()` calls; inline styles are only for genuinely
  per-instance, data-driven values (e.g. a kanban card's status-accent color, set via
  `objectName` + a narrow instance-level QSS override — see `KanbanCard` for the pattern).
  When adding an `objectName`-based selector, double check the selector's widget type matches
  the actual base class (e.g. `QFrame#foo` silently never matches a plain `QWidget` subclass
  named "foo" — this caused the detail panel dark-background bug fixed in 0.8.0).
- **Toolbar over per-view buttons**: "New Application" and "Refresh" live once on the
  `MainWindow` toolbar (built with `QStyle` standard icons, no icon assets needed) rather than
  duplicated per view. Don't re-add a per-view "New Application" button — wire new
  cross-view actions into the toolbar instead.
- **User scoping**: every query that lists applications takes `user_id` and must filter on
  it. All views receive `user_id` at construction (CHANGELOG 0.7.4).

## Known issues / active work

Track detailed status in `CHANGELOG.md` (versioned, newest first). As of 0.8.0 there are no
open bugs being tracked; treat `CHANGELOG.md`'s latest entry as the source of truth going
forward.

## Working agreements

- **Keep `CHANGELOG.md` updated** with a new version entry for user-visible changes, matching
  the existing format (Features Added / Bug Fixes / Known Issues / Notes). Bump the version
  string in `main.py`/docs the way recent commits do.
- Match the existing code style: module docstrings, method docstrings, broad `try/except`
  with `print(...)` diagnostics in UI code.
- Windows is the primary dev environment (PowerShell). Use forward slashes / `os.path` for
  paths.
- Don't commit `data/job_tracker.db` or `.venv/` (already git-ignored).
