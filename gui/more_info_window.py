from constants import *
import tkinter as tk

class more_info_window(tk.Toplevel):
    def refresh(self, window, master, obj):
        window.destroy()
        more_info_window(master, obj)
    def __init__(self, master, obj):
        self.master = master
        myWindow = tk.Toplevel(master)
        finalString = ""
        if obj._practice_session is None:
            finalString += "\n No Input Yet"
        elif obj._practice_session._total_count > 0:
            avg_cents= obj._practice_session._cents / obj._practice_session._total_count
            for i in range(12):
                if obj._practice_session._pitch_count[i] == 0:
                    finalString += ("\n" + obj._notes[i] + " was not played/sung in the session.")
                else:
                    pitch_error = (100.0*obj._practice_session._pitch_class[i]) / obj._practice_session._pitch_count[i]
                    finalString += ("\n%s was in tune for %.2f %% of the time." % (obj._notes[i], pitch_error))
            finalString += "\n"
            finalString += "\nOverall"
            finalString += "\nYou were in tune for %.2f %% of the time." % obj.get_overall()
            finalString += "\nYou were off by an average of %.2f cents." % avg_cents
        else:
            finalString += "\nno input yet"
        myLabel = tk.Label(myWindow, text = finalString, bg = background_color, fg = "white")
        myLabel.pack()
        exitButton = tk.Button(myWindow, text = "Exit", command = lambda : myWindow.destroy())
        exitButton.pack()
        refreshButton = tk.Button(myWindow, text = "Refresh", command = lambda : self.refresh(myWindow, master, obj))
        refreshButton.pack()
        myWindow.lift(master)
