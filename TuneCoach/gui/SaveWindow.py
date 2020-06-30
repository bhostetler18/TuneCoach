import tkinter as tk
from array import array
import pickle
import zlib
from TuneCoach.gui.constants import *


class SaveWindow: #TODO Gavin and Jenny work on storing data
    def __init__(self, mainWindow):
        myWindow = tk.Toplevel(mainWindow.master)
        myWindow.configure(bg = background_color)
        myLabel = tk.Label(myWindow, text = "Session Successfully Saved.", bg = background_color, fg = "white")
        myLabel.pack(side = tk.TOP, padx = 5, pady = 5)
        myButton = tk.Button(myWindow, text = "OK", command = lambda: myWindow.destroy())
        myButton.pack(side = tk.BOTTOM, padx = 5, pady = 5)
        myWindow.lift(mainWindow.master)

