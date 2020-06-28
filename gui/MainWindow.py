# main gui for TuneCoach. Made by the group, Jamm Hostetler, James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

import tkinter as tk
import tkinter.ttk as ttk
# import PIL.Image
# import PIL.ImageTk
import numpy as np

from PitchDisplay import *
from Session import *
from constants import *
from SessionHistory import *
from MoreInfoWindow import *
from SessionDiagnostics import *
from NewSessionWindow import *
from EndSessionWindow import *
from SaveWindow import *
from RemoveWindow import *
from TunerSettingsWindow import *
from LoadSessionWindow import *
from FAQWindow import *
from TutorialWindow import *

# Stand-in variable for noise-filter level, when we come up with some sort of filter, 
# then can initialize real variable like the threshold variable in main of master.py 
noise_filter_level = 20


# main gui
class MainWindow(tk.Frame):
    def __init__(self, master, manager, session):
        self.practiceSessionList = []
        self.practiceSessionNameList = []
        self.currentPracticeSession = session
        self.isPaused = False
        tk.Frame.__init__(self, master)
        self.master = master

        self.audio_manager = manager
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar(self.master, session)
        self.layout_frames(screen_width, screen_height)

    # adding menu options to the top of the screen.
    def save_practice_session(self):
        SaveWindow(self)

    def remove_practice_session(self):
        RemoveWindow(self)

    def tuner_settings(self, feedback_data):
        TunerSettingsWindow(self.master, feedback_data)

    def change_layout(self):
        print("this will change the layout")

    def user_settings(self):
        print("function to display menu to change user settings")

    def load_faq(self):
        FAQWindow(self)

    def load_tutorial(self):
        TutorialWindow(self)

    def new_practice_session(self, feedback_data):
        NewSessionWindow(self)

    def load_practice_session(self, feedback_data):
        LoadSessionWindow(self.master, self)

    def end_practice_session(self, feedback_data):
        EndSessionWindow(self)
    
    def create_menubar(self, master, feedback_data):
        menubar = tk.Menu(master)    

        master.config(menu=menubar)

        file_menu = tk.Menu(menubar)

        # File menubar
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New Practice Session", command = lambda: self.new_practice_session(feedback_data))
        file_menu.add_separator
        file_menu.add_command(label="End Practice Session", command = lambda: self.end_practice_session(feedback_data))
        file_menu.add_separator
        file_menu.add_command(label="Load Practice Session", command = lambda: self.load_practice_session(feedback_data))
        file_menu.add_separator
        file_menu.add_command(label = "Save Practice Session", command = lambda: self.save_practice_session)
        file_menu.add_separator
        file_menu.add_command(label = "Remove Practice Session", command = lambda : self.remove_practice_session)

        # Settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        settings_menu.add_command(label="Tuner Settings", command = lambda: self.tuner_settings(feedback_data))

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

        # Creating frames to organize the screen.
    def layout_frames(self, screen_width, screen_height):
        bottom_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)
        left_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)
        right_frame = tk.Frame(self.master, bd=5, relief=tk.RAISED, bg=background_color)

        # Putting the frames into a grid layout
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # setting up grid weights.
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=4)

        # Here we can work on creating the functionality for each frame, ex: tuner, pitch history, information
        self.myHistoryObject = SessionHistory(bottom_frame, screen_width, screen_height)
        self.myDiagnosticObject = SessionDiagnostics(left_frame, self)
        self.pitchDisplay = PitchDisplay(self, right_frame, self.audio_manager)
