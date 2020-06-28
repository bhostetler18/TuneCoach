import tkinter as tk
from practice_session import *
from constants import *


# Settings window to create a new session
class NewSessionWindow(tk.Toplevel):
    def creating_a_new_session(self, mainWindow, oldWindow, newName, obj):
        oldWindow.destroy()
        my_session = practice_session(newName)
        mainWindow.practiceSessionList.append(my_session)
        mainWindow.practiceSessionNameList.append(my_session._name)
        mainWindow.currentPracticeSession = my_session
        obj._practice_session = my_session
        mainWindow.myDiagnosticObject.sessionName.configure(text=newName)

    def __init__(self, master, mainWindow, obj):
        self.master = master
        new_sesh_window = tk.Toplevel(master)
        new_sesh_window.geometry("500x100")
        top_frame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        left_frame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        middle_frame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        right_frame = tk.Frame(new_sesh_window, bd=5, bg=background_color)

        top_frame.grid(column=0, row=0, columnspan=3, sticky="nsew")
        left_frame.grid(row=1, column=0, sticky="nsew")
        middle_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid(row=1, column=2, sticky="nsew")

        new_sesh_window.grid_rowconfigure(0, weight=1)
        new_sesh_window.grid_rowconfigure(1, weight=3)
        new_sesh_window.grid_columnconfigure(0, weight=1)
        new_sesh_window.grid_columnconfigure(1, weight=1)
        new_sesh_window.grid_columnconfigure(2, weight=1)

        # will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        create_session_label = tk.Label(top_frame, text="Create New Session", bg=background_color, fg="white")
        create_session_label.pack()
        new_sesh_window.lift(master)
        text_entry_label = tk.Label(left_frame, text="Enter name of new Session", fg="white", bg=background_color)
        text_entry_label.pack()
        text_entry = tk.Entry(middle_frame)
        text_entry.insert(tk.END, "new-session-1")
        text_entry.pack()
        enter_entry = tk.Button(right_frame, text="Enter",
                               command=lambda: self.creating_a_new_session(mainWindow, new_sesh_window, text_entry.get(),
                                                                           obj))
        enter_entry.pack()

        new_sesh_window.lift(master)
