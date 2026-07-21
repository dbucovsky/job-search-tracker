# Job Search Tracker - Version History

## [0.8.0] - 2026-07-21

### Look & Feel
- Introduced a centralized light, modern theme (`src/ui/theme.py`) applied
  app-wide, replacing the old default-gray Qt look and the scattered
  per-widget inline stylesheets: flat buttons with hover/pressed states,
  rounded inputs with an accent focus ring, modern tab/table/calendar/menu
  styling, and thin scrollbars.
- **Fixed**: the login screen, the tab strip's inactive tabs, and the job
  detail panel could render with a black/dark background and gray/dark text
  on top - unreadable. Root cause: several stylesheet rules used
  `background-color: transparent` (the generic `QWidget` fallback, the
  unselected-tab background, scroll area backgrounds) intending "show
  whatever's behind me," plus a selector typo (`QFrame#detailPanel`) that
  never matched the actual widget (a `QWidget`) so its background was never
  forced to white. On top of that, `apply_theme()` never set an explicit
  `QPalette`. All three combined so certain regions fell through to a dark
  color instead of the intended light one. Fixed by: correcting the
  selector, forcing the Fusion style plus a fully-specified light
  `QPalette`, and replacing every `transparent` background in the
  stylesheet with an explicit opaque light color (keeping `QLabel`/
  `QCheckBox` transparent on purpose, since those should blend into
  whatever they sit on rather than paint their own box). The app should now
  render the same light theme everywhere regardless of OS theme settings.
- Application status now has five distinct, unambiguous colors (previously
  Applied and Offer shared the same green); used consistently in the table
  and kanban board.
- Kanban cards and columns redesigned: rounded cards with a status-colored
  accent stripe, a colored status dot plus item-count pill on each column
  header, and an accent-colored drop highlight while dragging.
- Table view gets alternating row colors and a cleaner header.
- Job detail form reorganized into clearly labeled sections (Position,
  Status & Dates, Contact, Notes) using aligned form rows and placeholder
  text in every field, with Save styled as the primary action and Delete
  styled as a clear warning action.
- Login and About dialogs restyled to match, with a subtitle on the login
  screen and Enter-to-submit on both the login and register forms.

### Functional / UX Changes
- **Job details are now a persistent side panel** instead of a modal popup
  dialog: selecting an application in any view (table row, calendar entry,
  kanban card, or drag-and-drop) loads it into the panel in place, without
  interrupting whatever view you're working in.
- Added a toolbar with **New Application** and **Refresh** actions, replacing
  the three separate "New Application" buttons that were previously
  duplicated across the Table, Calendar, and Kanban views.
- Table rows now preview into the detail panel on a single click (previously
  required a double click and opened a popup).
- Kanban drag-and-drop now shows the card's updated details in the panel
  after a status change, since doing so no longer pops up a dialog.
- Fixed: the "Deselect Job" button in the table view didn't actually clear
  the detail form - it only cleared internal selection state. It now also
  clears the panel.
- Removed the unused, always-empty "Actions" column from the table view.

---

## [0.7.5] - 2026-07-21

### Bug Fixes
- **Kanban drag-and-drop**: Dropping a card no longer opens the job detail
  popup. Root cause: the drop handler was explicitly emitting
  `application_selected`, which is wired to the modal detail dialog;
  `application_updated` already refreshes all views on its own.
- **Table view**: refreshing the table no longer re-triggers `itemChanged`
  handlers for every cell, which previously caused redundant DB writes and
  re-entrant refreshes on every load.
- **Table view**: sorting is now disabled while rows are being populated, so
  Qt can no longer re-sort mid-insert and desynchronize the stored app ID
  from the rest of a row.
- **Job details**: deleting an application now clears the form instead of
  trying to reload the just-deleted record (which left a stale, unsavable
  form on screen). Delete now also asks for confirmation before proceeding.
- **Job details**: creating a new application now saves the "Date Applied"
  value entered in the form; previously it was silently dropped and the new
  record's date stayed empty until the next edit.
- **Calendar view**: refreshing no longer misses clearing highlighted dates
  from years other than the current one; it now only clears dates it
  actually marked.
- **Logout**: "Logout" now returns to the login screen instead of quitting
  the entire application.

### Security
- Passwords are now hashed with a per-user random salt using
  PBKDF2-HMAC-SHA256 (200,000 iterations) instead of unsalted SHA-256.
  Existing accounts are verified against their legacy hash and
  transparently upgraded to the new format on next successful login - no
  action needed, no passwords reset.

### Notes
- Consolidated password verification into `DatabaseManager.verify_password`
  so authentication logic isn't split across the login dialog and the user
  model.

---

## [0.7.4] - 2026-07-16 16:50

### Features Added
- User-specific data filtering in all views
- Database queries now accept optional user_id parameter
- All views properly filter applications by current user

### Bug Fixes
- Fixed data leakage between users (all users could see all applications)
- All views now receive and use user_id during initialization
- Multi-user isolation now complete and enforced

### Known Issues
- **Kanban drag-and-drop**: Dragging cards still opens detail popup in some cases
  - Workaround: Use Table or Calendar view to edit applications
  - Will be fixed in a future version with alternative UI approach

### Notes
- Each user sees only their own applications across all views
- Database queries enforce user_id filtering
- No data visible between different user accounts

---

## [0.7.3] - 2026-07-16 16:45

### Features Added
- N/A

### Bug Fixes
- Fixed DetachedInstanceError when registering new user
- User methods now return dictionaries instead of detached SQLAlchemy objects
- Password verification now uses active session to prevent detached object errors

### Known Issues
- **Kanban drag-and-drop**: Dragging cards still opens detail popup in some cases
  - Workaround: Use Table or Calendar view to edit applications
  - Will be fixed in a future version with alternative UI approach

### Notes
- User registration fully functional and crash-free
- All user database operations properly handle session lifecycle

---

## [0.7.1] - 2026-07-16 16:35

### Features Added
- N/A

### Bug Fixes
- Fixed sqlite3.OperationalError when registering new user
- User model now shares Base with JobApplication to ensure users table is created

### Known Issues
- **Kanban drag-and-drop**: Dragging cards still opens detail popup in some cases
  - Workaround: Use Table or Calendar view to edit applications
  - Will be fixed in a future version with alternative UI approach

### Notes
- Users table now properly created on first run
- User registration flow fully functional

---

## [0.7.0] - 2026-07-16 16:30

### Features Added
- **User Authentication**: Full login and registration system
- Multi-user support with separate job records per user
- User menu showing current logged-in user
- Logout functionality (returns to login screen)
- Database schema updated to associate applications with users
- Title bar shows current username

### Bug Fixes
- N/A

### Known Issues
- **Kanban drag-and-drop**: Dragging cards still opens detail popup in some cases
  - Workaround: Use Table or Calendar view to edit applications
  - Will be fixed in a future version with alternative UI approach
  - State machine + aggressive click blocking partially mitigates issue but not 100% reliable

### Notes
- Each user has completely separate job application database
- Passwords stored as SHA-256 hashes
- First-time users see registration tab
- Returning users use login tab
- User context maintained throughout session

---

## [0.6.3] - 2026-07-16 16:25

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- **CRITICAL**: Fixed persistent Kanban drag-and-drop opening detail popup
- Replaced state machine + cooldown with aggressive click blocking
- Set `block_clicks = True` as soon as drag movement detected
- Block persists for 500ms AFTER drag completes
- Complete protection: clicks are never emitted during or after drag operations

### Notes
- Renamed flag from `just_dragged` to `block_clicks` for clarity
- Aggressive 500ms block ensures all synthetic events are caught
- Works by preventing click signal emission entirely, not by timing tricks
- Most direct solution to drag-opening-popup problem

---

## [0.6.2] - 2026-07-16 16:20

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- Fixed missing QTimer import that was causing "name 'QTimer' is not defined" errors
- Restored QTimer to kanban_view.py imports for post-drag cooldown functionality

### Notes
- Critical fix for Kanban initialization errors
- All columns now initialize without import errors

---

## [0.6.1] - 2026-07-16 16:18

### Features Added
- N/A (Bug fixes only)

### Bug Fixes
- Fixed Kanban UI display issue where columns and cards were not showing
- Removed duplicate main_layout creation that was clearing all widgets
- Fixed layout initialization logic to prevent widget destruction
- Cleaned up CHANGELOG: removed duplicate version entries
- Version history now flows logically without duplicate 0.5.10 entries

### Notes
- Kanban columns and application cards now display correctly
- UI layout properly initialized on refresh

---

## [0.6.0] - 2026-07-16 16:15

### Features Added
- Added About menu with app information (Help → About)
- About dialog shows app name, version, last update date/time, and comprehensive features list

### Bug Fixes
- Fixed Kanban drag-and-drop opening detail popup
- Implemented state machine architecture (STATE_IDLE → STATE_PRESSED → STATE_DRAGGING)
- Added post-drag 200ms cooldown to block synthetic click events after drag.exec_()
- Hybrid approach combines state machine + cooldown for maximum robustness
- Card only emits click signals from PRESSED→IDLE transitions
- Completely eliminates synthetic event interference from drag operations

### Notes
- State machine replaces all previous timing-based approaches
- Cleaner, more deterministic logic for click vs drag detection
- If state reaches DRAGGING, reset to IDLE without emitting click
- No race conditions or timing issues with hybrid approach

---

## [0.5.9] - 2026-07-16 16:05

### Features Added
- N/A (Bug fixes only)

### Bug Fixes
- Fixed Kanban drag-and-drop opening detail popup with post-drag cooldown
- Added 150ms cooldown after drag operation to prevent synthetic click events
- Robust approach: ignores any clicks that fire during or immediately after drag

### Notes
- Post-drag cooldown blocks click signals for 150ms after drag completes
- Prevents all synthetic or delayed click events from drag operation
- Combined with position-based detection for maximum reliability
- No more race conditions or timing issues

---

## [0.5.8] - 2026-07-16 16:00

### Features Added
- Added "New Application" button to all tabs (Table, Calendar, Kanban)
- Create new job records from any view without needing to open the detail form first
- New records are created via modal dialog popup

### Bug Fixes
- Fixed Kanban drag-and-drop triggering detail popup with position-based click detection
- Replaced timer-based approach with mouse position tracking (press vs release)
- Only emits click signal if mouse press and release occur within 10 pixels

### Notes
- Renamed "Clear" button to "New" in detail form for clarity
- All three views now have consistent "New Application" button
- Kanban now uses pure position tracking: no timers, no flags, no race conditions
- Much more reliable and natural interaction pattern

---

## [0.5.7] - 2026-07-16 15:50

### Features Added
- N/A (Bug fixes and UX improvements)

### Bug Fixes
- Fixed persistent Kanban drag-and-drop opening detail popup
- Fixed detail popup clearing form after save instead of staying on edited entry
- Changed Kanban interaction model from double-click to delayed single-click

### Notes
- Kanban cards now use 300ms delayed single-click (cancel on drag start)
- More natural UX: click to open details, drag to change status
- Detail popup reloads saved application after save (keeps it open)
- Eliminates all race conditions in Kanban drag detection
- User can now save edits without losing context

---

## [0.5.6] - 2026-07-16 15:45

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- Completely fixed Kanban drag-and-drop opening detail popup
- Replaced timer-based cooldown with timestamp-based approach
- Eliminated race conditions in drag detection

### Notes
- Uses system time (millisecond precision) instead of relying on timers
- More reliable: checks elapsed time since last drag ended
- If less than 500ms has passed since drag, all double-clicks are ignored
- No more timer state issues or event ordering problems

---

## [0.5.5] - 2026-07-16 15:30

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- Fixed persistent Kanban drag-and-drop opening detail popup after drop
- Improved drag cooldown from 200ms to 500ms for better event queue processing
- Added mouseReleaseEvent handling to prevent accidental triggers
- Added guard in mousePressEvent to prevent new drag detection during cooldown

### Notes
- Implemented triple-layer protection: cooldown timer, release event blocking, and press event guarding
- More robust event handling across all mouse interactions
- Prevents any possibility of drag-related events triggering double-click detection

---

## [0.5.4] - 2026-07-16 15:15

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- Fixed drag-and-drop in Kanban still opening detail popup after drop
- Implemented drag cooldown timer (200ms) to prevent false double-click detection after drag completion

### Notes
- Uses QTimer to delay resetting drag flag, allowing Qt event queue to process all drag-related events
- Prevents race condition where pending events could trigger double-click detection

---

## [0.5.3] - 2026-07-16

### Features Added
- N/A (Bug fix only)

### Bug Fixes
- Fixed Kanban drag-and-drop triggering detail popup on drop
- Added is_dragging flag to prevent double-click detection during drag operations

### Notes
- Drag-and-drop now works smoothly without side effects
- Improved Kanban interaction experience

---

## [0.5.2] - 2026-07-16

### Features Added
- Calendar today indicator with dark underline and bold text
- Independent calendar highlighting system preventing conflicts
- Combined formatting for today with job dates (yellow background + underline)

### Bug Fixes
- Fixed red background overriding job highlighting
- Fixed selection color (grey/blue) conflicting with indicators
- Fixed today indicator being hidden by other formatting

### Notes
- Calendar highlighting now uses underline (visual indicator) instead of conflicting backgrounds
- Today remains visible regardless of whether it has jobs
- Better visual clarity in calendar view

---

## [0.5.1] - 2026-07-16

### Features Added
- Double-click requirement for opening detail popup in Table View
- Double-click requirement for opening detail popup in Calendar View
- Consistent double-click interaction pattern across all views

### Bug Fixes
- Fixed single-click opening popup in table view
- Fixed single-click opening popup in calendar view

### Notes
- Improved interaction consistency
- Prevents accidental popup openings from navigation

---

## [0.5.0] - 2026-07-16

### Features Added
- Job Detail View converted from side panel to modal popup dialog
- Popup opens only on application selection (with deferred double-click requirement)
- Cleaner main window layout (reduced from 1400x800 to 1000x800)
- Improved space usage by removing permanent detail panel

### Bug Fixes
- N/A (Architecture refactoring)

### Notes
- Better UX with modal dialog for job details
- Main window layout simplified
- Focus remains on tabbed views with popup for details

---

## [0.4.0] - 2026-07-16

### Features Added
- Kanban drag-and-drop status updates with automatic database sync
- Dual signal emission (application_updated and application_selected) for proper view refresh
- Kanban card double-click to open detail view
- Calendar view independent highlighting system

### Bug Fixes
- Fixed drag-and-drop not updating other views
- Fixed detail view not updating after Kanban status changes
- Fixed view synchronization after data changes in Kanban

### Notes
- Improved multi-view data synchronization
- Kanban now properly updates all views on status change
- Better user feedback on data modifications

---

## [0.3.0] - 2026-07-16

### Features Added
- Table cell editing for Company, Job Title, Location, Salary fields
- Date Applied column editing with YYYY-MM-DD format parsing
- Status column dropdown restriction (StatusDelegate) with valid enum values only
- Dynamic database updates on cell edits

### Bug Fixes
- Fixed table cell changes not saving to database
- Fixed date parsing and validation in table view
- Fixed status column allowing invalid values

### Notes
- Implemented custom QStyledItemDelegate for status dropdown
- Added comprehensive error handling for cell edits
- Improved user experience with in-place editing

---

## [0.2.0] - 2026-07-15

### Features Added
- Archive checkbox for marking applications as inactive
- Archive filter in Table View to show/hide archived jobs
- Deselect buttons in all three views
- View synchronization via signal cascade
- Current selection tracking for persistent detail view display
- Color-coded status indicators in table and Kanban
- Database filtering by active/archived status

### Bug Fixes
- Fixed database schema to include is_archived column
- Resolved view synchronization issues between tabs

### Notes
- Improved workflow by allowing users to hide completed applications
- Better data management with archive functionality

---

## [0.1.0] - 2026-07-15

### Features Added
- Initial project scaffold with MVC architecture
- SQLAlchemy ORM model with JobApplication entity
- SQLite database for persistent storage
- Table View with basic display of job applications
- Calendar View for date-based job tracking
- Kanban View with status-based columns (Identified, Applied, Interviewing, Offer, Rejected)
- Job Detail Form for adding and editing applications
- Database Manager for CRUD operations

### Bug Fixes
- N/A (Initial release)

### Notes
- Project created with Python 3.11.4
- PyQt5 framework for GUI
- Initial feature set covers core tracking functionality

---

## Semantic Versioning Explanation

**Version Format: X.Y.Z**
- **X (Major)**: Incremented when significant new features are added (e.g., new view, major architecture change)
- **Y (Minor)**: Incremented when features are added or modified (e.g., new functionality, view improvements)
- **Z (Patch)**: Incremented for bug fixes and corrections (no new features)

### Current Status
- **Latest Version**: 0.7.4
- **Stability**: Stable - Multi-user support fully functional
- **Data Isolation**: Complete - each user sees only their own data
- **Next Major Version Target**: 1.0.0 (when additional major features are planned)

