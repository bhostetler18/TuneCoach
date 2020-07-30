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
                               "Range: %s%s to %s%s" % (data.threshold, data.key_signature.name, data.from_note, data.from_octave, data.to_note, data.to_octave)
            updated_disply_text = "Overall Score: %.2f" % data.get_overall() + '\n'\
                + "You are off by an average of %.2f cents." % data.avg_cents + '\n' \
                + display_settings

            self.summary.set_text(updated_disply_text)
            data.update_score_history()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        workingFrame = mainWindow.left_frame
        currentSession = mainWindow.controller.session.data
        frames_style = ttk.Style()
        frames_style.configure('DiagnosticsFrame.TFrame', background=Colors.aux)
        title_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')
        left_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')
        right_frame = ttk.Frame(workingFrame, style='DiagnosticsFrame.TFrame')

        title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        left_frame.grid(row=1, column=0, rowspan=3, sticky="nsew")
        right_frame.grid(row=1, column=1, rowspan=3, sticky="nsew")

        workingFrame.grid_rowconfigure(0, weight=1)
        workingFrame.grid_rowconfigure(1, weight=1)
        workingFrame.grid_rowconfigure(2, weight=1)
        workingFrame.grid_rowconfigure(3, weight=1)
        workingFrame.grid_columnconfigure(0, weight=1)
        workingFrame.grid_columnconfigure(1, weight=1)

        self.myGraph = Graph(right_frame)
        self.myGraph.pack(expand=True, anchor=tk.CENTER, fill=tk.BOTH)
        title_label_style = ttk.Style()
        title_label_style.configure("TitleLabel.TLabel", font="Ubuntu 20", side=tk.TOP, foreground=Colors.text, background=Colors.aux)
        title_label = ttk.Label(title_frame, text="Session Diagnostics", style="TitleLabel.TLabel")
        title_label.pack()

        session_name_label_style = ttk.Style()
        session_name_label_style.configure("SessionName.TLabel", font="Ubuntu 16", foreground="light sky blue", background=Colors.aux)
        self.session_name = ttk.Label(title_frame, text=mainWindow.controller.session.name, style="SessionName.TLabel")
        self.session_name.pack()

        v = "Overall Score: N/A"
        c = "You are off by an average of N/A cents"

        display_settings = "Settings:\n" \
                           "-------------------\n" \
                           "Threshold: ±15 cents\n" \
                           "Key Signature: C Major\n" \
                           "Range: C2 to B7"

        self.summary = RoundedLabel(left_frame, v + '\n' + c + '\n' + display_settings, 300, 130)
        self.summary.pack()

