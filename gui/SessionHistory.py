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

    def __init__(self, workingFrame):
        self.frame = workingFrame
        self.canvas = tk.Canvas(workingFrame, bg="#bdd0df")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()

        self.large_image = PIL.Image.open("./gui/piano.jpeg")
        self.aspect_ratio = self.large_image.width / self.large_image.height
        self.piano_image = PIL.ImageTk.PhotoImage(self.large_image)

        self.circle_list = [None] * 64  # TODO: don't hardcode size and coordinate with Feedback buffer
        #self.canvas.image = piano_image
        self.frame.bind("<Configure>", self.setup)


    def setup(self, event):
        self.clear()
        self.canvas.delete("all")
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()
        resized = self.large_image.resize((int(self.height*self.aspect_ratio), int(self.height)), PIL.Image.ANTIALIAS)
        self.piano_image = PIL.ImageTk.PhotoImage(resized)
        #self.large_image.thumbnail(max, PIL.Image.ANTIALIAS)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.piano_image)
        
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
            self.canvas.create_line(self.piano_image.width(), self.noteDict[note], self.width, self.noteDict[note], width=3)

    def update(self, data):
        if data is not None:
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

    def clear(self):
        for circle in self.circle_list:
            self.canvas.delete(circle)
        self.circle_list = [None] * 64
