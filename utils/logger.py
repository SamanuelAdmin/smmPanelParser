import sys
from datetime import datetime


class ConsoleOutputLogger:
    def __init__(self, LoggerBuffer):
        self.LoggerBuffer = LoggerBuffer

        self._stdout = sys.stdout
        self._stderr = sys.stderr

    def start(self):
        sys.stdout = self
        sys.stderr = self

    def stop(self):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def write(self, message):
        self.LoggerBuffer.info(f'[{str(datetime.now())[:-4]}] {message}' if len(message) > 2 else str(message))

    def flush(self): pass