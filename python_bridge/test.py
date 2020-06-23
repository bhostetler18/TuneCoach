from ctypes import *
import threading
from pitch_utilities import *

def load_library():
    lib = cdll.LoadLibrary("./libPitchDetection.so")
    lib.create_stream.argtypes = [c_int]
    lib.create_stream.restype = c_void_p
    lib.pause_stream.argtypes = [c_void_p]
    lib.resume_stream.argtypes = [c_void_p]
    lib.kill_stream.argtypes = [c_void_p]
    lib.is_alive.argtypes = [c_void_p]
    lib.is_alive.restype = c_bool
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
      
    def run(self):
        print("Starting")
        self.lib.start_stream(self.handle)

class Reader(threading.Thread):
    def __init__(self, handle, lib):
        super().__init__()
        self.handle = handle
        self.lib = lib
      
    def run(self):
        print("Starting")
        while(True):
            response = c_double()
            success = lib.read_stream(handle, byref(response))
            if success and response:
                hz = response.value
                midi = hz_to_midi(hz) 
                pitch_class = midi_to_pitch_class(midi)
                desired_hz = closest_in_tune_frequency(hz)
                cent = cents(desired_hz, hz)
                name = pitch_class_to_name(pitch_class, Accidental.SHARP)
                print(f"{name}: {round(hz, 2)} Hz ({round(cent)} cents)")

if __name__ == "__main__":
    lib = load_library()
    handle = lib.create_stream(44100)
    audio = AudioThread(handle, lib)
    reader = Reader(handle, lib)
    audio.start()
    reader.start()
