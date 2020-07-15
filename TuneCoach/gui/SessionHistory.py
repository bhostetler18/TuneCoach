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

        self.scrollbar = tk.Scrollbar(workingFrame, orient=tk.HORIZONTAL)
        self.scrollbar.pack(side='bottom', fill='x')
        self.scrollbar.config(command=self.scroll)
        self.scrollbar_width = 1
        self.scrollbar.set(1 - self.scrollbar_width, 1)
        self.buffer = []

        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()

        self.aspect_ratio = 580/820
        self.piano = Piano(self.canvas, width=50, height=90)
        self.piano.pack(side='bottom', expand=True, fill='y', anchor='w')

        self.available_width = self.width
        self.circle_size = self.available_width/65
        self.circle_start = 0
        self.circle_list = [None] * 64  # TODO: don't hardcode size and coordinate with Feedback buffer

        self.frame.bind("<Configure>", self.setup)

    def scroll(self, *args):
        if args[0] == 'moveto':
            offset = max(0, min(float(args[1]), 1 - self.scrollbar_width))
            self.scrollbar.set(offset, offset + self.scrollbar_width)
            start = int(len(self.buffer) * offset)
            self.display_previous(start)
        if args[0] == 'update_width':
            self.scrollbar.set(1 - self.scrollbar_width, 1)



    def setup(self, event): # TODO: fix bug where resizing window removes current data from display
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
            "B": self.height / 14,
            "A#": self.height / 7,
            "A": self.height / 14 * 3,
            "G#": self.height / 7 * 2,
            "G": self.height / 14 * 5,
            "F#": self.height / 7 * 3,
            "F": self.height / 14 * 7,
            "E": self.height / 14 * 9,
            "D#": self.height / 7 * 5,
            "D": self.height / 14 * 11,
            "C#": self.height / 7 * 6,
            "C": self.height / 14 * 13
        }

        for note in self.noteDict:
            self.canvas.create_line(piano_width, self.noteDict[note], self.width, self.noteDict[note], width=3)


    def update(self, data, force=False):
        if data is not None and (force or data.has_new_data):
            data.has_new_data = False
            recent = list(data.display_buffer)
            self.buffer.append(recent[-1]) # TODO: use note_history, replace note names with integral values
            self.scrollbar_width = 1/(max(1, len(self.buffer)/64))
            self.scroll('update_width')
            pitch_errors = [(100.0 * data._in_tune_count[i]) / (data._pitch_count[i] if data._pitch_count[i] != 0 else 1) for i in range(0,12)]
            self.piano.set_scores(pitch_errors)
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

    def display_previous(self, start):
        # TODO: make sure paused
        self.clear()
        recent = self.buffer[start : start+64]
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
