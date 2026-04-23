import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, ACEestApp


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_setup_workout_tab_configures_treeview_headings():
    fake_tree = MagicMock()
    fake_button = MagicMock()

    gui = ACEestApp.__new__(ACEestApp)
    gui.tab_workouts = object()

    with patch("app.ttk.Treeview", return_value=fake_tree), patch("app.ttk.Button", return_value=fake_button):
        gui.setup_workout_tab()

    expected_columns = ("date", "type", "duration", "notes")
    assert fake_tree.heading.call_count == len(expected_columns)
    for column in expected_columns:
        fake_tree.heading.assert_any_call(column, text=column.title())
