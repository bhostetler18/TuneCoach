import tkinter as tk
import tkinter.ttk as ttk
from TuneCoach.gui.constants import *


# Settings window to end current session
class EndSessionWindow:
    def __init__(self, mainWindow):
        if mainWindow.currentPracticeSession is not None:
            mainWindow.reset_everything()
            mainWindow.currentPracticeSession = None
            mainWindow.audio_manager.destroy()
            mainWindow.audio_manager = None
            mainWindow.myHistoryObject.clear()
            mainWindow.myDiagnosticObject.sessionName.configure(text="No Practice Session Selected")
        else:
            pass

        self.end_sesh_window = tk.Toplevel(mainWindow.master)
        self.end_sesh_window.configure(bg=background_color)
        self.end_sesh_window.geometry("200x100")

        top_frame = tk.Frame(self.end_sesh_window, bg=background_color, bd=5)
        bottom_frame = tk.Frame(self.end_sesh_window, bg=background_color, bd=5)
        top_frame.grid(row=0, sticky="nsew")
        bottom_frame.grid(row=1, sticky="nsew")

        self.end_sesh_window.grid_rowconfigure(0, weight=1)
        self.end_sesh_window.grid_rowconfigure(1, weight=1)

        label_style = ttk.Style()
        label_style.configure("EndSession.TLabel", foreground="white", background=background_color)
        success_label = ttk.Label(top_frame, text="Session ended successfully.", style="EndSession.TLabel")
        success_label.pack()

        button_style = ttk.Style()
        button_style.configure("EndSession.TButton")
        end_button = ttk.Button(bottom_frame, text="Ok", command=lambda: self.end_sesh_window.destroy(), style="EndSession.TButton")
        end_button.pack()
