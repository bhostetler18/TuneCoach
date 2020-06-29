from gui.MoreInfoWindow import *
import tkinter as tk
from gui.constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SessionDiagnostics:
    def more_info_window_caller(self, mainWindow):
        MoreInfoWindow(mainWindow)

    def clear_plot(self):
        self.a.clear()
        self.a.set_xlim([0,10])
        self.a.set_ylim([0,100])
        self.a.set_autoscale_on(False)
        self.a.set_title("Score Over Time")
        self.canvas.draw()
        if self.mainWindow.currentPracticeSession is not None:
            self.overallScoreLabel.configure(text = "Overall Score: %.2f" % self.mainWindow.currentPracticeSession.get_overall())
        else:
            self.overallScoreLabel.configure(text = "N/A")

    def update_plot(self, new_score):
        if self.mainWindow.currentPracticeSession is not None:
            if new_score >= 0:
                self.mainWindow.currentPracticeSession._scoreList.append(new_score)
                if len(self.mainWindow.currentPracticeSession._scoreList) > 10:
                    self.mainWindow.currentPracticeSession._scoreList.pop(0)
                else:
                    self.mainWindow.currentPracticeSession._scoreIndex.append(len(self.mainWindow.currentPracticeSession._scoreIndex))
            self.clear_plot()
            self.a.plot(self.mainWindow.currentPracticeSession._scoreIndex, self.mainWindow.currentPracticeSession._scoreList, color = "blue")
            self.canvas.draw()
        else:
            self.clear_plot()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        workingFrame = mainWindow.left_frame
        currentSession = mainWindow.currentPracticeSession
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

        # Will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        title_label = tk.Label(topest_frame, text="Session Diagnostics", bg=background_color, fg="white", font=("calibri", 20))
        title_label.pack(side=tk.TOP)
        self.sessionName = tk.Label(topest_frame, text=mainWindow.currentPracticeSession._name, bg=background_color, fg="white")
        self.sessionName.pack(side=tk.BOTTOM)

        if currentSession is None:
            print("There is no session.")
            v = "Overall Score: 0.00"
        else:
            v = "Overall Score: %.2f" % currentSession.get_overall()

        self.overallScoreLabel = tk.Label(top_frame, text=v, bg=background_color, fg="white")
        self.overallScoreLabel.pack()
        more_info_button = tk.Button(middle_frame, text="More info", command=lambda: self.more_info_window_caller(mainWindow))
        more_info_button.pack()

        defaultX = [0]
        defaultY = [0]
        if mainWindow.screen_width > 1000:
            self.fig = Figure(figsize=(3, 3))
        else:
            self.fig = Figure(figsize=(2,2))
        self.a = self.fig.add_subplot(111)
        self.a.plot(defaultX, defaultY, color='blue')

        #Not sure whether or not we want it to have the same axis the whole time
        self.a.set_ylim([0, 100])
        self.a.set_xlim([0, 10])
        my_fontsize = 16
        my_axissize = 14
        if mainWindow.screen_width < 1000:
            my_fontsize = 3
            my_axissize = 3
        self.a.set_title("Score Over Time", fontsize=my_fontsize)
        self.a.set_ylabel("Score", fontsize=my_axissize)
        self.a.set_autoscale_on(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().configure(relief=tk.RIDGE, bd=5)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
