import tkinter.ttk as ttk
import tkinter as tk
from TuneCoach.gui.constants import background_color


class IntroWindow:
    @staticmethod
    def intro_load_session(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.controller.load_from()
        mainWindow.enable()

    @staticmethod
    def intro_new_session(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.controller.new_session()
        mainWindow.enable()

    def __init__(self, mainWindow):
        self.master = mainWindow.master
        introWindow = tk.Toplevel(self.master)
        # introWindow.configure(bg=background_color)
        introWindow.geometry("410x250")

        intro_window_style = ttk.Style()
        intro_window_style.configure("Intro.TFrame")#, background=background_color)
        topFrame = ttk.Frame(introWindow, style="Intro.TFrame")
        middleFrame = ttk.Frame(introWindow, style="Intro.TFrame")
        bottomFrame = ttk.Frame(introWindow, style="Intro.TFrame")
        # bottomRight = tk.Frame(introWindow, bg=background_color)
        # bottomLeft = tk.Frame(introWindow, bg=background_color)

        topFrame.grid(row=0, column=1, sticky="nsew")
        middleFrame.grid(row=1, column=1, sticky="nsew")
        bottomFrame.grid(row=2, column=1, sticky="nsew")
        # bottomRight.grid(row=2, column=2, sticky="nsew")
        # bottomLeft.grid(row=2, column=0, sticky="nsew")

        introWindow.grid_rowconfigure(0, weight=1)
        introWindow.grid_rowconfigure(1, weight=1)
        introWindow.grid_rowconfigure(2, weight=1)
        # introWindow.grid_columnconfigure(0, weight=1)
        # introWindow.grid_columnconfigure(1, weight=1)
        # introWindow.grid_columnconfigure(2, weight=1)

        intro_label_style = ttk.Style()
        intro_label_style.configure("IntroTitle.TLabel", font="Ubuntu 24")
        introLabel = ttk.Label(topFrame, text="Welcome to Tune Coach!", anchor=tk.CENTER, style="IntroTitle.TLabel")#, fg="white", bg=background_color)
        introLabel.pack(side=tk.TOP)

        text = "Please create a new session or load a previous session to begin using the application. \n" \
               "If you don't create or load a session, a temporary session will be used.\n" \
               "\n" \
               "For more information on using TuneCoach, navigate to the \"Help\" tab and then \"Tutorial\"."

        explain_label_style = ttk.Style()
        explain_label_style.configure("Intro.TLabel", wraplength=375)
        explainLabel = ttk.Label(middleFrame, text=text, style="Intro.TLabel")# wraplength=350, bg=background_color, fg="white")
        explainLabel.pack()
        okButton = ttk.Button(bottomFrame, text="OK", command=lambda: introWindow.destroy())
        okButton.pack(side=tk.RIGHT, padx=15, pady=20)
        loadButton = ttk.Button(bottomFrame, text="Load Session",
                               command=lambda: self.intro_load_session(mainWindow, introWindow))
        loadButton.pack(side=tk.LEFT, padx=15, pady=20)
        newSession = ttk.Button(bottomFrame, text="New Session",
                               command=lambda: self.intro_new_session(mainWindow, introWindow))
        newSession.pack(side=tk.LEFT, padx=15, pady=20)

        introWindow.lift(self.master)
