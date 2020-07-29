import tkinter as tk
import tkinter.ttk as ttk
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

        self.display_size = 64
        self.current_pos = 0

        self.scrollbar = ttk.Scrollbar(workingFrame, orient=tk.HORIZONTAL)
        self.scrollbar.pack(side='bottom', fill='x')
        self.scrollbar.config(command=self.scroll)
        self.scrollbar_width = 1
        self.scrollbar.set(1 - self.scrollbar_width, 1)
        self.buffer = []

        self.aspect_ratio = 580/820
        self.piano = Piano(self.canvas, self.mainWindow, width=50, height=90)
        self.piano.pack(side='bottom', expand=True, fill='y', anchor='w')

        self.circle_size = 5
        self.circle_start = 0
        self.circle_list = [None] * self.display_size

        self.frame.bind("<Configure>", self.setup)
        self.canvas.bind("<Configure>", self.setup)
        self.setup(None)

    def scroll(self, *args):
        if args[0] == 'update_width':
            self.scrollbar_width = args[1]
            self.scrollbar.set(1 - self.scrollbar_width, 1)
        if not self.mainWindow.controller.paused:
            # TODO: change color to indicate the user can't scroll
            return

        if args[0] == 'moveto':
            offset = max(0, min(float(args[1]), 1 - self.scrollbar_width))
            self.scrollbar.set(offset, offset + self.scrollbar_width)
            self.display_notes(int(len(self.buffer) * offset))
        elif args[0] == 'scroll':
            amount = int(args[1])
            if args[2] == 'pages':
                self.display_notes(self.current_pos + int(0.5*self.display_size*amount))
            elif args[2] == 'units':
                self.display_notes(self.current_pos + amount)
            offset = self.current_pos/len(self.buffer)
            self.scrollbar.set(offset, offset + self.scrollbar_width)
        
    def setup(self, event): # TODO: fix bug where resizing window removes current data from display
        self.clear()
        self.canvas.delete("all")

        width = self.frame.winfo_width()
        height = self.canvas.winfo_height() # Don't count the scrollbar

        piano_width = height*self.aspect_ratio
        self.piano.configure(width=piano_width)
            
        available_width = width - piano_width
        self.circle_start = piano_width
        self.circle_size = 0.5*available_width/self.display_size
        
        self.noteDict = {
            11: height / 14,
            10: height / 7,
            9: height / 14 * 3,
            8: height / 7 * 2,
            7: height / 14 * 5,
            6: height / 7 * 3,
            5: height / 14 * 7,
            4: height / 14 * 9,
            3: height / 7 * 5,
            2: height / 14 * 11,
            1: height / 7 * 6,
            0: height / 14 * 13
        }

        for note in self.noteDict:
            self.canvas.create_line(piano_width, self.noteDict[note], width, self.noteDict[note], width=3)

        self.display_notes(self.current_pos) # redraw the notes the user was currently looking at

    def update(self, data):
        if len(data.display_buffer) > 0:
            recent = data.display_buffer[-1] #TODO: this could miss events
            self.buffer.append(recent) # TODO: use note_history, replace note names with integral values, remove buffer
            if len(self.buffer) % 10 == 0:
                self.scroll('update_width', 1 / max(1, len(self.buffer) / self.display_size))
            pitch_errors = [(100.0 * data._in_tune_count[i]) / (data._pitch_count[i] if data._pitch_count[i] != 0 else 1) for i in range(0,12)]
            self.piano.set_scores(pitch_errors, data)
            self.display_recent_notes()

    def display_recent_notes(self):
        self.display_notes(max(0, len(self.buffer) - self.display_size))

    def display_notes(self, pos):
        if len(self.buffer) <= self.display_size:
            pos = 0
        else:
            pos = min(max(0, pos), len(self.buffer) - self.display_size)
        self.current_pos = pos
        notes = self.buffer[pos : pos + self.display_size]
        for i, (note, cents) in enumerate(notes):
            color = "red"
            if abs(cents) <= self.mainWindow.controller.threshold:
                color = "green"
            elif abs(cents) <= self.mainWindow.controller.yellow_threshold:
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
        self.circle_list = [None] * self.display_size
