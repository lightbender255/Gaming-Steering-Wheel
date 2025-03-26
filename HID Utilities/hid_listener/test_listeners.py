import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from pynput import mouse

# Import the class from hid_listener_001.py
try:
    from hid_listener_001 import MouseClickMonitor
except ImportError:
    print("Error: Could not import MouseClickMonitor from hid_listener_001.py. "
          "Make sure the file is in the same directory or adjust the import path.")
    sys.exit(1)


class TestMouseClickMonitorUnit(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        self.monitor = MouseClickMonitor()
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Cleanup after each test."""
        sys.stdout = sys.__stdout__  # Restore stdout
        if self.monitor.listener:
            self.monitor.stop_monitoring()

    @patch('hid_listener_001.mouse.Listener')
    @patch('hid_listener_001.datetime')
    def test_start_monitoring(self, mock_datetime, mock_listener):
        """Test if start_monitoring starts the listener."""
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance

        self.monitor.start_monitoring()

        mock_listener.assert_called_once_with(on_click=self.monitor._on_click)
        mock_listener_instance.start.assert_called_once()
        self.assertIn("Mouse monitoring started...", self.captured_output.getvalue())

    @patch('hid_listener_001.mouse.Listener')
    def test_start_monitoring_already_active(self, mock_listener):
        """Test if start_monitoring handles being called when already active."""
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance
        self.monitor.listener = mock_listener_instance

        self.monitor.start_monitoring()
        self.assertIn("Monitoring is already active.", self.captured_output.getvalue())
        mock_listener_instance.start.assert_not_called()

    @patch('hid_listener_001.mouse.Listener')
    def test_stop_monitoring(self, mock_listener):
        """Test if stop_monitoring stops the listener."""
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance
        self.monitor.listener = mock_listener_instance

        self.monitor.stop_monitoring()
        mock_listener_instance.stop.assert_called_once()
        self.assertIsNone(self.monitor.listener)
        self.assertIn("Stopping mouse monitoring...", self.captured_output.getvalue())
        self.assertIn("Mouse monitoring stopped.", self.captured_output.getvalue())

    @patch('hid_listener_001.mouse.Listener')
    def test_stop_monitoring_not_active(self, mock_listener):
        """Test if stop_monitoring handles being called when not active."""
        self.monitor.stop_monitoring()
        self.assertIn("Monitoring was not active.", self.captured_output.getvalue())
        mock_listener.assert_not_called()

    @patch('hid_listener_001.datetime')
    def test_on_click_left_click(self, mock_datetime):
        """Test if _on_click correctly handles a left click."""
        mock_datetime.datetime.now.return_value.strftime.return_value = "2023-10-27 10:00:00.000000"
        # Simulate a left click
        self.monitor._on_click(100, 200, mouse.Button.left, True)
        expected_output = "2023-10-27 10:00:00.000000 - OOP: Left Click Detected at (100, 200)\n"
        self.assertIn(expected_output, self.captured_output.getvalue())

    @patch('hid_listener_001.datetime')
    def test_on_click_other_event(self, mock_datetime):
        """Test if _on_click ignores other events (e.g., right click)."""
        mock_datetime.datetime.now.return_value.strftime.return_value = "2023-10-27 10:00:00.000000"
        # Simulate a right click
        self.monitor._on_click(100, 200, mouse.Button.right, True)
        self.assertEqual("", self.captured_output.getvalue())

    @patch('hid_listener_001.mouse.Listener')
    def test_join_no_listener(self, mock_listener):
        """Test if join method works correctly when there is no listener"""
        self.monitor.join()
        mock_listener.assert_not_called()

    @patch('hid_listener_001.mouse.Listener')
    def test_join_with_listener(self, mock_listener):
        """Test if join method works correctly when there is a listener"""
        mock_listener_instance = MagicMock()
        mock_listener.return_value = mock_listener_instance
        self.monitor.listener = mock_listener_instance
        self.monitor.join()
        mock_listener_instance.join.assert_called_once()

if __name__ == '__main__':
    unittest.main()
