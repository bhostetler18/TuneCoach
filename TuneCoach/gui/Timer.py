from datetime import datetime
import time

# Big thanks to https://stackoverflow.com/questions/60026296/how-to-make-a-pausable-timer-in-python


class Timer:
    def __init__(self):
        print("Initializing")
        self.started = None
        self.paused = None
        self.is_paused = False

    def start(self):
        print("Starting")
        self.started = datetime.now()

    def pause(self):
        if self.started is None:
            print("PAUSE: Timer not started")
        if self.is_paused:
            print("Already paused")
        print("Pausing")
        self.paused = datetime.now()
        self.is_paused = True

    def resume(self):
        if self.started is None:
            print("RESUME: Timer not started")
        if not self.is_paused:
            print("Timer is not paused")
        print("Resuming")

        pause_time = datetime.now() - self.paused
        self.started += pause_time
        self.is_paused = False

    def get(self):
        if self.started is None:
            print("GET: Timer not started")
        if self.is_paused:
            return int((self.paused - self.started).total_seconds())
        else:
            return int((datetime.now() - self.started).total_seconds())

    def clear(self):
        print("Clearing")
        self.started = None
        self.paused = None
        self.is_paused = False

    def has_started(self):
        if self.started is None:
            return False
        else:
            return True
