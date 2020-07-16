#Where the graph canvas will be created
from tkinter import *

class Graph:
    def clear_plot(self):
        self.myCanvas.delete("points")
    def update_plot(self)
        pointsToPlot = self.mainWindow.session.data._score_history
    def __init__(self, frame, mainWindow, windowWidth, windowHeight):
        self.frame = frame
        self.mainWindow = mainWindow
        canvasHeight = windowHeight/3
        canvasWidth = windowWidth/4
        self.myCanvas = Canvas(self.frame, width = canvasWidth, height = canvasHeight, bg = "white")
        self.myCanvas.pack()
        self.myCanvas.create_line(30, 20,30, canvasHeight-30, fill = "black")
        self.myCanvas.create_line(30, canvasHeight-30, canvasWidth-15, canvasHeight-30, fill = "black")
        self.myCanvas.create_text(canvasWidth/2, 10,text= "Score over Time", fill = "black")

        self.myCanvas.create_text(15, 20, text = "100", fill = "black")
        self.myCanvas.create_text(15, int((canvasHeight-50)*.2+20),text = "80", fill = "black")
        self.myCanvas.create_text(15, int((canvasHeight-50)*.4+20), text = "60", fill = "black")
        self.myCanvas.create_text(15, int((canvasHeight-50)*.6+20), text = "40", fill = "black")
        self.myCanvas.create_text(15, int((canvasHeight-50)*.8+20), text = "20", fill = "black")

        self.myCanvas.create_text(20, canvasHeight-20, text = "0", fill = "black")

        self.myCanvas.create_line(30,20, 34, 20, fill = "black")
        self.myCanvas.create_line(30, int((canvasHeight-50)*.2+20), 34, int((canvasHeight-50)*.2+20), fill = "black")
        self.myCanvas.create_line(30, int((canvasHeight-50)*.4+20), 34, int((canvasHeight-50)*.4+20), fill = "black")
        self.myCanvas.create_line(30, int((canvasHeight-50)*.6+20), 34, int((canvasHeight-50)*.6+20), fill = "black")
        self.myCanvas.create_line(30, int((canvasHeight-50)*.8+20), 34, int((canvasHeight-50)*.8+20), fill = "black")

        self.myCanvas.create_text(int((canvasWidth-45)*.2+30), canvasHeight-15, text = "20", fill = "black")
        self.myCanvas.create_text(int((canvasWidth-45)*.4+30), canvasHeight-15, text = "40", fill = "black")
        self.myCanvas.create_text(int((canvasWidth-45)*.6+30), canvasHeight-15, text = "60", fill = "black")
        self.myCanvas.create_text(int((canvasWidth-45)*.8+30), canvasHeight-15, text = "80", fill = "black")
        self.myCanvas.create_text(int((canvasWidth-45)+30), canvasHeight-15, text = "100", fill = "black")

        self.myCanvas.create_line(int((canvasWidth-45)*.2+30), canvasHeight-30, int((canvasWidth-45)*.2+30), canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((canvasWidth-45)*.4+30), canvasHeight-30, int((canvasWidth-45)*.4+30), canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((canvasWidth-45)*.6+30), canvasHeight-30, int((canvasWidth-45)*.6+30), canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((canvasWidth-45)*.8+30), canvasHeight-30, int((canvasWidth-45)*.8+30), canvasHeight-34, fill = "black")
        self.myCanvas.create_line(int((canvasWidth-45)+30), canvasHeight-29, int((canvasWidth-45)+30), canvasHeight-34, fill = "black")

