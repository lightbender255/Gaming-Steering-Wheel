import unittest
import io
from unittest.mock import patch
from pynput import mouse
from hid_listener_001 import MouseClickMonitor

class TestMouseClickMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = MouseClickMonitor()

    @patch('hid_listener_001.mouse.Listener')
    def test_start_monitoring(self, MockListener):
        self.monitor.start_monitoring()
        MockListener.assert_called_once_with(on_click=self.monitor._on_click)
        MockListener().start.assert_called_once()

    @patch('hid_listener_001.mouse.Listener')
    def test_start_monitoring_already_active(self, MockListener):
        MockListener().start.return_value = None
        self.monitor.listener = MockListener()
        self.monitor.start_monitoring()
        MockListener().start.assert_not_called()

    @patch('hid_listener_001.mouse.Listener')
    def test_stop_monitoring(self, MockListener):
        self.monitor.listener = MockListener()
        self.monitor.stop_monitoring()
        MockListener().stop.assert_called_once()

    @patch('hid_listener_001.mouse.Listener')
    def test_stop_monitoring_not_active(self, MockListener):
        self.monitor.stop_monitoring()
        MockListener.assert_not_called()

    def test_on_click_left_click(self):
        with patch('hid_listener_001.datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-07-26 10:00:00.000000"
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                self.monitor._on_click(100, 200, mouse.Button.left, True)
                expected_output = "2024-07-26 10:00:00.000000 - OOP: Left Click Detected at (100, 200)\n"
                self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_on_click_other_event(self):
        with patch('hid_listener_001.datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-07-26 10:00:00.000000"
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                self.monitor._on_click(100, 200, mouse.Button.right, True)
                self.assertEqual(mock_stdout.getvalue(), "")

    @patch('hid_listener_001.mouse.Listener')
    def test_join(self, MockListener):
        mock_listener = MockListener()
        self.monitor.listener = mock_listener
        self.monitor.join()
        mock_listener.join.assert_called_once()

    @patch('hid_listener_001.mouse.Listener')
    def test_join_no_listener(self, MockListener):
        self.monitor.join()
        MockListener.assert_not_called()


if __name__ == '__main__':
    unittest.main()
