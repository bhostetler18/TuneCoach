import tkinter as tk
from practice_session import *
from constants import *

# settings window to create a new session
class new_session_window(tk.Toplevel):
    def creating_a_new_session(self, mainWindow, oldWindow, newName, obj):
        oldWindow.destroy()
        mySession = practice_session(newName)
        mainWindow.practiceSessionList.append(mySession)
        mainWindow.practiceSessionNameList.append(mySession._name)
        mainWindow.practiceSession = mySession
        obj._practice_session = mySession
        mainWindow.myDiagnosticObject.sessionName.configure(text=newName)

    def __init__(self, master, mainWindow, obj):
        self.master = master
        new_sesh_window = tk.Toplevel(master)
        new_sesh_window.geometry("500x100")
        topFrame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        leftFrame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        middleFrame = tk.Frame(new_sesh_window, bd=5, bg=background_color)
        rightFrame = tk.Frame(new_sesh_window, bd=5, bg=background_color)

        topFrame.grid(column=0, row=0, columnspan=3, sticky="nsew")
        leftFrame.grid(row=1, column=0, sticky="nsew")
        middleFrame.grid(row=1, column=1, sticky="nsew")
        rightFrame.grid(row=1, column=2, sticky="nsew")

        new_sesh_window.grid_rowconfigure(0, weight=1)
        new_sesh_window.grid_rowconfigure(1, weight=3)
        new_sesh_window.grid_columnconfigure(0, weight=1)
        new_sesh_window.grid_columnconfigure(1, weight=1)
        new_sesh_window.grid_columnconfigure(2, weight=1)

        # will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame, text="Create New Session", bg=background_color, fg="white")
        createSessionLabel.pack()
        new_sesh_window.lift(master)
        textEntryLabel = tk.Label(leftFrame, text="Enter name of new Session", fg="white", bg=background_color)
        textEntryLabel.pack()
        textEntry = tk.Entry(middleFrame)
        textEntry.insert(tk.END, "new-session-1")
        textEntry.pack()
        enterEntry = tk.Button(rightFrame, text="Enter",
                               command=lambda: self.creating_a_new_session(mainWindow, new_sesh_window, textEntry.get(),
                                                                           obj))
        enterEntry.pack()

        new_sesh_window.lift(master)
