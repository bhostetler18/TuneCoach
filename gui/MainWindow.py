# main gui for TuneCoach. Made by the group, Jamm Hostetler, James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

import tkinter as tk
import tkinter.ttk as ttk
# import PIL.Image
# import PIL.ImageTk
import numpy as np

from gui.PitchDisplay import *
from python_bridge.Session import *
from python_bridge.AudioManager import *
from gui.constants import *
from gui.SessionHistory import *
from gui.MoreInfoWindow import *
from gui.SessionDiagnostics import *
from gui.NewSessionWindow import *
from gui.EndSessionWindow import *
from gui.SaveWindow import *
from gui.RemoveWindow import *
from gui.TunerSettingsWindow import *
from gui.LoadSessionWindow import *
from gui.FAQWindow import *
from gui.TutorialWindow import *
from gui.IntroWindow import *

# Stand-in variable for noise-filter level, when we come up with some sort of filter, 
# then can initialize real variable like the threshold variable in main of master.py 
noise_filter_level = 20

# main gui
class MainWindow:
    def __init__(self, master):
        self.practiceSessionList = []
        self.currentPracticeSession = Session(15, "temp") # TODO: don't hardcode threshold
        self.audio_manager = AudioManager(self.currentPracticeSession)
        self.threshold = 15
        
        self.isPaused = False


        self.master = master

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar()

        self.layout_frames(screen_width, screen_height)

        IntroWindow(self)
    # adding menu options to the top of the screen.
    def save_practice_session(self):
        SaveWindow(self)

    def remove_practice_session(self):
        RemoveWindow(self)

    def tuner_settings(self):
        TunerSettingsWindow(self)

    def change_layout(self):
        print("this will change the layout")

    def user_settings(self):
        print("function to display menu to change user settings")

    def load_faq(self):
        FAQWindow(self)

    def load_tutorial(self):
        TutorialWindow(self)

    def new_practice_session(self):
        NewSessionWindow(self)

    def load_practice_session(self):
        LoadSessionWindow(self)

    def end_practice_session(self):
        EndSessionWindow(self)
    
    def create_menubar(self):
        menubar = tk.Menu(self.master)

        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar)

        # File menubar
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New Practice Session", command = self.new_practice_session)
        file_menu.add_separator
        file_menu.add_command(label="End Practice Session", command = self.end_practice_session)
        file_menu.add_separator
        file_menu.add_command(label="Load Practice Session", command = self.load_practice_session)
        file_menu.add_separator
        file_menu.add_command(label = "Save Practice Session", command = self.save_practice_session)
        file_menu.add_separator
        file_menu.add_command(label = "Remove Practice Session", command = self.remove_practice_session)

        # Settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        settings_menu.add_command(label="Tuner Settings", command = self.tuner_settings)

        settings_menu.add_separator
        settings_menu.add_command(label="User Settings", command=self.user_settings)
        settings_menu.add_separator

        # View menubar
        view_menu = tk.Menu(menubar)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Change layout", command=self.change_layout)
        view_menu.add_separator

        # Help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="FAQ", command=self.load_faq)
        help_menu.add_separator
        help_menu.add_command(label="Tutorial", command=self.load_tutorial)
        help_menu.add_separator

    def toggle_pause(self):
        if self.audio_manager.is_paused():
            print("Resuming")
            self.isPaused = False
            self.pitchDisplay.light.start_flashing()
            self.audio_manager.resume()
        else:
            print("Pausing")
            self.isPaused = True
            self.pitchDisplay.light.stop()
            self.audio_manager.pause()

    def force_pause(self):
        if not self.audio_manager.is_paused():
            print("Pausing")
            self.isPaused = True
            self.pitchDisplay.light.stop()
            self.audio_manager.pause()

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
        self.myHistoryObject = SessionHistory(self.bottom_frame, screen_width, screen_height)
        self.myDiagnosticObject = SessionDiagnostics(self)
        self.pitchDisplay = PitchDisplay(self)
