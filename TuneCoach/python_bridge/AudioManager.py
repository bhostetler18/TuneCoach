from ctypes import *
import threading
from TuneCoach.python_bridge.pitch_utilities import *
from TuneCoach.python_bridge.SessionData import *
from TuneCoach.pitch_detection import TunerStream
from time import sleep


class AudioThread(threading.Thread):
    def __init__(self, stream):
        super().__init__()
        self._stream = stream
        # self.daemon = True

    def run(self):
        # print("Starting background audio thread")
        self._stream.mainloop()
        # print("Exited background audio thread")


class Reader(threading.Thread):
    def __init__(self, stream, session):
        super().__init__()
        self._stream = stream
        # self.daemon = True
        if session is None:
            raise AttributeError('Session cannot be None!')
        self.session = session

    def run(self):
        # print("Starting reader")
        while (self._stream.is_alive()):
            response, success = self._stream.read()
            if success and response:
                hz = response
                self.session.collect_data(hz)
            sleep(.01)
        # print("Reader stopped")


class AudioManager(TunerStream):
    def __init__(self, session):
        super().__init__(44100)
        self._background_audio = threading.Thread(target=lambda: self.mainloop())
        self._background_audio.start()
        self._background_reader = Reader(self, session)
        self._background_reader.start()

    def destroy(self):
        self.kill()

    @property
    def paused(self):
        return self.is_paused()