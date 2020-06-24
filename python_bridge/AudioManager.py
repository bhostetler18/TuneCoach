from ctypes import *
import threading
from pitch_utilities import *
from FeedbackSystem import *


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
        self._handle = handle
        self._lib = lib
        self.daemon = True
      
    def run(self):
        print("Starting reader")
        while(True):
            response = c_double()
            success = self._lib.read_stream(self._handle, byref(response))
            if success and response:
                hz = response.value
                self.handle_data(hz)

    def handle_data(self, hz):
        midi = hz_to_midi(hz) 
        pitch_class = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        name = pitch_class_to_name(pitch_class, Accidental.SHARP)
        print(f"{name}: {round(hz, 2)} Hz ({round(cent)} cents)")


#Change how incoming data is dealt with in handle_data
class ExampleCustomReader(Reader):
    def __init__(self, handle, lib):
        super().__init__(handle, lib) 

    def handle_data(self, hz):
        print(hz)


class AudioManager:
    def __init__(self):
        self._lib = load_library()
        self._handle = self._lib.create_stream(44100)
        self._background_audio = AudioThread(self._handle, self._lib)
        self._background_reader = ExampleCustomReader(self._handle, self._lib)
        self.daemon = True

    def start_capture(self):
        self._background_audio.start()

    def start_reader(self):
        self._background_reader.start()

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
