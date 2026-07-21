"""
Central light theme for the Job Search Tracker UI.

Widgets should prefer these constants and the shared stylesheet over ad-hoc
inline setStyleSheet() calls, so the app reads as one consistent design
instead of a patchwork of per-widget colors. Per-instance styling is still
fine when a property is genuinely data-driven (e.g. a kanban card's status
accent color) - see kanban_view.py for that pattern.
"""
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QStyleFactory

# Base palette
BG_APP = "#F4F5F7"
SURFACE = "#FFFFFF"
SURFACE_MUTED = "#F8F9FB"
BORDER = "#E1E4E8"
BORDER_STRONG = "#C7CCD1"
TEXT_PRIMARY = "#1F2430"
TEXT_SECONDARY = "#6B7280"

# Accent (primary action color)
ACCENT = "#2F6FED"
ACCENT_HOVER = "#255ACC"
ACCENT_PRESSED = "#1E49A8"
ACCENT_SOFT = "#DCE7FD"

# Semantic
DANGER = "#DC2626"
DANGER_SOFT = "#FEF2F2"
DANGER_SOFT_PRESSED = "#FEE2E2"

FONT_FAMILY = "'Segoe UI', Arial, sans-serif"

STYLESHEET = f"""
* {{
    font-family: {FONT_FAMILY};
    font-size: 10pt;
    color: {TEXT_PRIMARY};
}}

QMainWindow, QDialog {{
    background-color: {BG_APP};
}}

QWidget {{
    background-color: {BG_APP};
}}

/* Leaf widgets that should always blend into whatever they're placed on
   (a card, a panel, a dialog) rather than paint their own opaque box. */
QLabel, QCheckBox {{
    background-color: transparent;
}}

QLabel[heading="true"] {{
    font-size: 15pt;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel[subheading="true"] {{
    font-size: 9pt;
    color: {TEXT_SECONDARY};
}}
QLabel[section="true"] {{
    font-size: 10pt;
    font-weight: 600;
    color: {ACCENT};
    padding-top: 8px;
}}
QLabel[fieldLabel="true"] {{
    font-size: 9pt;
    font-weight: 600;
    color: {TEXT_SECONDARY};
}}

QPushButton {{
    background-color: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 6px;
    padding: 6px 14px;
    color: {TEXT_PRIMARY};
}}
QPushButton:hover {{
    background-color: {SURFACE_MUTED};
    border-color: #9AA1A9;
}}
QPushButton:pressed {{
    background-color: #E4E7EB;
}}
QPushButton:disabled {{
    color: #A6ACB3;
    background-color: {BG_APP};
    border-color: {BORDER};
}}

QPushButton[variant="primary"] {{
    background-color: {ACCENT};
    border: 1px solid {ACCENT};
    color: #FFFFFF;
    font-weight: 600;
}}
QPushButton[variant="primary"]:hover {{
    background-color: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
}}
QPushButton[variant="primary"]:pressed {{
    background-color: {ACCENT_PRESSED};
    border-color: {ACCENT_PRESSED};
}}

QPushButton[variant="danger"] {{
    background-color: {SURFACE};
    border: 1px solid {DANGER};
    color: {DANGER};
}}
QPushButton[variant="danger"]:hover {{
    background-color: {DANGER_SOFT};
}}
QPushButton[variant="danger"]:pressed {{
    background-color: {DANGER_SOFT_PRESSED};
}}

QLineEdit, QTextEdit, QDateEdit, QComboBox {{
    background-color: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 6px;
    padding: 5px 8px;
    selection-background-color: {ACCENT};
    selection-color: #FFFFFF;
}}
QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {{
    border: 1px solid {ACCENT};
}}
QLineEdit:disabled, QTextEdit:disabled {{
    background-color: {BG_APP};
    color: #A6ACB3;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox QAbstractItemView {{
    background-color: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    selection-background-color: {ACCENT};
    selection-color: #FFFFFF;
    outline: 0;
}}

QCheckBox {{
    spacing: 6px;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 6px;
    background: {SURFACE};
    top: -1px;
}}
QTabBar {{
    background-color: {BG_APP};
}}
QTabBar::tab {{
    background: {BG_APP};
    color: {TEXT_SECONDARY};
    padding: 8px 20px;
    margin-right: 2px;
    border: 1px solid {BG_APP};
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{
    background: {SURFACE};
    color: {ACCENT};
    border-color: {BORDER};
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_PRIMARY};
}}

QTableWidget {{
    background-color: {SURFACE};
    alternate-background-color: {SURFACE_MUTED};
    gridline-color: #EEF0F2;
    border: 1px solid {BORDER};
    border-radius: 6px;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT_PRIMARY};
}}
QTableWidget::item {{
    padding: 4px;
}}
QHeaderView::section {{
    background-color: {BG_APP};
    color: {TEXT_SECONDARY};
    padding: 6px;
    border: none;
    border-bottom: 1px solid {BORDER};
    font-weight: 600;
}}

QListWidget {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
}}
QListWidget::item {{
    padding: 6px;
    border-bottom: 1px solid {SURFACE_MUTED};
}}
QListWidget::item:selected {{
    background-color: {ACCENT_SOFT};
    color: {TEXT_PRIMARY};
}}

QScrollArea {{
    border: none;
    background: {BG_APP};
}}
QScrollBar:vertical {{
    background: {SURFACE_MUTED};
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_STRONG};
    border-radius: 5px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: #9AA1A9;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {SURFACE_MUTED};
    height: 10px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER_STRONG};
    border-radius: 5px;
    min-width: 24px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

QCalendarWidget QWidget#qt_calendar_navigationbar {{
    background-color: {SURFACE};
}}
QCalendarWidget QToolButton {{
    color: {TEXT_PRIMARY};
    background-color: {SURFACE};
    border-radius: 4px;
    padding: 4px;
}}
QCalendarWidget QToolButton:hover {{
    background-color: {SURFACE_MUTED};
}}
QCalendarWidget QMenu {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
}}
QCalendarWidget QAbstractItemView:enabled {{
    background-color: {SURFACE};
    selection-background-color: {ACCENT};
    selection-color: #FFFFFF;
}}

QMenuBar {{
    background-color: {SURFACE};
    border-bottom: 1px solid {BORDER};
}}
QMenuBar::item {{
    padding: 6px 10px;
    background: {SURFACE};
}}
QMenuBar::item:selected {{
    background-color: {SURFACE_MUTED};
    border-radius: 4px;
}}
QMenu {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
}}
QMenu::item {{
    padding: 6px 20px;
}}
QMenu::item:selected {{
    background-color: {ACCENT};
    color: #FFFFFF;
}}

QToolBar {{
    background-color: {SURFACE};
    border-bottom: 1px solid {BORDER};
    spacing: 6px;
    padding: 4px;
}}
QToolButton {{
    border-radius: 6px;
    padding: 6px;
}}
QToolButton:hover {{
    background-color: {SURFACE_MUTED};
}}

QSplitter::handle {{
    background-color: {BORDER};
}}
QSplitter::handle:horizontal {{
    width: 1px;
}}

QMessageBox {{
    background-color: {SURFACE};
}}

QFrame#kanbanCard {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}
QFrame#kanbanCard:hover {{
    border: 1px solid {ACCENT};
}}

QFrame#kanbanColumnHeader {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
}}

QWidget#detailPanel {{
    background-color: {SURFACE};
}}
"""


def _build_light_palette():
    """A fully light QPalette covering every color role.

    Qt's native Windows style pulls its default palette from the OS theme,
    so on a machine with "Apps: Dark" enabled, any widget our stylesheet
    doesn't explicitly style (or where a selector fails to match - see the
    detailPanel bug this replaced) falls back to a dark background with our
    light-mode text color on top, which is unreadable. Setting an explicit
    palette closes that gap regardless of stylesheet coverage.
    """
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_APP))
    palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Base, QColor(SURFACE))
    palette.setColor(QPalette.AlternateBase, QColor(SURFACE_MUTED))
    palette.setColor(QPalette.ToolTipBase, QColor(SURFACE))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Button, QColor(SURFACE))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.BrightText, QColor(DANGER))
    palette.setColor(QPalette.Link, QColor(ACCENT))
    palette.setColor(QPalette.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(QPalette.PlaceholderText, QColor(TEXT_SECONDARY))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#A6ACB3"))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor("#A6ACB3"))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#A6ACB3"))
    return palette


def apply_theme(app):
    """Apply the shared light theme to the whole application.

    Forces the Fusion style plus an explicit light QPalette (in addition to
    the stylesheet) so the app looks the same light theme regardless of the
    OS's light/dark setting - the native Windows style otherwise inherits a
    dark palette from the OS for anything our QSS doesn't cover.
    """
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(_build_light_palette())
    app.setStyleSheet(STYLESHEET)
