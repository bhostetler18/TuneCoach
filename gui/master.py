# main rename for our project, tuneCoach. Made by the group , Jamm , James , Joe Gravelle, Jenny Baik, Gavin Gui

from tkinter import *
from tkinter import ttk
import os
import pitchDisplay as PitchDisplay
import menu as MenuBar
# import CONSTANTS
background_color = "#575759"

class Master(Tk):
    def __init__(self):
        super().__init__()
        self.title = 'TuneCoach'

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width}x{screen_height}')

        menu = MenuBar(self)

        bottomFrame = Frame(self, bd=5, relief=RAISED, bg=background_color)
        leftFrame = Frame(self, bd=5, relief=RAISED, bg=background_color)
        rightFrame = Frame(self, bd=5, relief=RAISED, bg=background_color)


        bottomFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        leftFrame.grid(row=0, column=0, sticky="nsew")
        rightFrame.grid(row=0, column=1, sticky="nsew")

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    # adding the temporary label to the session history section.
        session_diagnostics = Label(bottomFrame, text="Session History", font=("Calibri", 20))
        session_diagnostics.config(bg=background_color, fg="white")
        session_diagnostics.pack()

        # adding the temporary label to the session Session Diagnostics section.
        info_header = Label(leftFrame, text="Session Diagnostics", font=("Calibri", 20))
        info_header.config(bg=background_color, fg="white")
        info_header.pack()

        # adding temporary label to the Pitch Detector Section
        tuner_header = Label(rightFrame, text="Pitch Detector", font=("Calibri", 20))
        tuner_header.config(bg=background_color, fg="white")
        tuner_header.pack()

root = Master()
root.mainloop()