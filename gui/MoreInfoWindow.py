from constants import *
import tkinter as tk


class MoreInfoWindow(tk.Toplevel):
    def refresh(self, window, master, obj):
        window.destroy()
        MoreInfoWindow(master, obj)

    def __init__(self, master, obj):
        self.master = master
        my_window = tk.Toplevel(master)
        final_string = ""
        if obj._practice_session is None:
            final_string += "\n No Input Yet"
        elif obj._practice_session._total_count > 0:
            avg_cents= obj._practice_session._cents / obj._practice_session._total_count
            for i in range(12):
                if obj._practice_session._pitch_count[i] == 0:
                    final_string += ("\n" + obj._notes[i] + " was not played/sung in the session.")
                else:
                    pitch_error = (100.0*obj._practice_session._pitch_class[i]) / obj._practice_session._pitch_count[i]
                    final_string += ("\n%s was in tune for %.2f %% of the time." % (obj._notes[i], pitch_error))
            final_string += "\n"
            final_string += "\nOverall"
            final_string += "\nYou were in tune for %.2f %% of the time." % obj.get_overall()
            final_string += "\nYou were off by an average of %.2f cents." % avg_cents
        else:
            final_string += "\nno input yet"
        my_label = tk.Label(my_window, text=final_string, bg=background_color, fg="white")
        my_label.pack()
        exit_button = tk.Button(my_window, text="Exit", command=lambda: my_window.destroy())
        exit_button.pack()
        refresh_button = tk.Button(my_window, text="Refresh", command=lambda: self.refresh(my_window, master, obj))
        refresh_button.pack()
        my_window.lift(master)
