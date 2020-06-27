import tkinter as tk
from constants import *

#settings window to end current session
class end_session_window(tk.Toplevel):
    def __init__(self, master, mainWindow, obj):
        self.master = master
        mainWindow.practiceSession = None
        obj._practice_session = None
        mainWindow.myDiagnosticObject.a.clear()
        mainWindow.myDiagnosticObject.a.set_title("Score Over Time")
        mainWindow.myDiagnosticObject.a.set_ylabel("Score")
        mainWindow.myDiagnosticObject.canvas.draw()
        self.end_sesh_window = tk.Toplevel(master)
        self.end_sesh_window.configure(bg=background_color)
        self.end_sesh_window.geometry("200x100")
        topFrame = tk.Frame(self.end_sesh_window, bg=background_color, bd=5)
        bottomFrame = tk.Frame(self.end_sesh_window, bg=background_color, bd=5)
        topFrame.grid(row=0, sticky="nsew")
        bottomFrame.grid(row=1, sticky="nsew")
        self.end_sesh_window.grid_rowconfigure(0, weight=1)
        self.end_sesh_window.grid_rowconfigure(1, weight=1)
        successLabel = tk.Label(topFrame, text="Session ended successfully.", fg="white", bg=background_color)
        successLabel.pack()
        endButton = tk.Button(bottomFrame, text="Ok", command=lambda: self.end_sesh_window.destroy())
        endButton.pack()
