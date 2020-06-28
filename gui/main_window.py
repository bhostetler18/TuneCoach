#main gui for our project, tuneCoach. Made by the group , Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

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

#stand-in variable for noise-filter level, when we come up with some sort of filter, then can initialize real variable like the threshold variable in main of master.py 
noise_filter_level = 20

#main gui
class main_window(tk.Frame):
    def __init__(self, master, manager, feedback_data):
        self.practiceSessionList = []
        self.practiceSessionNameList = []
        self.currentPracticeSession = None
        self.isPaused = False
        tk.Frame.__init__(self, master)
        self.master = master

        self.audio_manager = manager
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar(self.master, feedback_data)
        self.layout_frames(self.master, screen_width, screen_height, feedback_data)

    #adding menu options to the top of the screen.
    def save_practice_session(self, feedback_data):
        SaveWindow(self, self.master, feedback_data)

    def remove_practice_session(self, feedback_data):
        RemoveWindow(self, self.master, feedback_data)

    def tuner_settings(self, feedback_data):
        settingsWindow = TunerSettingsWindow(self.master, feedback_data)

    def change_layout(self):
        print("this will change the layout")

    def user_settings(self):
        print("function to display menu to change user settings")

    def load_faq(self):
        faq = FAQWindow(self.master)

    def load_tutorial(self):
        tutorial = TutorialWindow(self.master)

    def new_practice_session(self, feedback_data):
        newPracticeSessionWindow = NewSessionWindow(self.master, self, feedback_data)

    def load_practice_session(self, feedback_data):
        loadPracticeSessionWindow = LoadSessionWindow(self.master, self, feedback_data)

    def end_practice_session(self, feedback_data):
        EndSessionWindow(self.master, self, feedback_data)
    
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
        file_menu.add_command(label = "Save Practice Session", command = lambda: self.save_practice_session(feedback_data))
        file_menu.add_separator
        file_menu.add_command(label = "Remove Practice Session", command = lambda : self.remove_practice_session(feedback_data))

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
    def layout_frames(self, master, screen_width, screen_height, feedback_data):
        bottomFrame = tk.Frame(master, bd=5, relief=tk.RAISED, bg=background_color)
        leftFrame = tk.Frame(master, bd=5, relief=tk.RAISED, bg=background_color)
        rightFrame = tk.Frame(master, bd=5, relief=tk.RAISED, bg=background_color)

        # Putting the frames into a grid layout
        bottomFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        leftFrame.grid(row=0, column=0, sticky="nsew")
        rightFrame.grid(row=0, column=1, sticky="nsew")

        # setting up grid weights.
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=3)
        master.grid_columnconfigure(1, weight=4)

        # Here we can work on creating the functionality for each frame, ex: tuner, pitch history, information
        self.myHistoryObject = SessionHistory(bottomFrame, screen_width, screen_height)
        self.myDiagnosticObject = SessionDiagnostics(leftFrame, feedback_data, master)

        self.pitchDisplay = PitchDisplay(master, rightFrame, self.audio_manager)
