from ctypes import *
import threading

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
            val = c_double()
            res = lib.read_stream(handle, byref(val))
            if res and val:
                print(val)


if __name__ == "__main__":
    lib = load_library()
    handle = lib.create_stream(44100)
    audio = AudioThread(handle, lib)
    reader = Reader(handle, lib)
    audio.start()
    reader.start()