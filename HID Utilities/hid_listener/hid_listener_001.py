# Example using pynput (install with: pip install pynput)
from pynput import mouse, keyboard
import datetime
from threading import Thread # Using Thread for potentially cleaner separation
import sys
import time

class MouseClickMonitor:
    """
    Monitors system-wide mouse clicks in an OOP manner.
    """
    def __init__(self):
        """Initializes the listener attribute."""
        # Listener will be created in start() to allow instantiation
        # without immediately starting the monitoring thread.
        self.listener: mouse.Listener | None = None
        self._monitor_thread: Thread | None = None
        
        # Also listen to keyboard
        self.keyboard_listener: mouse.Listener | None = None
        self._keyboard_monitor_thread: Thread | None = None
        

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        """Callback method executed when a mouse event occurs."""
        if button == mouse.Button.left and pressed:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            print(f'{timestamp} - OOP: Left Click Detected at ({x}, {y})')
        # Add logic for other buttons or 'released' events (pressed=False) if needed

    def start_monitoring(self):
        """Creates and starts the mouse listener in a separate thread."""
        if self.listener is None:
            # Create the listener instance, connecting it to our callback
            self.listener = mouse.Listener(on_click=self._on_click)
            # Start the listener in its own thread
            # Using listener.start() directly also works and uses threading
            self.listener.start()
            print("Mouse monitoring started...")
        else:
            print("Monitoring is already active.")

    def stop_monitoring(self):
        """Stops the mouse listener."""
        if self.listener:
            print("Stopping mouse monitoring...")
            self.listener.stop()
            # Optional: Wait for the listener thread to actually finish
            # self.listener.join() # Uncomment if blocking until stopped is needed
            self.listener = None
            print("Mouse monitoring stopped.")
        else:
            print("Monitoring was not active.")

    def join(self):
        """Waits for the listener thread to complete (blocks)."""
        if self.listener:
            self.listener.join()

# --- Example Usage (Optional) ---
if __name__ == "__main__":
    monitor = MouseClickMonitor()
    monitor.start_monitoring()
    print("Monitoring mouse clicks... Press Ctrl+C to stop.")
    try:
        monitor.join()
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping monitoring...")
        monitor.stop_monitoring()
        print("Monitoring stopped.")
