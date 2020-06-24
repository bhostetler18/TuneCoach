from ctypes import *
import threading
from pitch_utilities import *
from feedback_system import *


def load_library():
    lib = cdll.LoadLibrary("./libPitchDetection.so")
    lib.create_stream.argtypes = [c_int]
    lib.create_stream.restype = c_void_p
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
    def __init__(self, handle, lib):
        super().__init__()
        self.handle = handle
        self.lib = lib
        self.daemon = True
      
    def run(self):
        print("Starting background audio thread")
        self.lib.start_stream(self.handle)


class Reader(threading.Thread):
    def __init__(self, handle, lib):
        super().__init__()
        self.handle = handle
        self.lib = lib

    def run(self):
        threshold = int(input("Please enter cents threshold: "))
        feedback_system(threshold)
        while(True):
            response = c_double()
            success = lib.read_stream(handle, byref(response))
            if success and response:
                hz = response.value
                feedback_system.collect_data(hz)


class AudioManager:
    def __init__(self):
        self._lib = load_library()
        self._handle = self._lib.create_stream(44100)
        self._background_audio = AudioThread(self._handle, self._lib)

    def start_capture(self):
        self._background_audio.start()

    def is_paused(self):
    	return self._lib.is_paused(self._handle)

    def pause(self):
        self._lib.pause_stream(self._handle)

    def resume(self):
        self._lib.resume_stream(self._handle)

    def peek(self):
        return self._lib.peek_stream(self._handle)

    def read(self):
        response = c_double()
        success = self._lib.read_stream(self._handle, byref(response))
        return success, response.value

    def destroy(self):
        self._lib.kill_stream(self._handle)
