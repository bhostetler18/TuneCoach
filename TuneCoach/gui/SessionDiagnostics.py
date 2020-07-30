import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.gui.RoundedLabel import *
import tkinter.ttk as ttk
from TuneCoach.gui.Graph import *

# OUT data.update_score_history()
class SessionDiagnostics:
    def clear_plot(self):
        self.myGraph.clear_plot()
        #self.plot.clear()
        #self.plot.set_xlim([0, 10])
        #self.plot.set_ylim([0, 100])
        #self.plot.set_autoscale_on(False)
        #self.plot.set_title("Score Over Time")
        #if self.mainWindow.session.data is not None:
        #    self.overallScoreLabel.set_text("Overall Score: %.2f" % self.mainWindow.session.data.get_overall())
        #else:
        #    self.overallScoreLabel.set_text("N/A")
        #self.canvas.draw()

        #self.canvas.draw()

    def update_plot(self, data):
        self.myGraph.update_plot(data.score_history)
        if data is not None:
            self.overallScoreLabel.set_text("Overall Score: %.2f" % data.get_overall())
            self.overallCentsLabel.set_text("You are off by an average of %.2f cents." % data.avg_cents)
            display_settings = "Settings:\n" \
                               "-------------------\n" \
                               "Threshold: ±%d cents\n" \
                               "Key Signature: %s\n" \
                               "Range: %s%s to %s%s" % (data.green_thresh, data.key_signature.name, data.from_note, data.from_octave, data.to_note, data.to_octave)
            self.settings.set_text(display_settings)

            data.update_score_history()
        #    self.clear_plot()
        #    numScores = len(self.mainWindow.session.data._score_history)
        #    self.plot.plot(range(numScores), self.mainWindow.session.data._score_history, color="blue")
        #    self.canvas.draw()
        #else:
        #    self.clear_plot()
        #    self.canvas.draw()

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

        workingFrame.grid_rowconfigure(0, weight=0)
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
        self.session_name.pack()#padx=10, pady=10)

        v = "Overall Score: N/A"
        c = "You are off by an average of N/A cents"

        self.overallScoreLabel = RoundedLabel(left_frame, v, 150, 60)
        self.overallScoreLabel.pack()

        self.overallCentsLabel = RoundedLabel(left_frame, c, 300, 60)
        self.overallCentsLabel.pack()

        display_settings = "Settings:\n" \
                           "-------------------\n" \
                           "Threshold: ±15 cents\n" \
                           "Key Signature: C Major\n" \
                           "Range: C2 to B7"
        self.settings = RoundedLabel(left_frame, display_settings, 200, 125)
        self.settings.pack()


        # defaultX = [0]
        # defaultY = [0]
        # if mainWindow.screen_width > 1000:
        #     self.fig = Figure(figsize=(3, 3))
        # else:
        #     self.fig = Figure(figsize=(2, 2))
        # self.plot = self.fig.add_subplot(111)
        # self.plot.plot(defaultX, defaultY, color='blue')

        # Not sure whether or not we want it to have the same axis the whole time
        #self.plot.set_ylim([0, 100])
        #self.plot.set_xlim([0, 10])
        #my_fontsize = 16
        #my_axissize = 14
        #if mainWindow.screen_width < 1000:
        #    my_fontsize = 3
        #    my_axissize = 3
        #self.plot.set_title("Score Over Time", fontsize=my_fontsize)
        #self.plot.set_ylabel("Score", fontsize=my_axissize)
        #self.plot.set_autoscale_on(False)

        # self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        # self.canvas.get_tk_widget().configure(relief=tk.RIDGE, bd=5)
        # self.canvas.get_tk_widget().pack()
        # self.canvas.draw()

