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
            self.score.set_text("Average error: %.1f cents" % data.avg_cents)
            self.thresh_label.set_text("Threshold: ±%d cents" % data.green_thresh)
            self.key_label.set_text("Key Signature: %s" % data.key_signature.name)
            self.range_label.set_text("Range: %s%s to %s%s" % (data.lowest_note, 
                                                              data.lowest_octave, 
                                                              data.highest_note, 
                                                              data.highest_octave))
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

        title_frame.grid(row=0, sticky="nsew", ipady=2.5)
        graph_frame.grid(row=1, sticky="nsew", ipady=2.5)
        settings_frame.grid(row=2, sticky="nsew", ipady=7.5, ipadx=2.5)

        workingFrame.grid_rowconfigure(0, weight=0)
        workingFrame.grid_rowconfigure(1, weight=1)
        workingFrame.grid_rowconfigure(2, weight=0)
        workingFrame.grid_columnconfigure(0, weight=1)

        self.myGraph = Graph(graph_frame)
        self.myGraph.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True, padx=20)
        title_label_style = ttk.Style()
        title_label_style.configure("TitleLabel.TLabel", font="Ubuntu 20", side=tk.TOP, foreground=Colors.text, background=Colors.aux)
        title_label = ttk.Label(title_frame, text="Current Session", style="TitleLabel.TLabel")
        title_label.pack()

        session_name_label_style = ttk.Style()
        session_name_label_style.configure("SessionName.TLabel", font="Ubuntu 16", foreground="light sky blue", background=Colors.aux)
        self.session_name = ttk.Label(title_frame, text=mainWindow.controller.session.name, style="SessionName.TLabel")
        self.session_name.pack()

        self.score = RoundedLabel(graph_frame, "Average error: 0.0 cents", Colors.score_label, width=225, height=35)
        self.score.pack()

        self.thresh_label = RoundedLabel(settings_frame, "Threshold: ±15 cents", Colors.settings_color, height=45)
        self.thresh_label.grid(row=0, column=0, sticky='ew', padx=5)

        self.key_label = RoundedLabel(settings_frame, "Key Signature: C Major", Colors.settings_color, height=45)
        self.key_label.grid(row=0, column=1, sticky='ew', padx=5)

        self.range_label = RoundedLabel(settings_frame, "Range: C2 to B7", Colors.settings_color, height=45)
        self.range_label.grid(row=0, column=2, sticky='ew', padx=5)

        settings_frame.grid_rowconfigure(0, weight=1)
        for i in range(0, 3):
            settings_frame.grid_columnconfigure(i, weight=1, uniform="settings_labels")
 


