import tkinter as tk
from TuneCoach.python_bridge.pitch_utilities import *
from TuneCoach.gui.constants import *


# set_score uses session.data.key_signature.accidental
class Piano(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs, bd=0, highlightthickness=0)
        self._parent = parent
        self.configure(bg='black')
        self.bind("<Configure>", self.draw)
        self.keys = []
        self.cached_scores = [0] * 12
        self.cached_key = KeySignature("C", 0, Accidental.SHARP, 0, KeySignatureType.MAJOR)
        self.draw(None)

    def draw(self, event):
        self.delete("all")
        self.keys.clear()
        width = self.winfo_width()
        height = self.winfo_height()
        key_gap = 1.2 # TODO: not needed because tk adds a pixel gap automatically?
        white_key_height = height/7
        black_key_height = height/14
        black_key_width = width*0.6
        for i in range(0, 7):
            w = self.create_rectangle(0, (white_key_height)*i + key_gap/2, width, (white_key_height)*(i+1) - key_gap/2, fill='white')
            if i not in {0,4,7}:
                b = self.create_rectangle(0, (white_key_height)*(i) - black_key_height/2, black_key_width, white_key_height*(i)+black_key_height/2, fill='black')
                self.keys.append(b)
            self.keys.append(w)
        self.keys.reverse()
        self.set_scores(self.cached_scores, self.cached_key)
    
    # pass in a list of 12 percentages for C through B
    def set_scores(self, scores, key_signature):
        if len(scores) != 12:
            print("INVALID SCORE LIST")
            return

        self.cached_scores = scores
        self.cached_key = key_signature
        self.delete("text")

        for i in [0, 2, 4, 5, 7, 9, 11]:
            key = self.keys[i]
            coords = self.coords(key)
            x = coords[2] - 30
            y = (coords[3] + coords[1]) / 2
            score = round(scores[i])
            if score >= 70:
                textColor = Colors.green
            elif score >= 50:
                textColor = "#e0b000" # More visible against white background
            elif score == 0:
                textColor = "black"
            else:
                textColor = Colors.red     
            self.create_text(x, y, text=f"{key_signature.get_display_for(i)}: {score}%", fill=textColor, tag="text")
        for i in [1,3,6,8,10]:
            key = self.keys[i]
            coords = self.coords(key)
            x = coords[2] - 30
            y = (coords[3] + coords[1]) / 2
            score = round(scores[i])
            if score >= 70:
                textColor = Colors.green
            elif score >= 50:
                textColor = Colors.yellow
            elif score == 0:
                textColor = "white"
            else:
                textColor = "red" # More visible against black background
            self.create_text(x, y, text=f"{key_signature.get_display_for(i)}: {round(scores[i])}%", fill=textColor, tag="text")