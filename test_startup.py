#!/usr/bin/env python3
"""Test script to check for app startup errors without GUI."""
import sys
sys.path.insert(0, '.')

try:
    print("Testing imports...")
    from src.database.db_manager import DatabaseManager
    print("✓ DatabaseManager imported")
    
    from src.ui.main_window import MainWindow
    print("✓ MainWindow imported")
    
    from src.ui.views.table_view import TableView, StatusDelegate
    print("✓ TableView and StatusDelegate imported")
    
    from src.ui.views.calendar_view import CalendarView
    print("✓ CalendarView imported")
    
    from src.ui.views.kanban_view import KanbanView
    print("✓ KanbanView imported")
    
    print("\nAll imports successful!")
    print("Testing database...")
    db = DatabaseManager()
    print("✓ Database initialized")
    
    apps = db.get_active_applications()
    print(f"✓ Database query successful ({len(apps)} active apps)")
    
    print("\n✅ All startup checks passed!")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
