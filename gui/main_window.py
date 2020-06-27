#main gui for our project, tuneCoach. Made by the group , Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

import tkinter as tk
import tkinter.ttk as ttk
# import PIL.Image
# import PIL.ImageTk
import numpy as np

from pitchDisplay import *
from FeedbackSystem import *
from constants import *
from session_history import *
from more_info_window import *
from session_diagnostics import *
from new_session_window import *
from end_session_window import *
from save_window import *
from remove_window import *
from tuner_settings_window import *
from load_session_window import *

#stand-in variable for noise-filter level, when we come up with some sort of filter, then can initialize real variable like the threshold variable in main of master.py 
noise_filter_level = 20

#main gui
class main_window(tk.Frame):
    def __init__(self, master, manager, obj):
        self.practiceSessionList = []
        self.practiceSessionNameList = []
        self.practiceSession = None
        self.isPaused = False
        tk.Frame.__init__(self, master)
        self.master = master

        self.audio_manager = manager
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar(self.master, obj)
        self.layout_frames(self.master, screen_width, screen_height, obj)

    #adding menu options to the top of the screen.
    def save_practice_session(self, obj):
        save_window(self, self.master, obj)
    def remove_practice_session(self, obj):
        remove_window(self, self.master,obj)
    def tuner_settings(self, obj):
        settingsWindow = tuner_settings_window(self.master, obj)
    def change_layout(self):
        print("this will change the layout")
    def user_settings(self):
        print("function to display menu to change user settings")
    def load_faq(self):
        print("function to load app faq")
    def load_tutorial(self):
        print("function to load a tutorial for how to use the app")   
    def new_practice_session(self, obj):
        newPracticeSessionWindow = new_session_window(self.master, self, obj)
    def load_practice_session(self, obj):
        loadPracticeSessionWindow = load_session_window(self.master, self, obj)
    def end_practice_session(self, obj):
        end_session_window(self.master, self, obj)   
    
    def create_menubar(self, master, obj):
        menubar = tk.Menu(master)    

        master.config(menu=menubar)

        file_menu = tk.Menu(menubar)

        #file menubar
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Practice Session", command = lambda: self.new_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label="End Practice Session", command = lambda: self.end_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label="Load Practice Session", command = lambda: self.load_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label = "Save Practice Session", command = lambda: self.save_practice_session(obj))
        file_menu.add_separator
        file_menu.add_command(label = "Remove Practice Session", command = lambda : self.remove_practice_session(obj))

        #settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Tuner Settings", command = lambda: self.tuner_settings(obj))
        settings_menu.add_separator
        settings_menu.add_command(label="User Settings", command =self.user_settings)
        settings_menu.add_separator

        #view menubar
        view_menu = tk.Menu(menubar)
        menubar.add_cascade(label="View", menu = view_menu)
        view_menu.add_command(label="Change layout", command = self.change_layout)
        view_menu.add_separator

        #help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="FAQ", command = self.load_faq)
        help_menu.add_separator
        help_menu.add_command(label="Tutorial", command = self.load_tutorial)
        help_menu.add_separator
        #creating frames to organize the screen.
    
    def layout_frames(self, master, screen_width, screen_height, obj):
        bottomFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)
        leftFrame = tk.Frame(master, bd = 5, relief = tk.RAISED ,bg =  background_color)
        rightFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)

        #putting the frames into a grid layout

        bottomFrame.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew")
        leftFrame.grid(row = 0, column = 0, sticky = "nsew")
        rightFrame.grid(row = 0, column = 1, sticky = "nsew")

        #setting up grid weights.

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=3)
        master.grid_columnconfigure(1, weight=4)

        #i think that here we can work on creating the funcitonality for each individual frame, ex: tuner, pitch history, information.


        self.myHistoryObject = session_history(bottomFrame, screen_width, screen_height)
        self.myDiagnosticObject = session_diagnostics(leftFrame, obj, master)

        self.pitchDisplay = PitchDisplay(master, rightFrame, self.audio_manager)
