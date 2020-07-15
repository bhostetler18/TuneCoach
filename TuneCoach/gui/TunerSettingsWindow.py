import tkinter as tk
from TuneCoach.gui.constants import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def update_pitch_settings(self, cent_threshold, oldSettingsView):
        self.mainWindow.threshold = cent_threshold
        self.mainWindow.pitch_display.set_threshold(cent_threshold)
        self.mainWindow.session.data._threshold = cent_threshold

        oldSettingsView.destroy()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        tuner_settings_window = tk.Toplevel(self.mainWindow.master)
        tuner_settings_window.geometry("500x300")

        tuner_settings_window.grid()

        top_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middle_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middle_frame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middle_frame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottom_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottom_frame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottom_frame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomest_frame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)

        # putting the frames into a grid layout
        top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        middle_frame.grid(row=1, column=0, columnspan=1, sticky="nsew")
        middle_frame1.grid(row=1, column=1, sticky="nsew")
        middle_frame2.grid(row=1, column=2, sticky="snew")
        bottom_frame.grid(row=2, column=0, sticky="nsew")
        bottom_frame1.grid(row=2, column=1, sticky="nsew")
        bottom_frame2.grid(row=2, column=2, sticky="nsew")
        bottomest_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # setting up grid weights.

        tuner_settings_window.grid_rowconfigure(0, weight=1)
        tuner_settings_window.grid_rowconfigure(1, weight=5)
        tuner_settings_window.grid_rowconfigure(1, weight=5)
        tuner_settings_window.grid_rowconfigure(3, weight=1)
        tuner_settings_window.grid_columnconfigure(0, weight=1)
        tuner_settings_window.grid_columnconfigure(1, weight=1)
        tuner_settings_window.grid_columnconfigure(2, weight=1)

        tuner_label = tk.Label(top_frame, text="Tuner Settings", font=("Calibri", 20))
        tuner_label.config(bg=background_color, fg="white")
        tuner_label.pack()

        centsitivity = tk.Label(middle_frame, text="Margin of Acceptable Pitch Error +- ")
        centsitivity.config(bg=background_color, fg="white")
        centsitivity.pack()

        v = tk.DoubleVar()
        v.set(mainWindow.threshold)

        cent_scale = tk.Scale(middle_frame1, from_=1, to=25, orient=tk.HORIZONTAL, variable=v)
        cent_scale.config(bg=background_color, fg="white")
        cent_scale.pack()

        in_cents = tk.Label(middle_frame2, text="cents")
        in_cents.config(bg=background_color, fg="white")
        in_cents.pack()

        sig_label = tk.Label(bottom_frame, text="Key Signature")
        sig_label.config(bg=background_color, fg="white")
        sig_label.pack()


        c_button = tk.Button(bottom_frame1, text="C", height=1, width=1)
        c_button.grid(row=1, column=0)
        db_button = tk.Button(bottom_frame1, text="Db", height=1, width=1)
        db_button.grid(row=1, column=1)
        d_button = tk.Button(bottom_frame1, text="D", height=1, width=1)
        d_button.grid(row=1, column=2)

        eb_button = tk.Button(bottom_frame1, text="Eb", height=1, width=1)
        eb_button.grid(row=2, column=0)
        e_button = tk.Button(bottom_frame1, text="E", height=1, width=1)
        e_button.grid(row=2, column=1)
        f_button = tk.Button(bottom_frame1, text="F", height=1, width=1)
        f_button.grid(row=2, column=2)

        fs_button = tk.Button(bottom_frame1, text="F#", height=1, width=1)
        fs_button.grid(row=3, column=0)
        g_button = tk.Button(bottom_frame1, text="G", height=1, width=1)
        g_button.grid(row=3, column=1)
        ab_button = tk.Button(bottom_frame1, text="Ab", height=1, width=1)
        ab_button.grid(row=3, column=2)

        a_button = tk.Button(bottom_frame1, text="A", height=1, width=1)
        a_button.grid(row=4, column=0)
        bb_button = tk.Button(bottom_frame1, text="Bb", height=1, width=1)
        bb_button.grid(row=4, column=1)
        b_button = tk.Button(bottom_frame1, text="B", height=1, width=1)
        b_button.grid(row=4, column=2)

        major_button = ttk.Button(bottom_frame2, text="Major")
        major_button.grid(row=1, column=0)
        minor_button = ttk.Button(bottom_frame2, text="Minor")
        minor_button.grid(row=2, column=0)

        done_button = ttk.Button(bottomest_frame, text="Apply",
                                command=lambda: self.update_pitch_settings(cent_scale.get(), tuner_settings_window))

        done_button.pack()
        tuner_settings_window.lift(self.mainWindow.master)
