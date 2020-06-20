from ctypes import *
import threading

def load_library():
    lib = cdll.LoadLibrary("./libPitchDetection.so")
    lib.peek_stream.restype = c_double
    lib.read_stream.restype = c_bool
    lib.read_stream.argtypes = [c_void_p, POINTER(c_double)]
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
            if res:
                print(val)


if __name__ == "__main__":
    lib = load_library()
    handle = lib.create_stream(44100)
    reader = Reader(handle, lib)
    reader.start()
    lib.start_stream(handle)