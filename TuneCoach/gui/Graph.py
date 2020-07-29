from tkinter import *


class Graph:
    def clear_plot(self):
        self.myCanvas.delete("points")
    
    def update_plot(self, score_history):
        # self.session.data.update_score_history()
        numScores = len(score_history)
        self.clear_plot()
        if numScores != 0:
            for i in range(0, numScores-1):
                yCoord = int((1 - (score_history[i])/100) * (self.canvasHeight-50)+20)
                xCoord = int ((i)/9 * (self.canvasWidth - 45)) + 30
                nextY = int((1-(score_history[i+1])/100)*(self.canvasHeight-50)+20)
                nextX = int((i+1)/9*(self.canvasWidth-45))+30
                self.create_circle(xCoord, yCoord, 4)
                self.myCanvas.create_line(xCoord, yCoord, nextX, nextY, tag = "points")
            yCoord = int((1-(score_history[numScores-1])/100) * (self.canvasHeight-50)+20)
            xCoord = int((numScores-1)/9*(self.canvasWidth-45))+30
            self.create_circle(xCoord, yCoord,4)

    def create_circle(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.myCanvas.create_oval(x0, y0, x1, y1, tag = "points", fill = "black")
    def __init__(self, frame, mainWindow, windowWidth, windowHeight):
        self.frame = frame
        self.mainWindow = mainWindow
        self.canvasHeight = windowHeight/3
        self.canvasWidth = windowWidth/4
        self.myCanvas = Canvas(self.frame, width = self.canvasWidth, height = self.canvasHeight, bg = "white")
        self.myCanvas.pack()
        self.myCanvas.create_line(30, 20,30, self.canvasHeight-30, fill = "black")
        self.myCanvas.create_line(30, self.canvasHeight-30, self.canvasWidth-15, self.canvasHeight-30, fill = "black")
        self.myCanvas.create_text(self.canvasWidth/2, 10,text= "Score over Time", fill = "black")

        self.myCanvas.create_text(15, 20, text = "100", fill = "black")
        self.myCanvas.create_text(15, int((self.canvasHeight-50)*.2+20),text = "80", fill = "black")
        self.myCanvas.create_text(15, int((self.canvasHeight-50)*.4+20), text = "60", fill = "black")
        self.myCanvas.create_text(15, int((self.canvasHeight-50)*.6+20), text = "40", fill = "black")
        self.myCanvas.create_text(15, int((self.canvasHeight-50)*.8+20), text = "20", fill = "black")

        self.myCanvas.create_text(20, self.canvasHeight-20, text = "0", fill = "black")

        self.myCanvas.create_line(30,20, 34, 20, fill = "black")
        self.myCanvas.create_line(30, int((self.canvasHeight-50)*.2+20), 34, int((self.canvasHeight-50)*.2+20), fill = "black")
        self.myCanvas.create_line(30, int((self.canvasHeight-50)*.4+20), 34, int((self.canvasHeight-50)*.4+20), fill = "black")
        self.myCanvas.create_line(30, int((self.canvasHeight-50)*.6+20), 34, int((self.canvasHeight-50)*.6+20), fill = "black")
        self.myCanvas.create_line(30, int((self.canvasHeight-50)*.8+20), 34, int((self.canvasHeight-50)*.8+20), fill = "black")

        self.myCanvas.create_text(int((self.canvasWidth-45)*.2+30), self.canvasHeight-15, text = "20", fill = "black")
        self.myCanvas.create_text(int((self.canvasWidth-45)*.4+30), self.canvasHeight-15, text = "40", fill = "black")
        self.myCanvas.create_text(int((self.canvasWidth-45)*.6+30), self.canvasHeight-15, text = "60", fill = "black")
        self.myCanvas.create_text(int((self.canvasWidth-45)*.8+30), self.canvasHeight-15, text = "80", fill = "black")
        self.myCanvas.create_text(int((self.canvasWidth-45)+30), self.canvasHeight-15, text = "100", fill = "black")

        self.myCanvas.create_line(int((self.canvasWidth-45)*.2+30), self.canvasHeight-30, int((self.canvasWidth-45)*.2+30), self.canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((self.canvasWidth-45)*.4+30), self.canvasHeight-30, int((self.canvasWidth-45)*.4+30), self.canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((self.canvasWidth-45)*.6+30), self.canvasHeight-30, int((self.canvasWidth-45)*.6+30), self.canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((self.canvasWidth-45)*.8+30), self.canvasHeight-30, int((self.canvasWidth-45)*.8+30), self.canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((self.canvasWidth-45)+30), self.canvasHeight-29, int((self.canvasWidth-45)+30), self.canvasHeight-34, fill = "black")

