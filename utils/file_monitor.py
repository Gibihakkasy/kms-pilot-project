import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class PDFChangeHandler(FileSystemEventHandler):
    """Handles file system events for PDF files."""
    def __init__(self, callback):
        self.callback = callback
        self.last_triggered = 0
        self.debounce_period = 5 # seconds

    def on_any_event(self, event):
        """
        Catches all events and triggers the callback for relevant PDF changes.
        """
        # Ignore directory events and non-PDF files
        if event.is_directory or not event.src_path.lower().endswith('.pdf'):
            return

        # Debounce to avoid multiple rapid triggers for a single file save
        current_time = time.time()
        if current_time - self.last_triggered < self.debounce_period:
            logging.info(f"Debouncing event for {os.path.basename(event.src_path)}")
            return

        if event.event_type in ['created', 'modified']:
            logging.info(f"Detected change in {os.path.basename(event.src_path)}. Triggering re-indexing.")
            self.last_triggered = current_time
            self.callback()

class DocumentMonitor:
    """Monitors a directory for document changes."""
    def __init__(self, path, callback):
        self.observer = Observer()
        self.path = path
        self.event_handler = PDFChangeHandler(callback=callback)

    def start(self):
        """Starts the monitoring in a non-blocking way."""
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()
        logging.info(f"Started monitoring directory: {self.path}")

    def stop(self):
        """Stops the monitoring."""
        self.observer.stop()
        self.observer.join()
        logging.info("Stopped monitoring directory.")

if __name__ == '__main__':
    # Example usage:
    # This part is for testing the monitor independently.
    import sys
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)
    
    from embeddings.vector_store import create_and_save_vector_store

    DOCUMENTS_DIR = os.path.join(project_root, 'documents')
    
    print(f"Watching directory: {DOCUMENTS_DIR}")
    print("Add or modify a PDF file in the directory to test. Press Ctrl+C to stop.")

    # Create and start the monitor
    monitor = DocumentMonitor(path=DOCUMENTS_DIR, callback=create_and_save_vector_store)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
        print("\nMonitoring stopped.")
