from TuneCoach.gui.constants import *
import tkinter as tk


class MoreInfoWindow:
    @staticmethod
    def refresh(window, mainWindow):
        window.destroy()
        MoreInfoWindow(mainWindow)

    def __init__(self, mainWindow):
        my_window = tk.Toplevel(mainWindow.master)
        currentSession = mainWindow.session
        data = currentSession.data

        topFrame = tk.Frame(my_window, bg=background_color)
        middleFrame = tk.Frame(my_window, bg=background_color)
        bottomFrame = tk.Frame(my_window, bg=background_color)

        topFrame.grid(row=0, sticky="nsew")
        middleFrame.grid(row=1, sticky="nsew")
        bottomFrame.grid(row=2, sticky="nsew")

        final_string = ""
        title_string = ""
        if currentSession is None:
            title_string += "No Session Currently Active"
        else:
            title_string += currentSession.name + " Information:"
            if data._overall_count > 0:
                avg_cents = data._cents / data._overall_count
                for i in range(12):
                    if data._pitch_count[i] == 0:
                        final_string += (data._notes[i] + " was not played/sung in the session.\n")
                    else:
                        pitch_error = (100.0 * data._in_tune_count[i]) / data._pitch_count[i]
                        final_string += ("%s was in tune for %.2f %% of the time.\n" % (
                        data._notes[i], pitch_error))
                final_string += "\nOverall"
                final_string += "\nYou were in tune for %.2f %% of the time." % data.get_overall()
                final_string += "\nYou were off by an average of %.2f cents." % avg_cents
            else:
                final_string += "no input yet"

        titleLabel = tk.Label(topFrame, text=title_string, bg=background_color, fg="white")
        titleLabel.pack()
        my_label = tk.Label(middleFrame, text=final_string, bg="#B0AFAF", fg="black", bd=5, relief=tk.RIDGE)
        my_label.pack()
        exit_button = tk.Button(bottomFrame, text="Exit", command=lambda: my_window.destroy())
        exit_button.pack(side=tk.LEFT, padx=5, pady=5)
        refresh_button = tk.Button(bottomFrame, text="Refresh", command=lambda: self.refresh(my_window, mainWindow))
        refresh_button.pack(side=tk.RIGHT, padx=5, pady=5)
        my_window.lift(mainWindow.master)
