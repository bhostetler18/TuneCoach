from datetime import datetime
import time

# Big thanks to https://stackoverflow.com/questions/60026296/how-to-make-a-pausable-timer-in-python


class Timer:
    def __init__(self):
        self.started = None
        self.paused = None
        self.is_paused = False

    def start(self):
        self.started = datetime.now()

    def pause(self):
        self.paused = datetime.now()
        self.is_paused = True

    def resume(self):
        pause_time = datetime.now() - self.paused
        self.started += pause_time
        self.is_paused = False

    def get(self):
        if self.is_paused:
            return int((self.paused - self.started).total_seconds())
        else:
            return int((datetime.now() - self.started).total_seconds())

    def clear(self):
        self.started = None
        self.paused = None
        self.is_paused = False

    def has_started(self):
        if self.started is None:
            return False
        else:
            return True
