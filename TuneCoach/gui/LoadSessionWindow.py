import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.gui.NewSessionWindow import *
from TuneCoach.python_bridge import Session

# Settings window to load new session
class LoadSessionWindow:
    def load_practice_session(self, oldWindow):
        #print(something)
        session = Session.load_from_file(self.selected_session.get())
        if session is None:
            pass #handle error, display to user
        else:
            self.mainWindow.currentPracticeSession = session
            if self.mainWindow.audio_manager is not None:
                self.mainWindow.audio_manager.destroy()
            self.mainWindow.reset_everything()
            self.mainWindow.audio_manager = AudioManager(session)
            self.mainWindow.myDiagnosticObject.sessionName.configure(text=session._name)
            oldWindow.destroy()
    def load_new_session(self, oldWindow):
        oldWindow.destroy()
        NewSessionWindow(self.mainWindow)

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.master = mainWindow.master

        load_window = tk.Toplevel(self.master)
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

        session_files = Session.get_existing_sessions()
        session_names = list(map(lambda filename: os.path.splitext(filename)[0], session_files))
        if len(session_files) > 0:
            select_session_label = tk.Label(left_frame, text="Select a session to load", bg=background_color, fg="white")
            select_session_label.pack()
            self.selected_session = tk.StringVar()
            self.selected_session.set(session_files[0]) # strip out extension

            load_session_dropdown = tk.OptionMenu(middle_frame, self.selected_session, *session_files)
            load_session_dropdown.pack()
            #TODO: complete functionality for acceptButton
            acceptButton = tk.Button(right_frame, text = "Select", command = lambda: self.load_practice_session(load_window))
            acceptButton.pack()
        else:
            stand_in_label = tk.Label(middle_frame, text="No sessions to choose from. \n Create a new session first.", fg="white", bg=background_color)
            stand_in_label.pack()
            new_session_button = tk.Button(right_frame, text = "New Session", command = lambda: self.load_new_session(load_window))
            new_session_button.pack() 

        load_window.lift(self.master)
