from tkinter import *
from tkinter.font import Font
import tkinter.ttk as ttk
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
    def __init__(self, parent, frame, manager, threshold=10):
        self.parent = parent
        self.frame = frame
        self.audio_manager = manager

        self.threshold = threshold

        self.font = Font(size=20)
        self.pitchOffset = self.font.metrics('linespace')/2

        self._pitchValue = '---' # default display
        self._centsValue = -50
        self._hertzValue = 0

        self._span = 75 # Size of tuner arc in degrees, starting at vertical

        self.canvas = Canvas(frame)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Configure>", self.configure)

        self.showsHertz = BooleanVar()

        c = ttk.Checkbutton(self.canvas, text="Show Hertz", variable=self.showsHertz, takefocus=False, command=self.display_default_gui)
        c.pack(anchor='e', side='bottom')

        self._last_time = 0
        self._clearing = False

        self.display_default_gui()
        self.update_data()

    def cents_to_angle(self, cents):
        return cents/50 * self._span

    def configure(self, event):
        self.display_default_gui()

    def display_current_gui(self):
        self.canvas.itemconfig(self.current_pitch_display, text=self._pitchValue)
        if self.showsHertz.get():
            self.canvas.itemconfig(self.hertzDisplay, text=self._hertzValue)
        self.update_line(self._centsValue)
        if not self._clearing and abs(self._centsValue) <= self.threshold:
            self.canvas.itemconfig(self.green_arc, fill="green")
        else:
            self.canvas.itemconfig(self.green_arc, fill="#ccffbf")

    def display_default_gui(self):
        self.canvas.delete("all")
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()
        min_dimension = min(self.width, self.height)
        self.radius = 0.4 * min_dimension
        self.centerX = self.width/2
        self.centerY = self.height/2

        self.current_pitch_display = self.canvas.create_text(self.width/2, self.height/2 + self.pitchOffset, font=self.font, text='---')
        if self.showsHertz.get():
            self.hertzDisplay = self.canvas.create_text(self.width/2, self.height/2 + 3*self.pitchOffset, font=(None, 14), text='')

        x0 = self.centerX - self.radius
        y0 = self.centerY - self.radius
        x1 = self.centerX + self.radius
        y1 = self.centerY + self.radius

        #rect = self.canvas.create_rectangle(x0, y0, x1, y1)

        rStart = 90 - self._span
        rSpan = 2 * self._span
        yStart = rStart + 20
        ySpan = 2 * (90 - yStart)
        gStart = 90 - self.cents_to_angle(self.threshold)
        gSpan = 2 * self.cents_to_angle(self.threshold)

        self.red_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.red_arc, start=rStart, fill="#ffbfbf", extent=rSpan, outline='')

        self.yellow_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.yellow_arc,  start=yStart, fill="#fffeb0", extent=ySpan, outline='')

        self.green_arc = self.canvas.create_arc(x0, y0, x1, y1)
        self.canvas.itemconfig(self.green_arc, start=gStart, fill="#ccffbf", extent=gSpan, outline='')


        self.line = self.canvas.create_line(0, 0, 0, 0, fill="#452A23", width=4, 
                                            arrow=FIRST, arrowshape=(self.radius,10,5))
        self.update_line(-50)


    def update_line(self, cents):
        deg = self.cents_to_angle(cents)
        theta = radians(deg)
        dx = self.radius * sin(theta)
        dy = self.radius * cos(theta)
        self.canvas.coords(self.line, self.centerX, self.centerY, self.centerX + dx, self.centerY - dy)

    def set_threshold(self, thresh):
        self.threshold = thresh
        self.display_default_gui()

    def update_pitch(self, value): # event as parameter
        self._pitchValue = value

    def update_hertz(self, value):
        self._hertzValue = value

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
            name = pitch_class_to_name(pitch_class, Accidental.SHARP) #TODO: coordinate accidental with FeedbackManager
            self.update_cents(cent)
            self.update_hertz(f"{round(hz)} Hz")
            self.update_pitch(name)
            self.display_current_gui()
            self._last_time = time.time()
        else:
            self._clearing = True
            if self._centsValue != -50 and time.time() - self._last_time > 1.5:
                self.update_cents(max(-50,self._centsValue - 3))
                self.update_pitch('---')
                self.update_hertz('')
                self.display_current_gui()


        self.parent.after(10, self.update_data)