from tkinter import *
from math import sin, cos, radians
import sys
sys.path.insert(1, '../python_bridge')
from ctypes import *
import threading
from pitch_utilities import *

class PitchDisplay:
    def __init__(self, master, pitch=None, hertz=None, cents=None):
        self.right_red = None
        self.right_yellow = None
        self.green = None
        self.left_red = None
        self.left_yellow = None
        if not pitch:
            self._pitchValue = 'C' # default display
            self.current_pitch_display = 'C'
        else:
            self._pitchValue = pitch
            self.current_pitch_display = 'C'

        if not hertz:
            self._hertzValue = 261.625565 # middle C - hardcodedstr(event.char)
        else:
            self._hertzValue = hertz

        if not cents:
            self._centsValue = 0
        else:
            self._centsValue = cents

        self._default_cents_bound = 100 # 50 cents below and above is allowed
        super().__init__()
        self.frame = Frame(master)
        self.frame.pack()

        self.title = 'Pitch Information'
        self.label = Label(master, text="Hello World")
        self.label.pack()

        self.screen_width = (4/7) * master.winfo_screenwidth()
        self.screen_height = (1/2) * master.winfo_screenheight()
        # master.geometry(f'{self.screen_width}x{self.screen_height}')

        self.canvas = Canvas(master, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        # print(master.winfo_screenheight(), master.winfo_screenwidth())

        self.display_default_gui()
        # self.current_needle_display = self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=self._pitchValue)
        self.display_current_gui()

    def display_current_gui(self):
        self.canvas.delete(self.left_red)
        self.canvas.delete(self.left_yellow)
        self.canvas.delete(self.green)
        self.canvas.delete(self.right_yellow)
        self.canvas.delete(self.right_red)

        temp = (self._default_cents_bound/2) - self._centsValue
        offset = (temp / self._default_cents_bound) * 90 #90 degrees, 45 offset from start +x
        startValue = offset + 45
        extentValue = 90 - offset

        self.canvas.delete(self.current_pitch_display)
        self.current_pitch_display = self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=self._pitchValue)

        if startValue > 120:
            self.left_red = self.canvas.create_arc(self.screen_width/4,self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
            self.canvas.itemconfig(self.left_red, fill='red', start=startValue, outline='',extent = extentValue)
        elif startValue > 95:
            self.left_red = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                   3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_red, fill='red', start=120, outline='', extent=15)
            self.left_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                   3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_yellow, fill='yellow', start=startValue, outline='', extent=extentValue-15)
        elif startValue > 85:
            self.left_red = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                   3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_red, fill='red', start=120, outline='', extent=15)
            self.left_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                      3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_yellow, fill='yellow', start=95, outline='', extent=25)
            self.green = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                      3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.green, fill='green', start=startValue, outline='', extent=extentValue-40)
        elif startValue > 60:
            self.left_red = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                   3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_red, fill='red', start=120, outline='', extent=15)
            self.left_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                      3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_yellow, fill='yellow', start=95, outline='', extent=25)
            self.green = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.green, fill='green', start=85, outline='', extent=10)
            self.right_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.right_yellow, fill='yellow', start=startValue, outline='', extent=extentValue-50)
        elif startValue > 45:
            self.left_red = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                   3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_red, fill='red', start=120, outline='', extent=15)
            self.left_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                      3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.left_yellow, fill='yellow', start=95, outline='', extent=25)
            self.green = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.green, fill='green', start=85, outline='', extent=10)
            self.right_yellow = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                       3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.right_yellow, fill='yellow', start=60, outline='',
                                   extent=25)
            self.right_red = self.canvas.create_arc(self.screen_width / 4, self.screen_height / 4,
                                                3 * self.screen_width / 4, 3 * self.screen_height / 4)
            self.canvas.itemconfig(self.right_red, fill='red', start=startValue, outline='', extent=extentValue-75)

    def display_default_gui(self):
        pitch_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(pitch_arc, fill="lightgrey", style=PIESLICE, stipple="gray25", start=45, outline='')

        left_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_red_arc, start=120, width=5, fill="#ffbfbf", extent=15, outline='')

        left_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_yellow_arc,  start=95, width=5, fill="#fffeb0", extent=25, outline='')

        green_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(green_arc, start=85, width=5, fill="#ccffbf", extent=10, outline='')

        right_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(right_yellow_arc, start=60, width=5, fill="#fffeb0", extent=25, outline='')

        right_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.itemconfig(right_red_arc, start=45, width=5, fill="#ffbfbf", extent=15, outline='')

    def update_pitch(self, value): # event as parameter
        self._pitchValue = value

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self, value):
        self._centsValue = value # perfectly in tune hardcoded - str(event.char)

    def update_data(self, handle, lib): #event
        response = c_double()
        success = lib.read_stream(handle, byref(response))
        if success and response:
            hz = response.value
            midi = hz_to_midi(hz)
            pitch_class = midi_to_pitch_class(midi)
            desired_hz = closest_in_tune_frequency(hz)
            cent = cents(desired_hz, hz)
            name = pitch_class_to_name(pitch_class, Accidental.SHARP)
            self.update_cents(cent)
            self.update_hertz()
            self.update_pitch(name)
            self.display_current_gui()

        root.after(10, self.update_data, handle, lib)

def load_library():
    lib = cdll.LoadLibrary("../python_bridge/libPitchDetection.so")
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

# if __name__ == "__main__":
#     root = Tk()
#     root.title("TuneCoach")
#     pitch = PitchDisplay(root)
#
#     lib = load_library()
#     handle = lib.create_stream(44100)
#     audio = AudioThread(handle, lib)
#     audio.start()
#     root.after(10, pitch.update_data, handle, lib)
#     root.mainloop()
