import tkinter as tk
from TuneCoach.python_bridge.pitch_utilities import Accidental

class Piano(tk.Canvas):
    def __init__(self, parent, mainWindow, **kwargs):
        super().__init__(parent, kwargs)
        self._parent = parent
        self.mainWindow = mainWindow
        self.configure(bd=0)
        self.configure(bg='black')
        self.configure(highlightthickness=0)
        self.bind("<Configure>", self.draw)
        self.keys = []
        self.flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.draw(None)

    def draw(self, event):
        self.delete("all")
        self.keys.clear()
        width = self.winfo_width()
        height = self.winfo_height()
        key_gap = 1
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
    
    # pass in a list of 12 percentages for C through B
    def set_scores(self, scores):
        if len(scores) != 12:
            print("INVALID SCORE LIST")
            return

        self.delete("text")
        notes = None
        if self.mainWindow.controller.session.data.key_signature.accidental == Accidental.SHARP: # TODO: refactor
            notes = self.sharp_notes
        else:
            notes = self.flat_notes

        for i in [0,2,4,5,7,9,11]:
            key = self.keys[i]
            coords = self.coords(key)
            x = coords[2] / 2
            y = (coords[3] + coords[1]) / 2
            if round(scores[i]) > 70:
                textColor = "green"
            elif round(scores[i]) > 50:
                textColor = "gold"
            else:
                textColor = "red"        
            textID = self.create_text(x, y, text=f"{notes[i]}: {round(scores[i])}%", fill=textColor, tag="text")
        for i in [1,3,6,8,10]:
            key = self.keys[i]
            coords = self.coords(key)
            x = coords[2] / 2
            y = (coords[3] + coords[1]) / 2
            if round(scores[i]) > 70:
                textColor = "green"
            elif round(scores[i]) > 50:
                textColor = "gold"
            else:
                textColor = "red"  
            textID = self.create_text(x, y, text=f"{notes[i]}: {round(scores[i])}%", fill=textColor, tag="text")
