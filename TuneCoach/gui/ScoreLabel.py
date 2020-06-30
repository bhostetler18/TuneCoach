import tkinter as tk

class ScoreLabel(tk.Canvas):
    def __init__(self, parent, text, width, height):
        super().__init__(parent, width=width, height=height, bg=parent["background"], bd=0, highlightthickness=0)
        self.backdrop = self.round_rectangle(0, 0, width, height, radius=40, fill='green')
        self._text = self.create_text(width/2, height/2, fill='white')
        self.itemconfig(self._text, text=text, font=(None, 10))
        self.set_text(text)

    def set_text(self, text):
        self.itemconfig(self._text, text=text)


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