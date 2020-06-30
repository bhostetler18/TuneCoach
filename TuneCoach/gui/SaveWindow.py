import tkinter as tk
from TuneCoach.gui.constants import *


class SaveWindow: #TODO Gavin and Jenny work on storing data
    def __init__(self, mainWindow,x):
        #uses x to decide whether or not the session can actually be saved.
        myWindow = tk.Toplevel(mainWindow.master)
        myWindow.configure(bg = background_color)
        if x > 0:
            myLabel = tk.Label(myWindow, text = "Session Successfully Saved.", bg = background_color, fg = "white")
            myLabel.pack(side = tk.TOP, padx = 5, pady = 5)
        elif x < 0:
            myLabel = tk.Label(myWindow, text = "No Session to Save", fg = "white", bg = background_color)
            myLabel.pack(side = tk.TOP, padx = 5, pady = 5)
        else:
            myLabel = tk.Label(myWindow, text = "Can't Save Temporary Session", fg = "white", bg = background_color)
            myLabel.pack(side = tk.TOP, padx = 5, pady = 5)
        myButton = tk.Button(myWindow, text = "OK", command = lambda: myWindow.destroy())
        myButton.pack(side = tk.BOTTOM, padx = 5, pady = 5)
        myWindow.lift(mainWindow.master)
