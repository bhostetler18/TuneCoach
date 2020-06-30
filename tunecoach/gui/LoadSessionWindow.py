import tkinter as tk
from tunecoach.gui.constants import *

# Settings window to load new session
class LoadSessionWindow:
    def call_function(self, value):
        self.reset_practice_session(self.mainWindow, value)

    def reset_practice_session(self, mainWindow, newPracticeSession):
        for practiceSession in mainWindow.practiceSessionList:
            if practiceSession._name == newPracticeSession:
                mainWindow.currentPracticeSession = practiceSession
                # obj._practice_session = practiceSession
                mainWindow.myDiagnosticObject.sessionName.configure(text=newPracticeSession)

    def __init__(self, master, mainWindow):
        self.mainWindow = mainWindow
        self.master = master

        load_window = tk.Toplevel(master)
        top_frame = tk.Frame(load_window, bd=5, bg=background_color)
        left_frame = tk.Frame(load_window, bd=5, bg=background_color)
        middle_frame = tk.Frame(load_window, bd=5, bg=background_color)
        right_frame = tk.Frame(load_window, bd=5, bg=background_color)

        top_frame.grid(column=0, row=0, columnspan=3, sticky="nsew")
        left_frame.grid(row=1, column=0, sticky="nsew")
        middle_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid(row=1, column=2, sticky="nsew")

        load_window.grid_rowconfigure(0, weight=1)
        load_window.grid_rowconfigure(1, weight=3)
        load_window.grid_columnconfigure(0, weight=1)
        load_window.grid_columnconfigure(1, weight=1)
        load_window.grid_columnconfigure(2, weight=1)

        # will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        create_session_label = tk.Label(top_frame, text="Load Previous Session", bg=background_color, fg="white")
        create_session_label.pack()
        if len(mainWindow.practiceSessionList) > 0:
            select_session_label = tk.Label(left_frame, text="Select a session to load", bg=background_color, fg="white")
            select_session_label.pack()
            first_session = tk.StringVar(master)
            first_session.set(mainWindow.practiceSessionList[0]._name)
            load_session_dropdown = tk.OptionMenu(middle_frame, first_session, *map(lambda session: session._name, mainWindow.practiceSessionList), command=self.call_function)
            load_session_dropdown.pack()
            #TODO: complete functionality for acceptButton
            # acceptButton = tk.Button(middle_frame, text = "Select", command = lambda: reset_practice_session(loadSessionDropDown.get(), mainWindow))
            # acceptButton.pack()
        else:
            stand_in_label = tk.Label(middle_frame, text="No sessions to choose from.", fg="white", bg=background_color)
            stand_in_label.pack()

        load_window.lift(master)
