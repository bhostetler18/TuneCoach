
from threading import Thread, Lock, Event
from subprocess import Popen, PIPE
from queue import Queue, Empty

class PitchDetector(Thread):
    def __init__(self):
        super().__init__()
        self.notes = []
        self.notes_lock = Lock()
        self.running = Event()
    def run(self):
        with Popen(["./PitchDetection/PitchDetection"], stdout=PIPE) as proc:
            while not self.running.is_set():
                if proc.stdout.readable():
                    line = proc.stdout.read()
                    with self.notes_lock:
                        self.notes.append(line)
                print("got line!")
    def stop(self):
        print("stopping")
        self.running.set()
