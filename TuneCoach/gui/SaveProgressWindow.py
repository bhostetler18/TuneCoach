import tkinter as tk
import tkinter.ttk as ttk
from TuneCoach.gui.constants import *

class SaveProgressWindow:
    def save_session(self, mainWindow, oldWindow, callingFunction, callingWindow):
        oldWindow.destroy()
        mainWindow.save_practice_session()
        #then we know the function is loadSession, else its newSession
        if self.new_name is None:
            callingFunction.load_practice_session(callingWindow)
        else:
            callingFunction.creating_a_new_session(mainWindow, callingWindow, self.new_name)

    def no_save(self,mainWindow, oldWindow, callingFunction, callingWindow):
        oldWindow.destroy()
        if self.new_name is None:
            callingFunction.load_practice_session(callingWindow)
        else:
            callingFunction.creating_a_new_session(mainWindow, callingWindow, self.new_name)

    def __init__(self, mainWindow, callingFunction, callingWindow,newName = None):
        self.new_name = newName
        myWindow = tk.Toplevel(mainWindow.master)

        topFrame = ttk.Frame(myWindow)
        bottomFrame = ttk.Frame(myWindow)
        topFrame.grid(row = 0, sticky = "nsew")
        bottomFrame.grid(row = 1, sticky = "nsew")
        myWindow.grid_rowconfigure(0, weight = 1)
        myWindow.grid_rowconfigure(1, weight = 1)
        myLabel = ttk.Label(topFrame, text = "Would you like to save your current session first?")
        myLabel.pack()
        noButton = ttk.Button(bottomFrame, text = "No", command = lambda: self.no_save(mainWindow, myWindow, callingFunction, callingWindow))
        noButton.pack(side = tk.LEFT, padx = 5, pady = 5)
        saveButton = ttk.Button(bottomFrame, text = "Save", command = lambda: self.save_session(mainWindow, myWindow, callingFunction, callingWindow))
        saveButton.pack(side = tk.RIGHT, padx = 5, pady = 5)
        myWindow.lift(mainWindow.master)

