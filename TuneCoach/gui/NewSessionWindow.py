
#just a class to create a window letting you know that a new session has been created

import tkinter as tk
import tkinter.ttk as ttk

class NewSessionWindow:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        newSessionWindow = tk.Toplevel(self.mainWindow.master,bg = "#F5F6F7")
        newSessionWindow.geometry("300x100")
        myLabel = tk.Label(newSessionWindow, text = "New Session Successfully Created.", bg = "#F5F6F7")
        myLabel.pack(padx = 10, pady = 10)
        myButton = ttk.Button(newSessionWindow, text = "Ok",command = lambda: newSessionWindow.destroy())
        myButton.pack(padx = 10, pady = 10)
        newSessionWindow.lift(self.mainWindow.master)
