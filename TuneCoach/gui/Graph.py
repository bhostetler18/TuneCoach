import tkinter as tk
from TuneCoach.gui.constants import *

class Graph(tk.Canvas):
    def clear_plot(self):
        self.delete("points")
    
    def update_plot(self, score_history):
        # self.session.data.update_score_history()
        numScores = len(score_history)
        self.cached_scores = score_history
        self.clear_plot()
        if numScores != 0:
            for i in range(0, numScores-1):
                yCoord = int((1 - (score_history[i])/100) * (self.canvasHeight-40)+10)
                xCoord = int ((i)/(self.scores_to_display-1) * (self.canvasWidth - 55)) + 40
                nextY = int((1-(score_history[i+1])/100)*(self.canvasHeight-40)+10)
                nextX = int((i+1)/(self.scores_to_display-1)*(self.canvasWidth-55))+40
                self.create_circle(xCoord, yCoord, 4)
                self.create_line(xCoord, yCoord, nextX, nextY, tag = "points", fill=Colors.graph_foreground)
            yCoord = int((1-(score_history[numScores-1])/100) * (self.canvasHeight-40)+10)
            xCoord = int((numScores-1)/(self.scores_to_display-1)*(self.canvasWidth-55))+40
            self.create_circle(xCoord, yCoord,4)

    def create_circle(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.create_oval(x0, y0, x1, y1, tag = "points", fill=Colors.graph_foreground, outline="")

    def __init__(self, frame, **kwargs):
        super().__init__(frame, kwargs, bg=Colors.graph_background, bd=0, highlightthickness=0)
        self.frame = frame
        self.canvasHeight = self.winfo_height()
        self.canvasWidth = self.winfo_width()
        self.cached_scores = []
        self.scores_to_display = 15
        self.pack()
        self.draw(None)
        self.bind("<Configure>", self.draw)

    def draw(self, event):
        self.delete("all")
        self.canvasHeight = self.winfo_height()
        self.canvasWidth = self.winfo_width()

        self.create_line(40, 10, 40, self.canvasHeight-30, fill=Colors.graph_foreground)
        self.create_line(40, self.canvasHeight-30, self.canvasWidth-15, self.canvasHeight-30, fill = Colors.graph_foreground)
        self.create_text(self.canvasWidth/2, self.canvasHeight-15,text= "Total Score over Time", fill=Colors.graph_foreground)

        self.create_text(20, 10, text = "100%", fill = Colors.graph_foreground)
        self.create_text(20, int((self.canvasHeight-40)*.2+10),text = "80%", fill=Colors.graph_foreground)
        self.create_text(20, int((self.canvasHeight-40)*.4+10), text = "60%", fill=Colors.graph_foreground)
        self.create_text(20, int((self.canvasHeight-40)*.6+10), text = "40%", fill=Colors.graph_foreground)
        self.create_text(20, int((self.canvasHeight-40)*.8+10), text = "20%", fill=Colors.graph_foreground)

        self.create_text(20, int((self.canvasHeight-40)+10), text = "0", fill = Colors.graph_foreground)

        self.create_line(40, 10, 44, 10, fill=Colors.graph_foreground")
        self.create_line(40, int((self.canvasHeight-40)*.2+20), 34, int((self.canvasHeight-40)*.2+20), fill=Colors.graph_foreground)
        self.create_line(40, int((self.canvasHeight-40)*.4+20), 34, int((self.canvasHeight-40)*.4+20), fill=Colors.graph_foreground)
        self.create_line(40, int((self.canvasHeight-40)*.6+20), 34, int((self.canvasHeight-40)*.6+20), fill=Colors.graph_foreground)
        self.create_line(40, int((self.canvasHeight-40)*.8+20), 34, int((self.canvasHeight-40)*.8+20), fill=Colors.graph_foreground)

        #self.create_line(int((self.canvasWidth-45)+30), self.canvasHeight-29, int((self.canvasWidth-45)+30), self.canvasHeight-34, fill = "black")

        self.update_plot(self.cached_scores) # So that redrawing while data isn't coming in doesn't clear existing points
