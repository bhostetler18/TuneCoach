from ctypes import *
import threading
from python_bridge.pitch_utilities import *
from python_bridge.FeedbackSystem import *
from pitch_detection import TunerStream
from multiprocessing import Process

def load_library():
    lib = cdll.LoadLibrary("./libPitchDetection.so")
    lib.create_stream.argtypes = [c_int]
    lib.create_stream.restype = c_void_p
    lib.mainloop.argtypes = [c_void_p]
    lib.pause_stream.argtypes = [c_void_p]
    lib.resume_stream.argtypes = [c_void_p]
    lib.kill_stream.argtypes = [c_void_p]
    lib.is_alive.argtypes = [c_void_p]
    lib.is_alive.restype = c_bool
    lib.is_paused.argtypes = [c_void_p]
    lib.is_paused.restype = c_bool
    lib.read_stream.restype = c_bool
    lib.read_stream.argtypes = [c_void_p, POINTER(c_double)]
    lib.peek_stream.argtypes = [c_void_p]
    lib.peek_stream.restype = c_double
    return lib


class AudioThread(threading.Thread):
    def __init__(self, stream):
        super().__init__()
        self._stream = stream
        # self.daemon = True
      
    def run(self):
        print("Starting background audio thread")
        self._stream.mainloop()
        print("Exited background audio thread")


class Reader(threading.Thread):
    def __init__(self, stream, session):
        super().__init__()
        self._stream = stream
        # self.daemon = True
        self.session = session
      
    def run(self):
        print("Starting reader")
        while(self._stream.is_alive()):
            response, success = self._stream.read()
            if success and response:
                hz = response
                self.session.collect_data(hz)
        print("Reader stopped")


class AudioManager(TunerStream):
    def __init__(self, session):
        super().__init__(44100)
        self._background_audio = threading.Thread(target = lambda: self.mainloop())
        self._background_audio.start()
        self._background_reader = Reader(self, session)
        self._background_reader.start()

    def destroy(self):
        self.kill()
        print("Successfully killed audio stream")
