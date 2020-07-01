from TuneCoach.gui.MoreInfoWindow import *
import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.gui.ScoreLabel import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SessionDiagnostics:
    @staticmethod
    def more_info_window_caller(mainWindow):
        MoreInfoWindow(mainWindow)

    def clear_plot(self):
        self.plot.clear()
        self.plot.set_xlim([0, 10])
        self.plot.set_ylim([0, 100])
        self.plot.set_autoscale_on(False)
        self.plot.set_title("Score Over Time")
        if self.mainWindow.session.data is not None:
            self.overallScoreLabel.set_text("Overall Score: %.2f" % self.mainWindow.session.data.get_overall())
        else:
            self.overallScoreLabel.set_text("N/A")
        self.canvas.draw()

    def update_plot(self):
        if self.mainWindow.session.data is not None:
            new_score = self.mainWindow.session.data.get_overall()
            self.overallScoreLabel.set_text("Overall Score: %.2f" % new_score)
            self.mainWindow.session.data.update_score_history()
            self.clear_plot()
            numScores = len(self.mainWindow.session.data._score_history)
            self.plot.plot(range(numScores), self.mainWindow.session.data._score_history, color="blue")
            self.canvas.draw()
        else:
            self.clear_plot()
            self.canvas.draw()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        workingFrame = mainWindow.left_frame
        currentSession = mainWindow.session.data
        topest_frame = tk.Frame(workingFrame, bd=5, bg=background_color)
        top_frame = tk.Frame(workingFrame, bd=5, bg=background_color)
        right_frame = tk.Frame(workingFrame, bd=5, bg=background_color)
        middle_frame = tk.Frame(workingFrame, bd=5, bg=background_color)
        bottom_frame = tk.Frame(workingFrame, bd=5, bg=background_color)

        topest_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        top_frame.grid(row=1, column=0, sticky="nsew")
        right_frame.grid(row=1, column=1, rowspan=3, sticky="nsew")
        middle_frame.grid(row=2, column=0, sticky="nsew")
        bottom_frame.grid(row=3, column=0, sticky="nsew")

        workingFrame.grid_rowconfigure(0, weight=1)
        workingFrame.grid_rowconfigure(1, weight=1)
        workingFrame.grid_rowconfigure(2, weight=1)
        workingFrame.grid_rowconfigure(3, weight=1)
        workingFrame.grid_columnconfigure(0, weight=1)
        workingFrame.grid_columnconfigure(1, weight=2)

        title_label = tk.Label(topest_frame, text="Session Diagnostics", bg=background_color, fg="white",
                               font=("calibri", 20))
        title_label.pack(side=tk.TOP)
        self.session_name = tk.Label(topest_frame, text=mainWindow.session.name, bg=background_color,
                                    fg="light sky blue", font=("Calibri", 16))
        self.session_name.pack(side=tk.BOTTOM)

        if currentSession is None:
            # print("There is no session.")
            v = "Overall Score: 0.00"
        else:
            v = "Overall Score: %.2f" % currentSession.get_overall()

        self.overallScoreLabel = ScoreLabel(top_frame, v, 150, 60)
        self.overallScoreLabel.pack()
        more_info_button = tk.Button(middle_frame, text="More info",
                                     command=lambda: self.more_info_window_caller(mainWindow))
        more_info_button.pack()

        defaultX = [0]
        defaultY = [0]
        if mainWindow.screen_width > 1000:
            self.fig = Figure(figsize=(3, 3))
        else:
            self.fig = Figure(figsize=(2,2))
        self.plot = self.fig.add_subplot(111)
        self.plot.plot(defaultX, defaultY, color='blue')

        # Not sure whether or not we want it to have the same axis the whole time
        self.plot.set_ylim([0, 100])
        self.plot.set_xlim([0, 10])
        my_fontsize = 16
        my_axissize = 14
        #if mainWindow.screen_width < 1000:
        #    my_fontsize = 3
        #    my_axissize = 3
        self.plot.set_title("Score Over Time", fontsize=my_fontsize)
        self.plot.set_ylabel("Score", fontsize=my_axissize)
        self.plot.set_autoscale_on(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().configure(relief=tk.RIDGE, bd=5)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
