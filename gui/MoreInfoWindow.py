from constants import *
import tkinter as tk


class MoreInfoWindow:
    def refresh(self, window, mainWindow):
        window.destroy()
        MoreInfoWindow(mainWindow)

    def __init__(self, mainWindow):
        my_window = tk.Toplevel(mainWindow)
        currentSession = mainWindow.currentPracticeSession

        print(currentSession._name, '**************************', currentSession._overall_count)

        final_string = ""
        # if currentSession._practice_session is None:
        if currentSession is None:
            final_string += "\n No Input Yet"
        # elif currentSession._practice_session._total_count > 0:
        elif currentSession._overall_count > 0:
            avg_cents= currentSession._cents / currentSession._overall_count
            for i in range(12):
                if currentSession._pitch_count[i] == 0:
                    final_string += ("\n" + currentSession._notes[i] + " was not played/sung in the session.")
                else:
                    pitch_error = (100.0*currentSession._in_tune_count[i]) / currentSession._pitch_count[i]
                    final_string += ("\n%s was in tune for %.2f %% of the time." % (currentSession._notes[i], pitch_error))
            final_string += "\n"
            final_string += "\nOverall"
            final_string += "\nYou were in tune for %.2f %% of the time." % currentSession.get_overall()
            final_string += "\nYou were off by an average of %.2f cents." % avg_cents
        else:
            final_string += "\nno input yet"
        my_label = tk.Label(my_window, text=final_string, bg=background_color, fg="white")
        my_label.pack()
        exit_button = tk.Button(my_window, text="Exit", command=lambda: my_window.destroy())
        exit_button.pack()
        refresh_button = tk.Button(my_window, text="Refresh", command=lambda: self.refresh(my_window, mainWindow))
        refresh_button.pack()
        my_window.lift(mainWindow)
