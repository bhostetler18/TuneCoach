# main gui for TuneCoach. Made by the group, Jamm Hostetler, James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui
from TuneCoach.gui.PitchDisplay import *
from TuneCoach.python_bridge.Session import Session, load_from_file, save_to_file
from TuneCoach.gui.SessionHistory import *
from TuneCoach.gui.SessionDiagnostics import *
from TuneCoach.gui.SaveWindow import *
from TuneCoach.gui.RemoveWindow import *
from TuneCoach.gui.TunerSettingsWindow import *
from TuneCoach.gui.FAQWindow import *
from TuneCoach.gui.TutorialWindow import *
from TuneCoach.gui.IntroWindow import *
from pathlib import Path


# Main GUI
class MainWindow:
    def __init__(self, master):
        self.practiceSessionList = []
        self.currentPracticeSession = Session(15)  # Temporary session! TODO: don't hardcode threshold
        self.currentPracticeSessionName = "Temporary Session"
        self.currentPracticeSessionPath = None
        self.audio_manager = AudioManager(self.currentPracticeSession)
        self.threshold = 15
        self.yellow_threshold = 35

        self.isPaused = True
        self.master = master

        master.attributes('-fullscreen', True)
        master.state('iconic')
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        master.attributes('-fullscreen', False)
        master.deiconify()
        master.title("TuneCoach")
        master.geometry(f'{self.screen_width}x{self.screen_height}')
        master.minsize(width=int(self.screen_width/2), height=int(self.screen_height/2))
        master.maxsize(width=self.screen_width, height=self.screen_height)

        self.create_menubar()
        self.layout_frames(self.screen_width, self.screen_height)
        IntroWindow(self)

    # Adding menu options to the top of the screen.
    def save_practice_session(self):
        if self.currentPracticeSessionPath is None:
            path = tk.filedialog.asksaveasfilename(initialdir = './', title="Save session", filetypes = [('session files', '*.session')])
            if path == '' or path == (): # if the user cancels the dialog, don't do anything
                return
        save_to_file(self.currentPracticeSession, self.currentPracticeSessionPath)
        SaveWindow(self)

    def remove_practice_session(self):
        RemoveWindow(self)

    def tuner_settings(self):
        TunerSettingsWindow(self)

    def load_FAQ(self):
        FAQWindow(self)

    def load_tutorial(self):
        TutorialWindow(self)

    def new_practice_session(self):
        # NewSessionWindow(self)
        path = tk.filedialog.asksaveasfilename(initialdir = './', title="Create a new session", filetypes = [('session files', '*.session')])
        if path == '' or path == (): # if the user cancels the dialog, don't do anything
            return
        if self.audio_manager is not None:
            self.audio_manager.kill()
        
        # New Session Code:
        self.reset_everything()
        self.currentPracticeSession = Session(self.threshold)
        self.currentPracticeSessionPath = path
        self.currentPracticeSessionName = Path(path).stem
        self.audio_manager = AudioManager(self.currentPracticeSession)
        self.myDiagnosticObject.sessionName.configure(text=self.currentPracticeSessionName)
        self.myDiagnosticObject.update_plot(-1)
        self.myHistoryObject.clear()

        self.piano_update()
        self.score_update()
    
    def load_practice_session(self):
        path = tk.filedialog.askopenfilename(initialdir = './', title="Select a session", filetypes = [('session files', '*.session')])
        if path == '' or path == (): # if the user cancels the dialog, don't do anything
            return

        session = load_from_file(path)

        if session is None:
            pass  # TODO: Handle error, display to user
        else:
            self.currentPracticeSession = session
            self.currentPracticeSessionPath = path
            self.currentPracticeSessionName = Path(path).stem
            if self.audio_manager is not None:
                self.audio_manager.kill()
            self.reset_everything()
            self.audio_manager = AudioManager(session)
            self.myDiagnosticObject.sessionName.configure(text=self.currentPracticeSessionName)
            print('success loading session')

            self.piano_update()
            self.score_update()
            # oldWindow.destroy()
    
    def create_menubar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        file_menu = tk.Menu(menubar)

        # File menubar
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Practice Session", command=self.new_practice_session)
        file_menu.add_command(label="Save Current Session", command=self.save_practice_session)
        file_menu.add_command(label="Load Existing Session", command=self.load_practice_session)
        # TODO: Add functionality to remove sessions
        # file_menu.add_separator
        # file_menu.add_command(label = "Remove Practice Session", command = self.remove_practice_session)

        # Settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Tuner Settings", command=self.tuner_settings)

        # Help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="FAQ", command=self.load_FAQ)
        help_menu.add_command(label="Tutorial", command=self.load_tutorial)

    def toggle_pause(self):
        if self.audio_manager is not None:
            if self.audio_manager.is_paused():
                print("Resuming")
                self.isPaused = False
                self.pitchDisplay.resume()
                self.audio_manager.resume()
                self.piano_update()
                self.score_update()
            else:
                print("Pausing")
                self.isPaused = True
                self.pitchDisplay.pause()
                self.audio_manager.pause()

    def force_pause(self):
        if self.audio_manager is not None and not self.audio_manager.is_paused():
            print("Pausing")
            self.isPaused = True
            self.pitchDisplay.pause()
            self.audio_manager.pause()

    def reset_everything(self):
        self.myHistoryObject.clear()
        self.myDiagnosticObject.reset()
        self.force_pause()

        # Creating frames to organize the screen.
    def layout_frames(self, screen_width, screen_height):
        self.bottom_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)
        self.left_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)
        self.right_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)

        # Putting the frames into a grid layout
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # setting up grid weights.
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=4)

        # Here we can work on creating the functionality for each frame, ex: tuner, pitch history, information
        self.myHistoryObject = SessionHistory(self, self.bottom_frame)
        self.myDiagnosticObject = SessionDiagnostics(self)
        self.pitchDisplay = PitchDisplay(self)
    
    def score_update(self):
        if self.audio_manager is not None and not self.isPaused:
            self.myDiagnosticObject.update_plot()
        if not self.isPaused:
            self.master.after(1000, lambda: self.score_update())


    def piano_update(self):
        self.myHistoryObject.update(self.currentPracticeSession)
        if not self.isPaused:
            self.master.after(20, lambda: self.piano_update())