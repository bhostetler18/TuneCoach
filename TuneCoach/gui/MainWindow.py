# main gui for TuneCoach. Made by the group, Jamm Hostetler, James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui
from TuneCoach.gui.PitchDisplay import *
from TuneCoach.gui.Session import Session, load_session, save_session
from TuneCoach.gui.SessionHistory import *
from TuneCoach.gui.SessionDiagnostics import *
from TuneCoach.gui.RemoveWindow import *
from TuneCoach.gui.TunerSettingsWindow import *
from TuneCoach.gui.FAQWindow import *
from TuneCoach.gui.TutorialWindow import *
from TuneCoach.gui.IntroWindow import *


from tkinter import messagebox

def invalid_path(path): return path == '' or path == () or path == None

# Main GUI
class MainWindow:
    def __init__(self, master):
        self.practiceSessionList = []
        self.session = Session(SessionData(15), None)  # Temporary session! TODO: don't hardcode threshold
        self.audio_manager = AudioManager(self.session.data)
        self.threshold = 15
        self.yellow_threshold = 35

        self.paused = True
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
        self.history = SessionHistory(self, self.bottom_frame)
        self.diagnostics = SessionDiagnostics(self)
        self.pitch_display = PitchDisplay(self)
    
    def save_as_practice_session(self):
        path = tk.filedialog.asksaveasfilename(initialdir = './', title="Save session as...", filetypes = [('session files', '*.session')])
        if invalid_path(path): # if the user cancels the dialog, don't do anything
            return False # we didn't save
        self.session = self.session.with_path(path)
        # notify session name change
        self.diagnostics.session_name.configure(text=self.session.name)
        save_session(self.session)
        return True # we did save
        
    # Adding menu options to the top of the screen.
    # returns False ONLY IF THE USER CANCELS
    def save_practice_session(self, ask=False):
        if self.session.path is None:

            # if ask if true, cancel if we say no at the messagebox or if we
            # cancel out of save_as. if ask is false, cancel only if we cancel out
            # of save_as
            if ask and not messagebox.askyesno("", "Save current session?"):
                return True # "save" was successfully, because the user chose to not save
            if not self.save_as_practice_session():
                return False # cancel save
        else:
            if ask and not messagebox.askyesno("", "Save current session?"):
                return True # "save" was successfully, because the user chose to not save
            save_session(self.session)
        
        messagebox.showinfo("Session Saved", f'Session saved to "{self.session.path}" successfully')
        return True # saved successfully

    def remove_practice_session(self):
        RemoveWindow(self)

    def tuner_settings(self):
        TunerSettingsWindow(self)

    def load_FAQ(self):
        FAQWindow(self)

    def load_tutorial(self):
        TutorialWindow(self)

    def setup_session(self, session):
        self.reset_everything()

        if self.audio_manager is not None:
            self.audio_manager.kill()
        
        self.session = session
        self.audio_manager = AudioManager(self.session.data)
        self.diagnostics.session_name.configure(text=self.session.name)

        if not self.session.data.empty:
            self.diagnostics.update_plot()
            self.history.update(self.session.data, force=True)

    def new_practice_session(self, ask=True):
        if ask:
            self.save_practice_session(ask=True)
        data = SessionData(self.threshold)
        self.setup_session(Session(data))
    
    def load_practice_session(self, ask=True):
        if ask:
            self.save_practice_session(ask=True)
        path = tk.filedialog.askopenfilename(initialdir = './', title="Select a session", filetypes = [('session files', '*.session')])
        if invalid_path(path): # if the user cancels the dialog, don't do anything
            return

        session = load_session(path)

        if session is None:
            messagebox.showerror("Invalid session", f'Session located at "{path}" is invalid!')
        else:
            self.setup_session(session)

    def create_menubar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        file_menu = tk.Menu(menubar)

        # File menubar
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Practice Session", command=self.new_practice_session)
        file_menu.add_command(label="Save Current Session", command=self.save_practice_session)
        file_menu.add_command(label="Save Current Session As...", command=self.save_as_practice_session)
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
                self.paused = False
                self.pitch_display.resume()
                self.audio_manager.resume()
                self.piano_update()
                self.score_update()
            else:
                print("Pausing")
                self.paused = True
                self.pitch_display.pause()
                self.audio_manager.pause()

    def force_pause(self):
        if self.audio_manager is not None and not self.audio_manager.is_paused():
            print("Pausing")
            self.paused = True
            self.pitch_display.pause()
            self.audio_manager.pause()

    def reset_everything(self):
        self.force_pause()
        self.history.clear()
        self.diagnostics.clear_plot()
    
    def score_update(self):
        if self.audio_manager is not None and not self.paused:
            self.diagnostics.update_plot()
        if not self.paused:
            self.master.after(500, lambda: self.score_update())

    def piano_update(self):
        self.history.update(self.session.data)
        if not self.paused:
            self.master.after(20, lambda: self.piano_update())
