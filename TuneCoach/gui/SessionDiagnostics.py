import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.gui.RoundedLabel import *
import tkinter.ttk as ttk
from TuneCoach.gui.Graph import *

# OUT data.update_score_history()
class SessionDiagnostics:
    def clear_plot(self):
        self.myGraph.clear_plot()

    def update_plot(self, data):
        self.myGraph.update_plot(data.score_history)
        if data is not None:
            display_settings = "Settings:\n" \
                                   "-------------------\n" \
                               "Threshold: ±%d cents\n" \
                               "Key Signature: %s\n" \
                               "Range: %s%s to %s%s" % (data.green_thresh, data.key_signature.name, data.lowest_note, 
                                                                                                    data.lowest_octave, 
                                                                                                    data.highest_note, 
                                                                                                    data.highest_octave)
            updated_display_text = "Average error: %.1f cents" % data.avg_cents
            self.settings.config(text=display_settings)
            self.score.set_text(updated_display_text)
            data.update_score_history()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        workingFrame = mainWindow.left_frame
        currentSession = mainWindow.controller.session.data
        frames_style = ttk.Style()
        frames_style.configure('DiagnosticsFrame.TFrame', background=Colors.aux)
        title_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')
        graph_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')
        settings_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')

        title_frame.grid(row=0, sticky="nsew", ipady=5)
        graph_frame.grid(row=2, sticky="nsew")
        settings_frame.grid(row=1, sticky="nsew")

        workingFrame.grid_rowconfigure(0, weight=1)
        workingFrame.grid_rowconfigure(1, weight=1)
        workingFrame.grid_rowconfigure(2, weight=1)
        workingFrame.grid_columnconfigure(0, weight=1, uniform="col")
        #workingFrame.grid_columnconfigure(1, weight=1, uniform="col")

        self.myGraph = Graph(settings_frame)
        self.myGraph.pack(side=tk.BOTTOM, anchor=tk.CENTER)
        title_label_style = ttk.Style()
        title_label_style.configure("TitleLabel.TLabel", font="Ubuntu 20", side=tk.TOP, foreground=Colors.text, background=Colors.aux)
        title_label = ttk.Label(title_frame, text="Current Session", style="TitleLabel.TLabel")
        title_label.pack()

        session_name_label_style = ttk.Style()
        session_name_label_style.configure("SessionName.TLabel", font="Ubuntu 16", foreground="light sky blue", background=Colors.aux)
        self.session_name = ttk.Label(title_frame, text=mainWindow.controller.session.name, style="SessionName.TLabel")
        self.session_name.pack()

        c = "Average error: 0.0 cents"

        display_settings = "Settings:\n" \
                           "-------------------\n" \
                           "Threshold: ±15 cents\n" \
                           "Key Signature: C Major\n" \
                           "Range: C2 to B7"


        self.score = RoundedLabel(graph_frame, c, Colors.piano_track, width=250, height=45)
        self.score.pack(anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Score.TLabel", foreground=Colors.text, background=Colors.aux)
        self.settings = ttk.Label(graph_frame, text=display_settings, style="Score.TLabel")
        self.settings.pack(side=tk.LEFT, )


