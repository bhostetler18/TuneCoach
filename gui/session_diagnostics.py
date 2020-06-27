from more_info_window import *
import tkinter as tk
from constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class session_diagnostics:
    def more_info_window_caller(self,master, obj):
        myMoreInfoWindow = more_info_window(master, obj)
    def update_plot(self, new_score, master):
        if master.practiceSession is not None:
            master.practiceSession._scoreList.append(new_score)
            if len(master.practiceSession._scoreList) > 10:
                master.practiceSession._scoreList.pop(0)
            else:
                master.practiceSession._scoreIndex.append(len(master.practiceSession._scoreIndex))
            self.a.clear()
            self.a.set_xlim([0,10])
            self.a.set_ylim([0,100])
            self.a.set_autoscale_on(False)
            self.a.set_title("Score Over Time")
            self.a.set_ylabel("Score")
            self.a.plot( master.practiceSession._scoreIndex, master.practiceSession._scoreList, color = "blue")
            self.canvas.draw()
    def __init__(self, workingFrame, obj, master):
        #testLabel = tk.Label(workingFrame, text = "testing", bg = background_color, fg = "white")
        #testLabel.pack()
        topestFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        topFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        rightFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)
        middleFrame = tk.Frame(workingFrame, bd = 5, bg= background_color)
        bottomFrame = tk.Frame(workingFrame, bd = 5, bg = background_color)

        topestFrame.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")
        topFrame.grid(row = 1, column = 0, sticky = "nsew")
        rightFrame.grid(row = 1, column = 1, rowspan = 3, sticky = "nsew")
        middleFrame.grid(row = 2, column = 0, sticky = "nsew")
        bottomFrame.grid(row = 3, column = 0, sticky = "nsew")

        workingFrame.grid_rowconfigure(0, weight = 1)
        workingFrame.grid_rowconfigure(1, weight = 1)
        workingFrame.grid_rowconfigure(2, weight = 1)
        workingFrame.grid_rowconfigure(3, weight = 1)
        workingFrame.grid_columnconfigure(0, weight = 1)
        workingFrame.grid_columnconfigure(1, weight = 2)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.
        titleLabel = tk.Label(topestFrame, text = "Session Diagnostics", bg = background_color, fg = "white", font = ("calibri", 20))
        titleLabel.pack(side = tk.TOP)
        self.sessionName = tk.Label(topestFrame, text = "No Practice Session Selected",bg = background_color, fg = "white" )
        self.sessionName.pack(side  = tk.BOTTOM)
        #v = tk.StringVar()
        v = "Overall Score: %.2f" % obj.get_overall()
        self.overallScoreLabel = tk.Label(topFrame, text = v, bg = background_color, fg = "white")
        self.overallScoreLabel.pack()
        moreInfoButton = tk.Button(middleFrame,text = "More info", command = lambda : self.more_info_window_caller(master, obj))
        moreInfoButton.pack()
        defaultX = [0]
        defaultY = [0]
        self.fig = Figure(figsize=(3,3))
        self.a = self.fig.add_subplot(111)
        self.a.plot(defaultX,defaultY,color='blue')
        #not sure whether or not we want it to have the same axis the whole time
        self.a.set_ylim([0,100])
        self.a.set_xlim([0,10])
        self.a.set_title ("Score Over Time", fontsize=16)
        self.a.set_ylabel("Score", fontsize=14)
        self.a.set_autoscale_on(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=rightFrame)
        self.canvas.get_tk_widget().configure(relief = tk.RIDGE, bd = 5)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
