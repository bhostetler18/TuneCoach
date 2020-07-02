from TuneCoach.gui.NewSessionWindow import *
from TuneCoach.gui.LoadSessionWindow import *


class IntroWindow:
    @staticmethod
    def intro_load_session(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.load_practice_session(ask=False)
        mainWindow.enable()

    @staticmethod
    def intro_new_session(mainWindow, oldFrame):
        oldFrame.destroy()
        mainWindow.disable()
        mainWindow.new_practice_session(ask=False)
        mainWindow.enable()

    def __init__(self, mainWindow):
        self.master = mainWindow.master
        introWindow = tk.Toplevel(self.master)
        introWindow.configure(bg=background_color)
        introWindow.geometry("400x250")

        topFrame = tk.Frame(introWindow, bg=background_color)
        middleFrame = tk.Frame(introWindow, bg=background_color)
        bottomFrame = tk.Frame(introWindow, bg=background_color)
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

        introLabel = tk.Label(topFrame, text="Welcome to Tune Coach!", anchor="e", fg="white", bg=background_color)
        introLabel.configure(font=("Calibri", 20))
        introLabel.pack(side=tk.TOP)

        text = "Please create a new session or load a previous session to begin using the application. \n" \
               "If you don't create or load a session, a temporary session will be used.\n" \
               "\n" \
               "For more information on using TuneCoach, navigate to the \"Help\" tab and then \"Tutorial\"."

        explainLabel = tk.Label(middleFrame, text=text, wraplength=350, bg=background_color, fg="white")
        explainLabel.pack()
        okButton = tk.Button(bottomFrame, text="Ok", command=lambda: introWindow.destroy())
        okButton.pack(side=tk.RIGHT, padx=20, pady=20)
        loadButton = tk.Button(bottomFrame, text="Load Session",
                               command=lambda: self.intro_load_session(mainWindow, introWindow))
        loadButton.pack(side=tk.LEFT, padx=20, pady=20)
        newSession = tk.Button(bottomFrame, text="New Session",
                               command=lambda: self.intro_new_session(mainWindow, introWindow))
        newSession.pack(side=tk.LEFT, padx=20, pady=20)

        introWindow.lift(self.master)
