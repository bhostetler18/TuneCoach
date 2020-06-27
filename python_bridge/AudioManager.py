from ctypes import *
import threading
from pitch_utilities import *
from FeedbackSystem import *


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
    def __init__(self, lib, handle):
        super().__init__()
        self._lib = lib
        self._handle = handle
        # self.daemon = True
      
    def run(self):
        print("Starting background audio thread")
        self._lib.mainloop(self._handle)
        print("Exited background audio thread")


class Reader(threading.Thread):
    def __init__(self, lib, handle, session):
        super().__init__()
        self._handle = handle
        self._lib = lib
        # self.daemon = True
        self.session = session
      
    def run(self):
        print("Starting reader")
        while(self._lib.is_alive(self._handle)):
            response = c_double()
            success = self._lib.read_stream(self._handle, byref(response))
            if success and response:
                hz = response.value
                self.session.collect_data(hz)
        print("Reader stopped")


class AudioManager:
    def __init__(self, session):
        self._lib = load_library()
        self._handle = self._lib.create_stream(44100)
        self._background_audio = AudioThread(self._lib, self._handle)
        self._background_audio.start()
        self._background_reader = Reader(self._lib, self._handle, session)
        self._background_reader.start()

    def resume(self):
        self._lib.resume_stream(self._handle)

    def pause(self):
        self._lib.pause_stream(self._handle)

    def is_paused(self):
        return self._lib.is_paused(self._handle)

    def peek(self):
        return self._lib.peek_stream(self._handle)

    def destroy(self):
        self._lib.kill_stream(self._handle)
        print("Successfully killed audio stream")
