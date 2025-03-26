# Example using pynput (install with: pip install pynput)
from pynput import mouse, keyboard
import datetime
import sys
import time

class MouseClickMonitor:
    """
    Monitors system-wide mouse clicks in an OOP manner.
    """
    def __init__(self):
        self.listener: mouse.Listener | None = None
        self._is_running = False

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        if button == mouse.Button.left and pressed:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            print(f'{timestamp} - OOP: Left Click Detected at ({x}, {y})')

    def start_monitoring(self):
        if self.listener is None:
            self.listener = mouse.Listener(on_click=self._on_click)
            self.listener.start()
            self._is_running = True
            print("Mouse monitoring started...")
        else:
            print("Monitoring is already active.")

    def stop_monitoring(self):
        if self.listener and self._is_running:
            print("Stopping mouse monitoring...")
            self.listener.stop()
            self._is_running = False
            print("Mouse monitoring stopped.")
        else:
            print("Monitoring was not active.")

    def join(self):
        if self.listener and self._is_running:
            self.listener.join()


if __name__ == "__main__":
    monitor = MouseClickMonitor()
    monitor.start_monitoring()
    print("Monitoring mouse clicks... Press Ctrl+C to stop.")
    try:
        while monitor._is_running:  # Keep the main thread running until stopped
            time.sleep(0.1)  # Check periodically
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping monitoring...")
        monitor.stop_monitoring()
        print("Monitoring stopped.")
