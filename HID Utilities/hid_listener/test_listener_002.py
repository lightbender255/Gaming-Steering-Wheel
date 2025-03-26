import unittest
from unittest.mock import patch, MagicMock
import logging
import io
from hid_listener_002 import HidDeviceManager

class TestHidDeviceManager(unittest.TestCase):
    def setUp(self):
        self.manager = HidDeviceManager()
        self.mock_device = MagicMock()
        self.mock_device.product_name = "Mock Device"
        self.mock_device.is_plugged.return_value = True
        self.mock_device.is_opened.side_effect = [False, True] # Simulate opening and closing

    @patch('hid_listener_002.hid.find_all_hid_devices')
    def test_enumerate_devices(self, mock_find_devices):
        mock_find_devices.return_value = [self.mock_device]
        num_devices = self.manager.enumerate_devices()
        self.assertEqual(num_devices, 1)

    @patch('hid_listener_002.hid.find_all_hid_devices')
    def test_enumerate_devices_no_devices(self, mock_find_devices):
        mock_find_devices.return_value = []
        num_devices = self.manager.enumerate_devices()
        self.assertEqual(num_devices, 0)

    @patch('hid_listener_002.hid.find_all_hid_devices')
    @patch('hid_listener_002.logging.info')
    def test_display_devices(self, mock_info, mock_find_devices):
        mock_find_devices.return_value = [self.mock_device]
        self.manager.enumerate_devices()
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.manager.display_devices(show_inputs=False)
            self.assertIn("Mock Device", mock_stdout.getvalue())

    @patch('hid_listener_002.hid.find_all_hid_devices')
    def test_display_devices_no_devices(self, mock_find_devices):
        mock_find_devices.return_value = []
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.manager.display_devices()
            self.assertIn("No devices to display", mock_stdout.getvalue())

    @patch('hid_listener_002.hid.HidDevice.open')
    @patch('hid_listener_002.hid.HidDevice.set_raw_data_handler')
    @patch('hid_listener_002.hid.HidDevice.is_plugged')
    @patch('hid_listener_002.time.sleep')
    @patch('hid_listener_002.logging.info')
    def test_start_listening(self, mock_info, mock_sleep, mock_is_plugged, mock_set_handler, mock_open):
        mock_is_plugged.return_value = True
        self.manager.devices = [self.mock_device]
        self.manager.start_listening(0)
        mock_open.assert_called_once()
        mock_set_handler.assert_called_once()

    @patch('hid_listener_002.hid.HidDevice.open')
    @patch('hid_listener_002.logging.error')
    def test_start_listening_error(self, mock_error, mock_open):
        mock_open.side_effect = Exception("Simulated error")
        self.manager.devices = [self.mock_device]
        self.manager.start_listening(0)
        mock_error.assert_called_once()

    @patch('hid_listener_002.hid.HidDevice.close')
    def test_stop_listening(self, mock_close):
        self.manager.listening_device = self.mock_device
        self.manager._is_listening = True
        self.manager.stop_listening()
        mock_close.assert_called_once()

    @patch('hid_listener_002.logging.info')
    def test_stop_listening_not_listening(self, mock_info):
        self.manager.stop_listening()
        mock_info.assert_called_once_with("Not currently listening.")

if __name__ == '__main__':
    unittest.main()
