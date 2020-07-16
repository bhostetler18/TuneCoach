from datetime import datetime
import time

# Big thanks to https://stackoverflow.com/questions/60026296/how-to-make-a-pausable-timer-in-python


class Timer:
    def __init__(self):
        print("Initializing Timer")
        self.started = None
        self.paused = None
        self.is_paused = False

    def start(self):
        print("Starting Timer")
        self.started = datetime.now()

    def pause(self):
        if self.started is None:
            print("PAUSE: Timer not started")
        if self.is_paused:
            print("Already paused")
        print("Pausing Timer")
        self.paused = datetime.now()
        self.is_paused = True

    def resume(self):
        if self.started is None:
            print("RESUME: Timer not started")
        if not self.is_paused:
            print("Timer is not paused")
        print("Resuming Timer")

        pause_time = datetime.now() - self.paused
        self.started += pause_time
        self.is_paused = False

    def get(self):
        print("Getting value")
        if self.started is None:
            print("GET: Timer not started")
        if self.is_paused:
            return self.paused - self.started
        else:
            return datetime.now() - self.started

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
