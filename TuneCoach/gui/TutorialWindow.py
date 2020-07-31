import tkinter as tk
import tkinter.ttk as ttk
from TuneCoach.gui.constants import *


class TutorialWindow: #TODO: Style Tutorial Window so it's not ugly - Jenny
    def __init__(self, mainWindow):
        tutorial_window = tk.Toplevel(mainWindow.master, bg = "#F4F4F4")
        tutorial_window.geometry()
        tutorial_window.minsize(width = 590, height = 480)

        message = "                                             Welcome to TuneCoach!\n" \
                  "TuneCoach is convenient PC-based tuning application that records sessions for intonation\n" \
                  "and provides detailed feedback for your performance. \n" \
                  "\n" \
                  "To get started, click the \"File\" dropdown menu in the top left corner and select \n" \
                  "\"New Practice Session\"\n" \
                  "In the same dropdown menu, there are more options to manage your tuning sessions\n" \
                  "(Note: The pitch detector will function upon startup, but it will be in practice mode.\n" \
                  "This means that the tuner works but no session is started and therefore no data is saved.)\n" \
                  "\n" \
                  "The Pitch Detector continuously shows the note being played, as well as the intonation.\n" \
                  "Green means you're in tune, yellow means you're a little bit out of tune, and red means\n" \
                  "you're completely out of tune.\n" \
                  "The bottom area shows your recently played notes, represented on a piano octave.\n" \
                  "The Session Diagnostics area shows your overall score and actively reflected in the graph.\n" \
                  "You can click on \"More Info\" button to display how in tune you were for each note,\n" \
                  "the overall score, and how out of tune you were overall in cents.\n" \
                  "\n" \
                  "Keyboard Shortcuts:\n" \
                  "------------------------------------------\n" \
                  "Space: Pause or resume the session.\n" \
                  "n: Create a new session.\n" \
                  "s: Save the current session (save as if in Temporary Session).\n" \
                  "F12: Opens the \"Save as\" menu.\n" \
                  "l: Opens the menu to load an existing session.\n" \
                  "o: Opens the tuner options and settings window.\n" \
                  "F1: Opens the tutorial.\n" \
                  "F2: Opens the Frequently Asked Questions.\n"

        tutorial_label = ttk.Label(tutorial_window, text=message)#, font=("Calibri", 12), justify=tk.LEFT)
        # tutorial_label.config(bg=background_color, fg="white")
        tutorial_label.pack()
        tutorial_window.lift(mainWindow.master)
