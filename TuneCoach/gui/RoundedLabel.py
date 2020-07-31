import tkinter as tk
from TuneCoach.gui.constants import *


class RoundedLabel(tk.Canvas):
    def __init__(self, parent, text, color, **kwargs):
        self.current_text = text
        self._text = None
        self.color = color
        super().__init__(parent, kwargs, bg=Colors.aux, bd=0, highlightthickness=0) # bg=parent["background"]
        self.draw()
        self.bind("<Configure>", self.draw)

    def set_text(self, text):
        self.current_text = text
        self.itemconfig(self._text, text=self.current_text)
        self.draw()

    def draw(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        self.backdrop = self.round_rectangle(0, 0, width, height, radius=40, fill=self.color)
        self._text = self.create_text(width/2, height/2, fill='#424651')
        self.itemconfig(self._text, text=self.current_text, font=(None, 10, 'bold'))


    # thanks https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)