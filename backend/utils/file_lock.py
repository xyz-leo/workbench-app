# backend/utils/file_lock.py

"""
Simple file-based lock to avoid concurrent writes.
"""

import time
import os

class FileLock:
    def __init__(self, filepath, timeout=5, delay=0.1):
        self.filepath = filepath + ".lock"
        self.timeout = timeout
        self.delay = delay

    def acquire(self):
        start_time = time.time()
        while True:
            try:
                # Cria o arquivo lock; falha se já existir
                self.fd = os.open(self.filepath, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                return
            except FileExistsError:
                if (time.time() - start_time) >= self.timeout:
                    raise TimeoutError(f"Could not acquire lock on {self.filepath}")
                time.sleep(self.delay)

    def release(self):
        os.close(self.fd)
        os.remove(self.filepath)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

