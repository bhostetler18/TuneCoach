import tkinter as tk
from TuneCoach.gui.constants import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def update_tuner_settings(self, cent_threshold, key, signature, oldSettingsView):
        self.mainWindow.threshold = cent_threshold
        self.mainWindow.pitch_display.set_threshold(cent_threshold)
        self.mainWindow.controller.session.data._threshold = cent_threshold

        self.mainWindow.controller.session.data.set_key(key)
        self.mainWindow.controller.session.data.set_signature(signature)

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
        
        # Default key signatures
        key = tk.StringVar(None, "C")
        sig = tk.StringVar(None, "Major")

        # Grid of key signature buttons
        c_button = tk.Radiobutton(bottom_frame1, text="C", indicatoron=0, width=3, variable=key, value="C")
        c_button.grid(row=1, column=0)
        db_button = tk.Radiobutton(bottom_frame1, text="Db", indicatoron=0, width=3, variable=key, value="Db")
        db_button.grid(row=1, column=1)
        d_button = tk.Radiobutton(bottom_frame1, text="D", indicatoron=0, width=3, variable=key, value="D")
        d_button.grid(row=1, column=2)
        eb_button = tk.Radiobutton(bottom_frame1, text="Eb", indicatoron=0, width=3, variable=key, value="Eb")
        eb_button.grid(row=2, column=0)
        e_button = tk.Radiobutton(bottom_frame1, text="E", indicatoron=0, width=3, variable=key, value="E")
        e_button.grid(row=2, column=1)
        f_button = tk.Radiobutton(bottom_frame1, text="F", indicatoron=0, width=3, variable=key, value="F")
        f_button.grid(row=2, column=2)
        fs_button = tk.Radiobutton(bottom_frame1, text="F#", indicatoron=0, width=3, variable=key, value="F#")
        fs_button.grid(row=3, column=0)
        g_button = tk.Radiobutton(bottom_frame1, text="G", indicatoron=0, width=3, variable=key, value="G")
        g_button.grid(row=3, column=1)
        ab_button = tk.Radiobutton(bottom_frame1, text="Ab", indicatoron=0, width=3, variable=key, value="Ab")
        ab_button.grid(row=3, column=2)
        a_button = tk.Radiobutton(bottom_frame1, text="A", indicatoron=0, width=3, variable=key, value="A")
        a_button.grid(row=4, column=0)
        bb_button = tk.Radiobutton(bottom_frame1, text="Bb", indicatoron=0, width=3, variable=key, value="Bb")
        bb_button.grid(row=4, column=1)
        b_button = tk.Radiobutton(bottom_frame1, text="B", indicatoron=0, width=3, variable=key, value="B")
        b_button.grid(row=4, column=2)
        major_button = tk.Radiobutton(bottom_frame2, text="Major", indicatoron=0, width=6, variable=sig, value="Major")
        major_button.grid(row=1, column=0)
        minor_button = tk.Radiobutton(bottom_frame2, text="Minor", indicatoron=0, width=7, variable=sig, value="Minor")
        minor_button.grid(row=2, column=0)

        done_button = ttk.Button(bottomest_frame, text="Apply", command=lambda: self.update_tuner_settings(cent_scale.get(), key.get(), sig.get(), tuner_settings_window))

        done_button.pack()
        tuner_settings_window.lift(self.mainWindow.master)
