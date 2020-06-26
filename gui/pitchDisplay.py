from tkinter import *
from tkinter.font import Font
from math import sin, cos, radians
import sys
sys.path.insert(1, '../python_bridge')
from ctypes import *
import threading
from pitch_utilities import *

class PitchDisplay:
    def __init__(self, grandparent, master, manager, pitch=None, hertz=None, cents=None):
        self.grandparent = grandparent
        self.master = master
        self.audio_manager = manager
        self.right_red = None
        self.right_yellow = None
        self.green = None
        self.left_red = None
        self.left_yellow = None
        self.font = Font(size=20)
        self.pitchOffset = self.font.metrics('linespace')/2
        if not pitch:
            self._pitchValue = '---' # default display
        else:
            self._pitchValue = pitch

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
        #
        # self.title = 'Pitch Information'
        # self.label = Label(master, text="Hello World")

        self.screen_width = (4/7) * master.winfo_screenwidth()
        self.screen_height = (1/2) * master.winfo_screenheight()

        self.canvas = Canvas(master, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        self.current_pitch_display = self.canvas.create_text(self.screen_width/2, self.screen_height/2 + self.pitchOffset, font=self.font, text='---')

        self.display_default_gui()

    def display_current_gui(self):
        temp = (self._default_cents_bound/2) - self._centsValue
        offset = (temp / self._default_cents_bound) * 90 #90 degrees, 45 offset from start +x
        startValue = offset + 45
        extentValue = 90 - offset

        self.canvas.itemconfig(self.current_pitch_display, text=self._pitchValue)

        self.canvas.itemconfig(self.left_red, start=0, extent=0)
        self.canvas.itemconfig(self.left_yellow, start=0, extent=0)
        self.canvas.itemconfig(self.green, start=0, extent=0)
        self.canvas.itemconfig(self.right_yellow, start=0, extent=0)
        self.canvas.itemconfig(self.right_red, start=0, extent=0)

        if startValue > 120:
            self.canvas.itemconfig(self.left_red, start=startValue, extent=extentValue)
        elif startValue > 95:
            self.canvas.itemconfig(self.left_red, start=120, extent=15)
            self.canvas.itemconfig(self.left_yellow, start=startValue, extent=extentValue-15)
        elif startValue > 85:
            self.canvas.itemconfig(self.left_red, start=120, extent=15)
            self.canvas.itemconfig(self.left_yellow, start=95, extent=25)
            self.canvas.itemconfig(self.green, start=startValue, extent=extentValue-40)
        elif startValue > 60:
            self.canvas.itemconfig(self.left_red, start=120, extent=15)
            self.canvas.itemconfig(self.left_yellow, start=95, extent=25)
            self.canvas.itemconfig(self.green, start=85, extent=10)
            self.canvas.itemconfig(self.right_yellow, start=startValue, extent=extentValue-50)
        elif startValue > 45:
            self.canvas.itemconfig(self.left_red, start=120, extent=15)
            self.canvas.itemconfig(self.left_yellow, start=95, extent=25)
            self.canvas.itemconfig(self.green, start=85, extent=10)
            self.canvas.itemconfig(self.right_yellow, start=60, extent=25)
            self.canvas.itemconfig(self.right_red, start=startValue, extent=extentValue-75)

    def display_default_gui(self):
        left_red_bg = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_red_bg, start=120, width=5, fill="#ffbfbf", extent=15, outline='')

        left_yellow_bg = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_yellow_bg,  start=95, width=5, fill="#fffeb0", extent=25, outline='')

        green_bg = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(green_bg, start=85, width=5, fill="#ccffbf", extent=10, outline='')

        right_yellow_bg = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(right_yellow_bg, start=60, width=5, fill="#fffeb0", extent=25, outline='')

        right_red_bg = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.itemconfig(right_red_bg, start=45, width=5, fill="#ffbfbf", extent=15, outline='')

        self.left_red = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.left_yellow = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.green = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.right_yellow = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.right_red = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(self.left_red, fill='red', start=0, outline='', extent=0)
        self.canvas.itemconfig(self.left_yellow, fill='yellow', start=0, outline='', extent=0)
        self.canvas.itemconfig(self.green, fill='green', start=0, outline='', extent=0)
        self.canvas.itemconfig(self.right_yellow, fill='yellow', start=0, outline='', extent=0)
        self.canvas.itemconfig(self.right_red, fill='red', start=0, outline='', extent=0)

    def update_pitch(self, value): # event as parameter
        self._pitchValue = value

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self, value):
        self._centsValue = value # perfectly in tune hardcoded - str(event.char)

    def update_data(self): #event
        hz = self.audio_manager.peek()
        if hz != 0:
            midi = hz_to_midi(hz)
            pitch_class = midi_to_pitch_class(midi)
            desired_hz = closest_in_tune_frequency(hz)
            cent = cents(desired_hz, hz)
            name = pitch_class_to_name(pitch_class, Accidental.SHARP)
            self.update_cents(cent)
            self.update_hertz()
            self.update_pitch(name)
            self.display_current_gui()

        self.grandparent.after(10, self.update_data)