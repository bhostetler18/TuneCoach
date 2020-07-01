import tkinter as tk
from TuneCoach.python_bridge.SessionData import *
from TuneCoach.gui.constants import *
from TuneCoach.python_bridge.AudioManager import *
from TuneCoach.gui.SaveProgressWindow import *


# Settings window to create a new session
class NewSessionWindow:
    #will check whether or not new session name is valid and whether or not you want to save your old session
    def new_session_buffer(self, mainWindow, popup, newName):
        x = 0
        for session in mainWindow.currentPracticeSession.get_existing_sessions():
            if mainWindow.currentPracticeSession.load_from_file(session)._name == newName or mainWindow.currentPracticeSession.load_from_file(session)._name == newName + ".session" or newName == "Temporary Practice Session" or newName == mainWindow.currentPracticeSession._name:
                self.text_entry_label.configure(text = "Session already exists. \n Please enter a new session name.")
                x += 1
        if x == 0:
            if mainWindow.currentPracticeSession is not None and mainWindow.currentPracticeSession._name != "Temporary Session":
                SaveProgressWindow(mainWindow, self, popup, newName)
            else:
                self.creating_a_new_session(mainWindow, popup, newName)
    #will actually create new session
    def creating_a_new_session(self, mainWindow, popup, newName):
        # Cleanup Code:
        #x = 0
        #for session in mainWindow.currentPracticeSession.get_existing_sessions():
        #    if mainWindow.currentPracticeSession.load_from_file(session)._name == newName or mainWindow.currentPracticeSession.load_from_file(session)._name == newName + ".session":
        #        self.text_entry_label.configure(text = "Session already exists.\n Please enter a new session name.")
        #        print("Session Already Exists")
        #        x += 1
        #if x == 0:
        #    if mainWindow.currentPracticeSession is not None and mainWindow.currentPracticeSession._name != "Temporary Session":
        #        SaveProgressWindow(mainWindow)
            if mainWindow.audio_manager is not None:
                mainWindow.audio_manager.destroy()

            # New Session Code:
            mainWindow.reset_everything()
            new_session = Session(mainWindow.threshold, newName) # TODO: Make threshold setting in the popup for new session
            mainWindow.currentPracticeSession = new_session
            mainWindow.practiceSessionList.append(new_session)
            mainWindow.audio_manager = AudioManager(new_session)
            print("new session is created, it is set to our current practice session variable")
            mainWindow.myDiagnosticObject.sessionName.configure(text=newName)
            mainWindow.myDiagnosticObject.update_plot(-1)
            mainWindow.myHistoryObject.clear()
            popup.destroy()

    def __init__(self, mainWindow):
        new_sesh_window = tk.Toplevel(mainWindow.master)
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
        new_sesh_window.lift(mainWindow.master)
        self.text_entry_label = tk.Label(left_frame, text="Enter name of new Session", fg="white", bg=background_color)
        self.text_entry_label.pack()
        text_entry = tk.Entry(middle_frame)
        if  mainWindow.currentPracticeSession._name != "new-session-%d" % len(mainWindow.currentPracticeSession.get_existing_sessions()):
            defaultText = "new-session-%d" % len(mainWindow.currentPracticeSession.get_existing_sessions())
        else:
            defaultText = "new-session-%d" % (len(mainWindow.currentPracticeSession.get_existing_sessions())+1)
        text_entry.insert(tk.END, defaultText)
        text_entry.pack()
        #enter_entry = tk.Button(right_frame, text="Enter",
                               #command=lambda: self.creating_a_new_session(mainWindow, new_sesh_window, text_entry.get()))
        enter_entry = tk.Button(right_frame, text = "Enter", command = lambda : self.new_session_buffer(mainWindow, new_sesh_window, text_entry.get()))
        enter_entry.pack()

        new_sesh_window.lift(mainWindow.master)
