import time
import logging

class PerformanceTracker:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        logging.info(f"⏱️ Processing time: {end - self.start:.2f} seconds")
