from tkinter import *
from tkinter.font import Font
from math import sin, cos, radians
import sys
sys.path.insert(1, '../python_bridge')
from ctypes import *
import threading
from constants import Colors
from pitch_utilities import *
from math import sin, cos, radians
import time

class PitchDisplay:
    def __init__(self, grandparent, frame, manager, threshold=15):
        self.grandparent = grandparent
        self.frame = frame
        self.audio_manager = manager

        self.font = Font(size=20)
        self.pitchOffset = self.font.metrics('linespace')/2

        self._pitchValue = '---' # default display
        self._centsValue = -50
        self._hertzValue = 0

        self._span = 75 #size of tuner arc in degrees, starting at vertical 

        self.canvas = Canvas(frame)
        self.canvas.pack(fill = BOTH, expand = True)
        self.canvas.bind("<Configure>", self.configure)

        self._last_time = 0
        self._clearing = False

        self.display_default_gui()
        self.display_current_gui()

    def cents_to_angle(self, cents):
        return cents/50 * self._span

    def configure(self, event):
        self.display_default_gui()


    def display_current_gui(self):
        self.canvas.itemconfig(self.current_pitch_display, text=self._pitchValue)
        deg = self.cents_to_angle(self._centsValue)
        self.update_line(deg)
        if not self._clearing and abs(deg) <= 15:
            self.canvas.itemconfig(self.green_bg, fill="green")
        else:
            self.canvas.itemconfig(self.green_bg, fill="#ccffbf")

        
    def display_default_gui(self):
        self.canvas.delete("all")
        self.frame.update()
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()
        min_dimension = min(self.width, self.height)
        self.radius = 0.4 * min_dimension
        self.centerX = self.width/2
        self.centerY = self.height/2

        self.current_pitch_display = self.canvas.create_text(self.width/2, self.height/2 + self.pitchOffset, font=self.font, text='---')
        #left_red_bg = self.canvas.create_arc(self.centerX - self.radius, self.centerY - self.radius, self.centerX + self.radius, self.centerY + self.radius)
        #self.canvas.itemconfig(left_red_bg, start=0, width=5, fill="black", extent=180, outline='')
        x0 = self.centerX - self.radius
        y0 = self.centerY - self.radius
        x1 = self.centerX + self.radius
        y1 = self.centerY + self.radius

        #rect = self.canvas.create_rectangle(x0, y0, x1, y1)
        d1 = 90 - self._span
        d2 = 0
        d3 = 0
        d4 = 0
        d5 = 0
        d6 = 90 + self._span

        self.left_red_bg = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.left_red_bg, start=150, width=5, fill="#ffbfbf", extent=15, outline='')

        self.left_yellow_bg = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.left_yellow_bg,  start=105, width=5, fill="#fffeb0", extent=45, outline='')

        self.green_bg = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.green_bg, start=75, width=5, fill="#ccffbf", extent=30, outline='')

        self.right_yellow_bg = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.right_yellow_bg, start=30, width=5, fill="#fffeb0", extent=45, outline='')

        self.right_red_bg = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.right_red_bg, start = 90-self._span, width=5, fill="#ffbfbf", extent=15, outline='')

        self.line = self.canvas.create_line(self.centerX, self.centerY, self.centerX, self.centerY - self.radius, fill="#452A23", width=4, 
                                            arrow=FIRST, arrowshape=(self.radius,10,5))

    def update_line(self, degrees):
        theta = radians(degrees)
        dx = self.radius * sin(theta)
        dy = self.radius * cos(theta)
        self.canvas.coords(self.line, self.centerX, self.centerY, self.centerX + dx, self.centerY - dy)


    def update_pitch(self, value): # event as parameter
        self._pitchValue = value

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self, value):
        self._centsValue = value

    def update_data(self): #event
        hz = self.audio_manager.peek()
        if hz != 0:
            self._clearing = False
            midi = hz_to_midi(hz)
            pitch_class = midi_to_pitch_class(midi)
            desired_hz = closest_in_tune_frequency(hz)
            cent = cents(desired_hz, hz)
            name = pitch_class_to_name(pitch_class, Accidental.SHARP)
            self.update_cents(cent)
            self.update_hertz()
            self.update_pitch(name)
            self.display_current_gui()
            self._last_time = time.time()
        else:
            self._clearing = True
            if self._centsValue != -50 and time.time() - self._last_time > 1.5:
                self.update_cents(max(-50,self._centsValue - 3))
                self.update_pitch('---')
                self.display_current_gui()


        self.grandparent.after(10, self.update_data)