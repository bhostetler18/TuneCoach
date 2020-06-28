import tkinter as tk
import PIL.Image
import PIL.ImageTk


# Different classes for pop-up windows.
class SessionHistory:
    def create_circle(self, x, y, r, canvasName, fillColor):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, fill=fillColor)

    def __init__(self, workingFrame, width, height):
        self.canvas = tk.Canvas(workingFrame, width=width / 2, height=height / 4, relief=tk.RIDGE, bd=5, bg="#bdd0df")
        self.canvas.pack(side=tk.LEFT, padx=width / 4)

        large_image = PIL.Image.open("./gui/piano.jpeg")
        large_image = large_image.resize((int(width / 10), int(height / 3.9)), PIL.Image.ANTIALIAS)
        piano_image = PIL.ImageTk.PhotoImage(large_image)

        self.width = width
        self.height = height

        self.canvas.create_image(0, 0, anchor=tk.NW, image=piano_image)

        self.noteDict = {
            "C": height / 3.9 / 15,
            "C#": height / 3.9 / 15 * 2.1,
            "D": height / 3.9 / 15 * 3.2,
            "D#": height / 3.9 / 15 * 4.3,
            "E": height / 3.9 / 15 * 5.6,
            "F": height / 3.9 / 15 * 7.1,
            "F#": height / 3.9 / 15 * 8.4,
            "G": height / 3.9 / 15 * 9.5,
            "G#": height / 3.9 / 15 * 10.6,
            "A": height / 3.9 / 15 * 11.7,
            "A#": height / 3.9 / 15 * 12.7,
            "B": height / 3.9 / 15 * 14

        }

        for note in self.noteDict:
            self.canvas.create_line(width / 10, self.noteDict[note], width / 2, self.noteDict[note], width=3)

        self.circle_list = [None] * 64  # TODO: don't hardcode size and coordinate with Feedback buffer
        self.canvas.image = piano_image

    def update(self, data):
        recent = list(data.display_buffer)
        thresh1 = 10
        thresh2 = 25
        for i, (note, cents) in enumerate(recent):
            color = "red"
            if abs(cents) <= thresh1:
                color = "green"
            elif abs(cents) <= thresh2:
                color = "yellow"

            circle = self.circle_list[i]
            x = self.width / 10 + (i + 1) * 20
            y = self.noteDict[note]
            if circle is None:
                c = self.create_circle(x, y, 10, self.canvas, color)
                self.circle_list[i] = c
            else:
                self.canvas.coords(circle, x - 10, y - 10, x + 10, y + 10)
                self.canvas.itemconfig(circle, fill=color)
