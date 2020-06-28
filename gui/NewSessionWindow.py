import tkinter as tk
from python_bridge.Session import *
from gui.constants import *


# Settings window to create a new session
class NewSessionWindow:
    def creating_a_new_session(self, mainWindow, oldWindow, newName): #TODO ask Joe why new sesh window is old window
        oldWindow.destroy()
        my_session = Session(15, newName) #TODO: fix cent range
        mainWindow.practiceSessionList.append(my_session)
        print("new session is created, it is set to our current practice session variable")
        mainWindow.currentPracticeSession = my_session
        mainWindow.myDiagnosticObject.sessionName.configure(text=newName)

    def __init__(self, mainWindow):
        new_sesh_window = tk.Toplevel(mainWindow)
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
        new_sesh_window.lift(mainWindow)
        text_entry_label = tk.Label(left_frame, text="Enter name of new Session", fg="white", bg=background_color)
        text_entry_label.pack()
        text_entry = tk.Entry(middle_frame)
        text_entry.insert(tk.END, "new-session-1")
        text_entry.pack()
        enter_entry = tk.Button(right_frame, text="Enter",
                               command=lambda: self.creating_a_new_session(mainWindow, new_sesh_window, text_entry.get()))
        enter_entry.pack()

        new_sesh_window.lift(mainWindow)
