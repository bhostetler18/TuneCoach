import tkinter as tk
import TuneCoach.gui as gui
from TuneCoach.gui.Piano import Piano


# Different classes for pop-up windows.
class SessionHistory:
    def create_circle(self, x, y, r, canvasName, fillColor):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, fill=fillColor)

    def __init__(self, mainWindow, workingFrame):
        self.mainWindow = mainWindow
        self.frame = workingFrame
        self.canvas = tk.Canvas(workingFrame, bg="#bdd0df")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()

        self.aspect_ratio = 580/820
        self.piano = Piano(self.canvas, width=50, height=90)
        self.piano.pack(side='left', expand=True, fill='y', anchor='w')

        self.available_width = self.width
        self.circle_size = self.available_width/65
        self.circle_start = 0
        self.circle_list = [None] * 64  # TODO: don't hardcode size and coordinate with Feedback buffer

        self.frame.bind("<Configure>", self.setup)


    def setup(self, event):
        self.clear()
        self.canvas.delete("all")

        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height() - 10  # Subtract 10 because MainWindow sets bd=5

        piano_width = self.height*self.aspect_ratio
        self.piano.configure(width=piano_width)
            
        self.available_width = self.width - piano_width
        self.circle_start = piano_width
        self.circle_size = 0.5*self.available_width/64
        
        self.noteDict = {
            "C": self.height / 14,
            "C#": self.height / 7,
            "D": self.height / 14 * 3,
            "D#": self.height / 7 * 2,
            "E": self.height / 14 * 5,
            "F": self.height / 14 * 7,
            "F#": self.height / 7 * 4,
            "G": self.height / 14 * 9,
            "G#": self.height / 7 * 5,
            "A": self.height / 14 * 11,
            "A#": self.height / 7 * 6,
            "B": self.height / 14 * 13
        }

        for note in self.noteDict:
            self.canvas.create_line(piano_width, self.noteDict[note], self.width, self.noteDict[note], width=3)


    def update(self, data, force=False):
        if data is not None and (force or data.has_new_data):
            data.has_new_data = False
            recent = list(data.display_buffer)
            for i, (note, cents) in enumerate(recent):
                color = "red"
                if abs(cents) <= self.mainWindow.threshold:
                    color = "green"
                elif abs(cents) <= self.mainWindow.yellow_threshold:
                    color = "yellow"

                circle = self.circle_list[i]
                x = self.circle_start + self.circle_size/2 + 2*self.circle_size*i
                y = self.noteDict[note]
                if circle is None:
                    c = self.create_circle(x, y, self.circle_size, self.canvas, color)
                    self.circle_list[i] = c
                else:
                    self.canvas.coords(circle, x - self.circle_size, y - self.circle_size, x + self.circle_size, y + self.circle_size)
                    self.canvas.itemconfig(circle, fill=color)

    def clear(self):
        for circle in self.circle_list:
            self.canvas.delete(circle)
        self.circle_list = [None] * 64
