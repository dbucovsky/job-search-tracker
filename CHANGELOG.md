# Job Search Tracker - Version History

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
- **Latest Version**: 0.5.9
- **Stability**: Stable - All core features working correctly
- **Next Major Version Target**: 1.0.0 (when additional major features are planned)

