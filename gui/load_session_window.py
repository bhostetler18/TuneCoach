import tkinter as tk
from gui.constants import *

# settings window to load new session
class load_session_window(tk.Toplevel):
    def call_function(self, value):
        self.reset_practice_session(self.mainWindow, value, self.obj)

    def reset_practice_session(self, mainWindow, newPracticeSession, obj):
        for practiceSession in mainWindow.practiceSessionList:
            if practiceSession._name == newPracticeSession:
                mainWindow.currentPracticeSession = practiceSession
                obj._practice_session = practiceSession
                mainWindow.myDiagnosticObject.sessionName.configure(text=newPracticeSession)

    def __init__(self, master, mainWindow, obj):
        self.obj = obj
        self.mainWindow = mainWindow
        self.master = master

        load_window = tk.Toplevel(master)
        topFrame = tk.Frame(load_window, bd=5, bg=background_color)
        leftFrame = tk.Frame(load_window, bd=5, bg=background_color)
        middleFrame = tk.Frame(load_window, bd=5, bg=background_color)
        rightFrame = tk.Frame(load_window, bd=5, bg=background_color)

        topFrame.grid(column=0, row=0, columnspan=3, sticky="nsew")
        leftFrame.grid(row=1, column=0, sticky="nsew")
        middleFrame.grid(row=1, column=1, sticky="nsew")
        rightFrame.grid(row=1, column=2, sticky="nsew")

        load_window.grid_rowconfigure(0, weight=1)
        load_window.grid_rowconfigure(1, weight=3)
        load_window.grid_columnconfigure(0, weight=1)
        load_window.grid_columnconfigure(1, weight=1)
        load_window.grid_columnconfigure(2, weight=1)

        # will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame, text="Load Previous Session", bg=background_color, fg="white")
        createSessionLabel.pack()
        if len(mainWindow.practiceSessionList) > 0:
            selectSessionLabel = tk.Label(leftFrame, text="Select a session to load", bg=background_color, fg="white")
            selectSessionLabel.pack()
            firstSession = tk.StringVar(master)
            firstSession.set(mainWindow.practiceSessionNameList[0])
            print("hello")
            loadSessionDropDown = tk.OptionMenu(middleFrame, firstSession, *mainWindow.practiceSessionNameList,
                                                command=self.call_function)
            loadSessionDropDown.pack()
            # acceptButton = tk.Button(middleFrame, text = "Select", command = lambda: reset_practice_session(loadSessionDropDown.get(), mainWindow))
            # acceptButton.pack()
        else:
            standInLabel = tk.Label(middleFrame, text="No sessions to choose from.", fg="white", bg=background_color)
            standInLabel.pack()

        load_window.lift(master)
