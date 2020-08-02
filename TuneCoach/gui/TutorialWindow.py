import tkinter as tk
import tkinter.ttk as ttk
from TuneCoach.gui.constants import *


class TutorialWindow: #TODO: Style Tutorial Window so it's not ugly - Jenny
    def __init__(self, mainWindow):
        tutorial_window = tk.Toplevel(mainWindow.master, bg = "#F4F4F4")
        tutorial_window.title("Tutorial")
        tutorial_window.geometry()
        tutorial_window.minsize(width=590, height=480)

        about_tunecoach_text = "TuneCoach is convenient PC-based tuning application that records sessions for intonation and provides detailed \nfeedback for your performance."
        new_to_tunecoach_text = 'New to TuneCoach?'
        get_started_text = 'To get started, click the "File" dropdown menu in the top left corner and select "New Practice Session".\n' \
                           'In the same dropdown menu, there are more options to manage your TuneCoach sessions.\n' \
                           '(Note: Upon startup of TuneCoach, no data will be saved unless a session is explicitly started.)' \
                           '\n\nThe Pitch Detector continuously shows the note being played, as well as the intonation.\n' \
                           'A Green square means that the note is in tune, a yellow square means that the note is outside set cents threshold,\n and a red square means the note is very out of tune.\n' \
                           '\nThe bottom area shows your recently played notes, represented on a piano octave.\n'\
                           'The Session Diagnostics area shows your overall score and actively reflected in the graph.\n' \
                           'You can click on "More Info" button to display how in tune you were for each note the overall score, and how out of tune\nyou were overall in cents.'
        keyboard_shortcuts_title = 'Keyboard Shortcuts:'

        tutorial_text_style = ttk.Style()
        tutorial_text_style.configure('TutorialTextLabel.TLabel', padding=10, width=100, anchor=tk.W)
        about_tunecoach_text_label = ttk.Label(tutorial_window, text=about_tunecoach_text, style='TutorialTextLabel.TLabel')
        about_tunecoach_text_label.configure(wraplength = mainWindow.screen_width - 10)
        about_tunecoach_text_label.pack()


        tutorial_title_style = ttk.Style()
        tutorial_title_style.configure('TutorialTitleLabel.TLabel', font="Ubuntu 15", width=73, anchor=tk.W)
        new_to_tunecoach_text_label = ttk.Label(tutorial_window, text=new_to_tunecoach_text, style='TutorialTitleLabel.TLabel')
        new_to_tunecoach_text_label.pack()

        get_started_text_label = ttk.Label(tutorial_window, text=get_started_text, style='TutorialTextLabel.TLabel')
        get_started_text_label.configure(wraplength = mainWindow.screen_width - 80)
        get_started_text_label.pack()

        keyboard_shortcuts_title_label = ttk.Label(tutorial_window, text=keyboard_shortcuts_title, style='TutorialTitleLabel.TLabel', padding=10)
        keyboard_shortcuts_title_label.pack()

        text = ttk.Style()
        text.configure('Text.TLabel', width=100, anchor=tk.W)

        keyboard_shortcut_pairs = [
            ('Space', 'Pause or resume the session.'),
            ('CTRL-N', 'Create a new session.'),
            ('CTRL-S', 'Save the current session.'),
            ('CTRL-SHIFT-S', 'Save the current session as... '),
            ('CTRL-O', 'Open the menu to load an existing session.'),
            ('CTRL-T', 'Open the tuner settings window.'),
            ('F1', 'Open the tutorial window.'),
            ('F2', 'Open the FAQ window.\n')
        ]

        for key, action in keyboard_shortcut_pairs:
            key_label = ttk.Label(tutorial_window, text=key +": "+ action, style='Text.TLabel')
            key_label.pack()

        tutorial_window.lift(mainWindow.master)
