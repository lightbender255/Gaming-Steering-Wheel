import os
import sys
import time
import logging
import pywinusb.hid as hid
from typing import List, Optional, Any  # For type hinting
import threading

class HidDeviceManager:
    """
    Manages enumeration and event listening for HID devices using pywinusb.
    """

    def __init__(self):
        """Initializes the device manager."""
        self.devices: List[hid.HidDevice] = []
        self.listening_device: Optional[hid.HidDevice] = None
        self._is_listening: bool = False
        self._stop_event = threading.Event()  # Event to signal stop

    def enumerate_devices(self) -> int:
        """
        Finds all HID devices and stores them internally.
        Returns the number of devices found.
        """
        logging.info("--- Enumerating HID Devices ---")
        try:
            # Clear previous list if re-enumerating
            self.devices = hid.find_all_hid_devices()
            if not self.devices:
                logging.info("No HID devices found.")
                return 0
            logging.info(f"Found {len(self.devices)} HID devices.")
            return len(self.devices)
        except Exception as e:
            logging.error(f"An error occurred during enumeration: {e}")
            self.devices = []
            return 0

    def display_devices(self, show_inputs: bool = True):
        """
        Displays detailed information about the enumerated devices.

        Args:
            show_inputs: If True, attempts to open each device and list
                         its input capabilities from the report descriptor.
        """
        if not self.devices:
            logging.info("No devices to display. Call enumerate_devices() first.")
            return

        logging.info("\n--- Displaying Device Information ---")
        for index, device in enumerate(self.devices):
            logging.info(f"\nDevice {index}:")
            # Use getattr to safely access potentially missing string attributes
            logging.info(f"  Vendor ID : {getattr(device, 'vendor_id', 'N/A'):#06x}")
            logging.info(f"  Product ID: {getattr(device, 'product_id', 'N/A'):#06x}")
            logging.info(f"  Version   : {getattr(device, 'version_number', 'N/A')}")
            # Instance ID and Path are usually reliable from the OS enumeration
            logging.info(f"  Instance ID: {getattr(device, 'instance_id', 'N/A')}")
            # Safely access potentially missing string descriptors
            logging.info(f"  Manuf. Str: {getattr(device, 'manufacturer_name', 'N/A')}")
            logging.info(f"  Product Str: {getattr(device, 'product_name', 'N/A')}")
            logging.info(f"  Path      : {getattr(device, 'device_path', 'N/A')}")

            if show_inputs:
                # --- Attempt to Inspect Inputs (Requires Opening Device) ---
                dev_opened = False
                try:
                    # Ensure device is opened if not already
                    # Check if it's opened *before* trying to open
                    needs_open = not device.is_opened()
                    if needs_open:
                        device.open()
                        dev_opened = True  # Track if we opened it here

                    report_inputs = device.find_input_reports()
                    if report_inputs:
                        logging.info("  Input Capabilities (from Report Descriptor):")
                        for report in report_inputs:
                            for usage_path, usage_val_obj in report.items():
                                report_id_val = getattr(usage_val_obj, 'report_id', None)
                                usage_page_val = getattr(usage_val_obj, 'usage_page', 0)
                                usage_id_val = getattr(usage_val_obj, 'usage_id', 0)
                                report_size_val = getattr(usage_val_obj, 'report_size', 0)
                                report_count_val = getattr(usage_val_obj, 'report_count', 0)

                                logging.info(
                                    f"    - Report ID: {report_id_val if report_id_val is not None else 'N/A'}, "
                                    f"Usage: {usage_page_val:#04x}:{usage_id_val:#04x}, "
                                    f"Size: {report_size_val} bits, Count: {report_count_val}")
                    else:
                        logging.info(
                            "  Could not find detailed input reports (or device requires special handling).")

                except Exception as e:
                    # Catching specific exceptions like hid.HIDError might be better
                    logging.error(f"  Could not open/inspect device reports: {e}")
                finally:
                    # Only close if we opened it within this method
                    if dev_opened and device.is_opened():
                        device.close()
        logging.info("\n--- Device Display Complete ---")

    def _raw_event_handler(self, data: List[int]):
        """Internal callback function when raw data is received."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info(f"[{timestamp}] Raw Data: {data}")

    def start_listening(self, device_index: int):
        """
        Starts listening to raw HID events from the device at the specified index.
        This method blocks until listening stops or the device is unplugged.
        """
        self.listening_device = self.devices[device_index]
        logging.debug(f"Listening device object: {self.listening_device}")  # Added debug line
        logging.debug(f"Device attributes: {dir(self.listening_device)}")  # Added debug line

        if self._is_listening:
            logging.info("Already listening to a device. Stop first.")
            return
        if not (0 <= device_index < len(self.devices)):
            logging.error(f"Error: Device index {device_index} is out of bounds.")
            return

        self.listening_device = self.devices[device_index]

        try:
            # logging.info(
            logging.info(f"\n--- Attempting to listen to: {self.listening_device.product_name} (Index: {device_index}) ---")
            self.listening_device.open(mode=hid.HID_READ_ACCESS)  # Ensure read access

            # Set the raw data handler
            self.listening_device.set_raw_data_handler(self._raw_event_handler)
            self._is_listening = True
            self._stop_event.clear() # Reset the stop event
            logging.info("Listening for events... Press Ctrl+C to stop.")

            # Keep this thread alive while listening and device is plugged
            # The handler runs in a background thread managed by pywinusb
            while self._is_listening and self.listening_device.is_plugged() and not self._stop_event.is_set():
                time.sleep(0.1)  # Check more frequently

            if not self.listening_device.is_plugged():
                logging.info("Device appears to have been unplugged.")

        except Exception as e:
            logging.error(f"Error starting listener for device {device_index}: {e}")
            logging.error("Ensure the script has necessary permissions (may need 'Run as Administrator').")
            self._is_listening = False  # Ensure state is correct on error
            if self.listening_device and self.listening_device.is_opened():
                self.listening_device.close()
            self.listening_device = None
        finally:
            # If the loop exited cleanly (e.g., unplugged), ensure stop logic runs
            if self._is_listening:
                self.stop_listening()  # Call stop to clean up state and handler

    def stop_listening(self):
        """Stops listening to the current device and closes it."""
        if not self._is_listening or self.listening_device is None:
            logging.info("Not currently listening.")
            return

        logging.info("\n--- Stopping Listener ---")
        self._is_listening = False  # Signal the loop in start_listening to exit
        self._stop_event.set() # Set the event to stop the loop

        try:
            if self.listening_device.is_opened():
                # Attempt to remove the handler (optional, closing usually suffices)
                # self.listening_device.set_raw_data_handler(None)
                self.listening_device.close()
                logging.info(f"Closed device: {self.listening_device.product_name}")
        except Exception as e:
            logging.error(f"Error closing device: {e}")
        finally:
            self.listening_device = None
            logging.info("Listener stopped.")

    def get_device(self, index: int) -> Optional[hid.HidDevice]:
        """Gets the device object at the specified index."""
        if 0 <= index < len(self.devices):
            return self.devices[index]
        return None


# --- Main Execution ---
if __name__ == "__main__":
    
    # Change working directory to the directory that contains this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create the log file if it does not exist
    open('logs/hid_listener.log', 'a').close()
    
    logging.basicConfig(filename='logs/hid_listener.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    manager = HidDeviceManager()
    listener_started_successfully = False

    try:
        num_devices = manager.enumerate_devices()
        if num_devices > 0:
            manager.display_devices(show_inputs=True)

            # --- Select Device to Listen To ---
            # Example: Listen to the first device found (index 0)
            # Modify this index based on the output of display_devices()
            target_device_index = 0
            logging.info(f"\n*** Will attempt to listen to device index: {target_device_index} ***")
            time.sleep(1)  # Brief pause before potentially blocking

            target_device = manager.get_device(target_device_index)
            if target_device:
                # This call will block until Ctrl+C, device unplugged, or error
                manager.start_listening(target_device_index)
                # If start_listening exits normally (e.g. unplugged),
                # it calls stop_listening internally via its finally block.
            else:
                logging.info(f"Could not get device at index {target_device_index}.")

        else:
            logging.info("\nNo HID devices found to interact with.")

    except KeyboardInterrupt:
        logging.info("\nCtrl+C detected. Initiating shutdown...")
        manager.stop_listening()
    except Exception as e:
        logging.error(f"\nAn unexpected error occurred in main execution: {e}")
    finally:
        # Ensure listening stops cleanly if it was running
        logging.info("Performing final cleanup...")
        #manager.stop_listening()  # Safe to call even if not listening
        logging.info("Program finished.")
        sys.exit(0)
