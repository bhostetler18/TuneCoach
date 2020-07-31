import tkinter as tk
from TuneCoach.gui.constants import *


class RoundedLabel(tk.Canvas):
    def __init__(self, parent, text, color, transparentColor=Colors.aux, **kwargs):
        self.current_text = text
        self._text = None
        self.color = color
        self.font = tk.font.Font(weight='bold',size=11)
        super().__init__(parent, kwargs, bg=transparentColor, bd=0, highlightthickness=0) # bg=parent["background"]
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
        self.set_font_size(width)
        self.backdrop = self.round_rectangle(0, 0, width, height, radius=30, fill=self.color)
        self._text = self.create_text(width/2, height/2, fill='#424651')

        self.itemconfig(self._text, text=self.current_text, font=self.font)

    def set_font_size(self, width):
        default_size = 11
        self.font.config(size=default_size)
        ratio = default_size/self.font.measure(self.current_text)
        size = min(default_size, int(ratio*width*0.95))
        self.font.config(size=size)


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