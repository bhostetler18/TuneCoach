import tkinter.ttk as ttk
import tkinter as tk
from TuneCoach.gui.constants import Colors


class IntroWindow:
    @staticmethod
    def intro_load_session(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.controller.load_from()
        mainWindow.enable()

    @staticmethod
    def intro_save_session_as(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.controller.save_as()
        mainWindow.enable()

    def __init__(self, mainWindow):
        self.master = mainWindow.master
        introWindow = tk.Toplevel(self.master)
        introWindow.geometry("520x300")
        introWindow.minsize(width = 520, height = 350)
        introWindow.maxsize(width = 520, height = 350)
        intro_window_style = ttk.Style()
        intro_window_style.configure("Intro.TFrame")
        topFrame = ttk.Frame(introWindow, style="Intro.TFrame")
        middleFrame = ttk.Frame(introWindow, style="Intro.TFrame")
        bottomFrame = ttk.Frame(introWindow, style="Intro.TFrame")

        topFrame.grid(row=0, column=1, sticky="nsew")
        middleFrame.grid(row=1, column=1, sticky="nsew")
        bottomFrame.grid(row=2, column=1, sticky="nsew")

        introWindow.grid_rowconfigure(0, weight=1)
        introWindow.grid_rowconfigure(1, weight=1)
        introWindow.grid_rowconfigure(2, weight=1)

        intro_label_style = ttk.Style()
        intro_label_style.configure("IntroTitle.TLabel", font="Ubuntu 24", padding=15)
        introLabel = ttk.Label(topFrame, text="Welcome to Tune Coach!", anchor=tk.CENTER, style="IntroTitle.TLabel")
        introLabel.pack(side=tk.TOP)

        text = "New to TuneCoach? Checkout Help -> Tutorial.\n\n" \
               "Click 'Load Session' if you would like to load a previous session from file. \n\n" \
               "If you don't load an existing session, a temporary session will be used. You can choose to store this session under a name by clicking the 'Save Temporary Session As...' button.\n"

        explain_label_style = ttk.Style()
        explain_label_style.configure("Intro.TLabel", wraplength=375)
        explainLabel = ttk.Label(middleFrame, text=text, style="Intro.TLabel")
        explainLabel.pack()
        loadButton = ttk.Button(bottomFrame, text="Load Session",
                               command=lambda: self.intro_load_session(mainWindow, introWindow))
        loadButton.pack(side=tk.RIGHT, padx=50, pady=20)
        newSession = ttk.Button(bottomFrame, text="Save Temporary Session As...",
                               command=lambda: self.intro_save_session_as(mainWindow, introWindow))
        newSession.pack(side=tk.LEFT, padx=50, pady=20)

        introWindow.lift(self.master)
