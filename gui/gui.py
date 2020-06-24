#main gui for our project, tuneCoach. Made by the group , Jamm Hostetler , James Eschrich, Joe Gravelle, Jenny Baik, Gavin Gui

import tkinter as tk
import tkinter.ttk as ttk
import PIL.Image
import PIL.ImageTk
from datetime import date
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pitchDisplay import *

#constants, will move to appriate constants file.
background_color = "#575759"
#just made it the halfway point for default, can change to what you guys think is best
acceptable_pitch_range = 25
#not sure what this number will mean, but we should be able to filter how loud of noises we account for.
noise_filter_level = 20

#store a list of session objects
session_history_list = []


#open the tuner settings window
#wrapper functions to create settings windows

def tuner_settings(self, master):
    settingsWindow = tuner_settings_window(master)

def update_pitch_settings(newPitch, newFilterLevel, oldSettingsView):
    acceptable_pitch_range = newPitch
    noise_filter_level = newFilterLevel
    oldSettingsView.destroy()
    
def new_practice_session(master):
    newPracticeSessionWindow = new_session_window(master)


def load_practice_session(master):
    loadPracticeSessionWindow = load_session_window(master) 

def end_practice_session(master):
    end_session_window(master)

def change_layout():
    print("this will change the layout")
    
def user_settings():
    print("function to display menu to change user settings")

def load_faq():
    print("function to load app faq")

def load_tutorial():
    print("function to load a tutorial for how to use the app")      

#additional functions

def creating_a_new_session(oldWindow, newName):
    oldWindow.destroy()
    mySession = new_practice_session(newName)
    reset_practice_session(mySession)

def reset_practice_session(newPracticeSession):
    print("will set up the selected practice session in the bottom and left frames.")


#class to create practice session objects. Will hold all the data for each practice session
class practice_session:
    def __init__(self, name):
        #note history can hold numbers corresponding to the appropriate notes. 1 = C, 2 = C#... I think it would be cool to add in a break point to signify a stop in the practice sesion, like a 13 or something.
        self._noteHistory = []
        #pitches can hold a int value of how off the cents are for the note in noteHistory of the same index.
        self._notePitches = []
        self._name = name
        self._date = date.today()

        #see about adding raw data

#dfferent classes for pop-up windows.
class session_history:
    def create_circle(self, x, y, r, canvasName, fillColor): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, fill = fillColor)
    
    def __init__(self, workingFrame, width, height):
        canvas = tk.Canvas(workingFrame,width = width/2, height = height/4, relief = tk.RIDGE, bd = 5, bg = "#bdd0df")
        canvas.pack(side = tk.LEFT, padx = width/4)
        largeImage = PIL.Image.open("piano.jpeg")
        largeImage = largeImage.resize((int(width/10),int(height/3.9)), PIL.Image.ANTIALIAS)
        pianoImage = PIL.ImageTk.PhotoImage(largeImage)

        canvas.create_image(0, 0, anchor = tk.NW, image = pianoImage)
        
        noteDict = {
            "C" : height/3.9/15,
            "C#" : height/3.9/15*2.1,
            "D" : height/3.9/15*3.2,
            "D#" : height/3.9/15*4.3,
            "E" : height/3.9/15*5.6,
            "F" : height/3.9/15*7.1,
            "F#" : height/3.9/15*8.4,
            "G" : height/3.9/15*9.5,
            "G#" : height/3.9/15*10.6,
            "A" : height/3.9/15*11.7,
            "A#" : height/3.9/15*12.7,
            "B" : height/3.9/15*14

        }
        canvas.create_line(width/10, noteDict["C"], width/2, noteDict["C"], width = 3)
        canvas.create_line(width/10, noteDict["C#"], width/2, noteDict["C#"], width = 3)
        canvas.create_line(width/10, noteDict["D"], width/2, noteDict["D"], width = 3)
        canvas.create_line(width/10, noteDict["D#"], width/2, noteDict["D#"], width = 3)
        canvas.create_line(width/10, noteDict["E"], width/2, noteDict["E"], width = 3)
        canvas.create_line(width/10, noteDict["F"], width/2, noteDict["F"], width = 3)
        canvas.create_line(width/10, noteDict["F#"], width/2, noteDict["F#"], width = 3)
        canvas.create_line(width/10, noteDict["G"], width/2, noteDict["G"], width = 3)
        canvas.create_line(width/10, noteDict["G#"], width/2, noteDict["G#"], width = 3)
        canvas.create_line(width/10, noteDict["A"], width/2, noteDict["A"], width = 3)
        canvas.create_line(width/10, noteDict["A#"], width/2, noteDict["A#"], width = 3)
        canvas.create_line(width/10, noteDict["B"], width/2, noteDict["B"], width = 3)


        noteArray = ["F#", "A", "B", "A", "F#","F#", "A", "B", "A","B","F#", "F#", "A", "B", "C#", "D", "A", "F#", "D", "F#", "G", "F#", "E"]
        colorArray = ["green", "red", "green", "green", "red", "green", "green", "red", "blue", "green", "green", "green", "blue", "green", "green", "red", "green", "red", "blue", "green", "green", "red", "blue", "green"]
        i = 0
        while i < len(noteArray):
            self.create_circle(width/10 + (i+1)*20, noteDict[noteArray[i]], 10, canvas,colorArray[i])
            i = i+1

        canvas.image = pianoImage


class session_diagnostics:
    def __init__(self, workingFrame):
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
        overallScoreLabel = tk.Label(topFrame, text = "overall score: 90", bg = background_color, fg = "white")
        overallScoreLabel.pack()
        mostMissedLabel = tk.Label(middleFrame,text = "most missed note: A", bg = background_color, fg = "white")
        mostMissedLabel.pack()
        mostMissedTransition = tk.Label(bottomFrame, text = "most missed jump: D to A", bg = background_color, fg = "white")
        mostMissedTransition.pack()
        
        Oder = np.array([1,2,3,4,5])
        Score = np.array([100, 95, 93, 94, 96])

        fig = Figure(figsize=(3,3))
        a = fig.add_subplot(111)
        a.plot(Oder,Score,color='blue')
        #not sure whether or not we want it to have the same axis the whole time
        #a.set_ylim([0,100])

        a.set_title ("Score over time", fontsize=16)
        a.set_ylabel("Score", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=rightFrame)
        canvas.get_tk_widget().configure(relief = tk.RIDGE, bd = 5)
        canvas.get_tk_widget().pack()
        canvas.draw()


#settings window to create a new session
class new_session_window(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        new_sesh_window = tk.Toplevel(master)
        new_sesh_window.geometry("500x100")
        topFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)
        leftFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(new_sesh_window, bd = 5, bg= background_color)
        rightFrame = tk.Frame(new_sesh_window, bd = 5, bg = background_color)

        topFrame.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")
        leftFrame.grid(row = 1, column = 0, sticky = "nsew")
        middleFrame.grid(row = 1, column = 1, sticky = "nsew")
        rightFrame.grid(row = 1, column = 2, sticky = "nsew")
        
        new_sesh_window.grid_rowconfigure(0, weight = 1)
        new_sesh_window.grid_rowconfigure(1, weight = 3)
        new_sesh_window.grid_columnconfigure(0, weight = 1)
        new_sesh_window.grid_columnconfigure(1, weight = 1)
        new_sesh_window.grid_columnconfigure(2, weight = 1)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame,text = "Create New Session", bg = background_color, fg = "white")
        createSessionLabel.pack()
        new_sesh_window.lift(master)
        textEntryLabel = tk.Label(leftFrame, text = "Enter name of new Session", fg = "white", bg = background_color)
        textEntryLabel.pack()
        textEntry = tk.Entry(middleFrame)
        textEntry.insert(tk.END, "new-session-1")
        textEntry.pack()
        enterEntry = tk.Button(rightFrame, text = "Enter", command = lambda: creating_a_new_session(new_sesh_window,textEntry.get()))
        enterEntry.pack()

        new_sesh_window.lift(master)

#settings window to load new session
class load_session_window(tk.Toplevel):
    def __init__(self, master):
        self.master = master

        load_window = tk.Toplevel(master)
        topFrame = tk.Frame(load_window, bd = 5, bg = background_color)
        leftFrame = tk.Frame(load_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(load_window, bd = 5, bg= background_color)
        rightFrame = tk.Frame(load_window, bd = 5, bg = background_color)

        topFrame.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")
        leftFrame.grid(row = 1, column = 0, sticky = "nsew")
        middleFrame.grid(row = 1, column = 1, sticky = "nsew")
        rightFrame.grid(row = 1, column = 2, sticky = "nsew")
        
        load_window.grid_rowconfigure(0, weight = 1)
        load_window.grid_rowconfigure(1, weight = 3)
        load_window.grid_columnconfigure(0, weight = 1)
        load_window.grid_columnconfigure(1, weight = 1)
        load_window.grid_columnconfigure(2, weight = 1)

        #will sub out these stand-ins for values once we get set up how and where we will store practice sessions.

        createSessionLabel = tk.Label(topFrame,text = "Load Previous Session", bg = background_color, fg = "white")
        createSessionLabel.pack()
        if len(session_history_list) > 0:
            selectSessionLabel = tk.Label(leftFrame, text = "Select a session to load", bg = background_color, fg = "white")
            selectSessionLabel.pack()
            firstSession = session_history[0]
            loadSessionDropDown = tk.OptionMenu(middleFrame, firstSession, session_history)
            loadSessionDropDown.pack()
            acceptButton = tk.Button(text = "Select", command = lambda: reset_practice_session(loadSessionDropDown.get()))
            acceptButton.pack()
        else:
            standInLabel = tk.Label(middleFrame, text = "No sessions to choose from.", fg = "white", bg = background_color)    
            standInLabel.pack()

        load_window.lift(master)

#settings window to end current session
class end_session_window(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        self.end_sesh_window = tk.Toplevel(master)
        self.end_sesh_window.configure(bg = background_color)
        self.end_sesh_window.geometry("200x100")
        topFrame = tk.Frame(self.end_sesh_window, bg = background_color, bd = 5)
        bottomFrame = tk.Frame(self.end_sesh_window, bg = background_color, bd = 5)
        topFrame.grid(row =0, sticky = "nsew")
        bottomFrame.grid(row =1, sticky = "nsew")
        self.end_sesh_window.grid_rowconfigure(0, weight = 1)
        self.end_sesh_window.grid_rowconfigure(1,weight = 1)
        successLabel = tk.Label(topFrame, text = "Session ended successfully.", fg = "white", bg= background_color)
        successLabel.pack()
        endButton = tk.Button(bottomFrame, text = "Ok", command = lambda : self.end_sesh_window.destroy())
        endButton.pack()

#tuner settings window
class tuner_settings_window(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        tuner_settings_window = tk.Toplevel(master)
        tuner_settings_window.geometry("500x300")

        topFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        middleFrame = tk.Frame(tuner_settings_window, bd = 5,bg =  background_color)
        middleFrame1 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        middleFrame2 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame1 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomFrame2 = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)
        bottomestFrame = tk.Frame(tuner_settings_window, bd = 5, bg = background_color)

        #putting the frames into a grid layout

        topFrame.grid(row = 0, column = 0, columnspan = 3, sticky = "nsew")
        middleFrame.grid(row = 1, column = 0, columnspan = 1,sticky = "nsew")
        middleFrame1.grid(row = 1, column = 1, sticky = "nsew")
        middleFrame2.grid(row = 1, column = 2, sticky = "snew")
        bottomFrame.grid(row = 2, column = 0,sticky = "nsew")
        bottomFrame1.grid(row = 2, column = 1, sticky = "nsew")
        bottomFrame2.grid(row = 2, column = 2, sticky = "nsew")
        bottomestFrame.grid(row = 3, column = 0, columnspan = 3, sticky = "nsew")

        #setting up grid weights.

        tuner_settings_window.grid_rowconfigure(0, weight = 1)
        tuner_settings_window.grid_rowconfigure(1, weight = 5)
        tuner_settings_window.grid_rowconfigure(2, weight = 5)
        tuner_settings_window.grid_rowconfigure(3, weight = 1)
        tuner_settings_window.grid_columnconfigure(0, weight = 1)
        tuner_settings_window.grid_columnconfigure(1, weight = 1)
        tuner_settings_window.grid_columnconfigure(2, weight = 1)

        tuner_label = tk.Label(topFrame, text = "Tuner Settings", font=("Calibri", 20))
        tuner_label.config(bg = background_color, fg = "white")
        tuner_label.pack()


        centsitivity = tk.Label(middleFrame, text = "Margin of Acceptable Pitch Error +- ")
        centsitivity.config(bg = background_color, fg= "white")
        centsitivity.pack()

        pitch_sensitivity_scale = tk.Scale(middleFrame1, from_= 0, to_ = 40, orient = tk.HORIZONTAL)
        pitch_sensitivity_scale.config(bg = background_color, fg = "white")
        pitch_sensitivity_scale.pack()

        inCents = tk.Label(middleFrame2, text = "cents")
        inCents.config(bg = background_color, fg = "white")
        inCents.pack()

        outside_noise_filter_level = tk.Label(bottomFrame, text = "Pitch Detection Threshold")
        outside_noise_filter_level.config(bg = background_color, fg = "white")
        outside_noise_filter_level.pack()

        outside_noise_scale = tk.Scale(bottomFrame1, from_= 0, to_ = 40, orient = tk.HORIZONTAL)
        outside_noise_scale.config(bg = background_color, fg = "white")
        outside_noise_scale.pack()        

        inCents = tk.Label(bottomFrame2, text = "decibals")
        inCents.config(bg = background_color, fg = "white")
        inCents.pack()
        
        doneButton = ttk.Button(bottomestFrame, text = "Apply", command = lambda: update_pitch_settings(pitch_sensitivity_scale.get(), outside_noise_scale.get(),tuner_settings_window))
        doneButton.pack()

        tuner_settings_window.lift(master)

#main gui
class main_window(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        
        
        master.title("TuneCoach")
        master.geometry(f'{screen_width}x{screen_height}')
    
        self.create_menubar(self.master)
        self.layout_frames(self.master, screen_width, screen_height)

    #adding menu options to the top of the screen.
    
    def create_menubar(self, master):    
        menubar = tk.Menu(master)

        master.config(menu=menubar)

        file_menu = tk.Menu(menubar)

        #file menubar
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Practice Session", command = lambda: new_practice_session(master))
        file_menu.add_separator
        file_menu.add_command(label="End Practice Session", command = lambda: end_practice_session(master))
        file_menu.add_separator
        file_menu.add_command(label="Load Practice Session", command = lambda: load_practice_session(master))
        file_menu.add_separator
        file_menu.add_command(label="Exit", command = master.quit)

        #settings menubar
        settings_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Tuner Settings", command = lambda: tuner_settings(self, master))
        settings_menu.add_separator
        settings_menu.add_command(label="User Settings", command = user_settings)
        settings_menu.add_separator

        #view menubar
        view_menu = tk.Menu(menubar)
        menubar.add_cascade(label="View", menu = view_menu)
        view_menu.add_command(label="Change layout", command = change_layout)
        view_menu.add_separator

        #help menubar
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="FAQ", command = load_faq)
        help_menu.add_separator
        help_menu.add_command(label="Tutorial", command = load_tutorial)
        help_menu.add_separator
        #creating frames to organize the screen.
    
    def layout_frames(self, master, screen_width, screen_height):
        bottomFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)
        leftFrame = tk.Frame(master, bd = 5, relief = tk.RAISED ,bg =  background_color)
        rightFrame = tk.Frame(master, bd = 5, relief = tk.RAISED, bg = background_color)

        #putting the frames into a grid layout

        bottomFrame.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew")
        leftFrame.grid(row = 0, column = 0, sticky = "nsew")
        rightFrame.grid(row = 0, column = 1, sticky = "nsew")

        #setting up grid weights.

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=3)
        master.grid_columnconfigure(1, weight=4)

        #i think that here we can work on creating the funcitonality for each individual frame, ex: tuner, pitch history, information.

        #adding temporary label to the Pitch Detector Section
        tuner_header = tk.Label(rightFrame, text = "Pitch Detector", font=("Calibri", 20))
        tuner_header.config(bg = background_color, fg = "white")
        tuner_header.pack()

        myHistoryObject = session_history(bottomFrame, screen_width, screen_height)
        myDiagnosticObject = session_diagnostics(leftFrame)

        pitch = PitchDisplay(master, rightFrame)

        lib = load_library()
        handle = lib.create_stream(44100)
        audio = AudioThread(handle, lib)
        audio.start()
        master.after(10, pitch.update_data, handle, lib)
