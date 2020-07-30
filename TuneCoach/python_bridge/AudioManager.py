from ctypes import *
import threading
from TuneCoach.python_bridge.pitch_utilities import *
from TuneCoach.python_bridge.SessionData import *
from TuneCoach.pitch_detection import TunerStream
from time import sleep

def read(stream, emit):
    while (stream.is_alive()):
        response, success = stream.read()
        if success and response:
            hz = response
            emit(hz)
        sleep(.01)

class AudioManager(TunerStream):
    def __init__(self, session, emit):
        super().__init__(44100)
        
        self._background_audio = threading.Thread(target=lambda: self.mainloop(), daemon=True)
        self._background_audio.start()
        self._background_reader = threading.Thread(target=lambda: read(self, emit))
        self._background_reader.start()

    def destroy(self):
        self.kill()

    @property
    def paused(self):
        return self.is_paused()