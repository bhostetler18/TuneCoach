import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.gui.ScoreLabel import *
from TuneCoach.gui.Graph import *


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
        data = self.mainWindow.controller.session.data
        if data is not None:
            self.overallScoreLabel.set_text("Overall Score: %.2f" % data.get_overall())
            self.overallCentsLabel.set_text("You are off by an average of %.2f cents." % data.avg_cents)
            self.key_signature.set_text("Key Signature: %s" % data.key_signature)
        else:
            self.overallScoreLabel.set_text("N/A")
            self.overallCentsLabel.set_text("N/A")
        #self.canvas.draw()

    def update_plot(self, data):
        self.myGraph.update_plot()
        if data is not None:
            new_score = data.get_overall()
            self.overallScoreLabel.set_text("Overall Score: %.2f" % new_score)
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

        self.myGraph = Graph(right_frame, mainWindow, mainWindow.screen_width, mainWindow.screen_height)

        title_label = tk.Label(topest_frame, text="Session Diagnostics", bg=background_color, fg="white",
                               font=("calibri", 20))
        title_label.pack(side=tk.TOP)
        self.session_name = tk.Label(topest_frame, text=mainWindow.controller.session.name, bg=background_color,
                                    fg="light sky blue", font=("Calibri", 16))
        self.session_name.pack(side=tk.BOTTOM, padx=10, pady=10)

        v = "Overall Score: %.2f" % currentSession.get_overall()
        c = "You are off by an average of %.2f cents." % currentSession.avg_cents

        self.overallScoreLabel = ScoreLabel(top_frame, v, 150, 60)
        self.overallScoreLabel.pack()

        self.overallCentsLabel = ScoreLabel(middle_frame, c, 300, 60)
        self.overallCentsLabel.pack()

        key_signature = "Key Signature: %s" % currentSession.key_signature.name
        self.key_signature = ScoreLabel(bottom_frame, key_signature, 200, 60)
        self.key_signature.pack()


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

