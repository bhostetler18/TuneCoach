import tkinter as tk
from constants import *
import tkinter.ttk as ttk
# tuner settings window
class TunerSettingsWindow(tk.Toplevel):
    def update_pitch_settings(self, newPitch, newFilterLevel, oldSettingsView, obj):
        obj.update_threshold(newPitch)
        noise_filter_level = newFilterLevel
        oldSettingsView.destroy()

    def __init__(self, master, obj):
        self.master = master
        tuner_settings_window = tk.Toplevel(master)
        tuner_settings_window.geometry("500x300")

        topFrame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middleFrame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middleFrame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        middleFrame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomFrame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomFrame1 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomFrame2 = tk.Frame(tuner_settings_window, bd=5, bg=background_color)
        bottomestFrame = tk.Frame(tuner_settings_window, bd=5, bg=background_color)

        # putting the frames into a grid layout

        topFrame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        middleFrame.grid(row=1, column=0, columnspan=1, sticky="nsew")
        middleFrame1.grid(row=1, column=1, sticky="nsew")
        middleFrame2.grid(row=1, column=2, sticky="snew")
        bottomFrame.grid(row=2, column=0, sticky="nsew")
        bottomFrame1.grid(row=2, column=1, sticky="nsew")
        bottomFrame2.grid(row=2, column=2, sticky="nsew")
        bottomestFrame.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # setting up grid weights.

        tuner_settings_window.grid_rowconfigure(0, weight=1)
        tuner_settings_window.grid_rowconfigure(1, weight=5)
        tuner_settings_window.grid_rowconfigure(2, weight=5)
        tuner_settings_window.grid_rowconfigure(3, weight=1)
        tuner_settings_window.grid_columnconfigure(0, weight=1)
        tuner_settings_window.grid_columnconfigure(1, weight=1)
        tuner_settings_window.grid_columnconfigure(2, weight=1)

        tuner_label = tk.Label(topFrame, text="Tuner Settings", font=("Calibri", 20))
        tuner_label.config(bg=background_color, fg="white")
        tuner_label.pack()

        centsitivity = tk.Label(middleFrame, text="Margin of Acceptable Pitch Error +- ")
        centsitivity.config(bg=background_color, fg="white")
        centsitivity.pack()

        pitch_sensitivity_scale = tk.Scale(middleFrame1, from_=0, to_=50, orient=tk.HORIZONTAL)
        pitch_sensitivity_scale.config(bg=background_color, fg="white")
        pitch_sensitivity_scale.pack()

        inCents = tk.Label(middleFrame2, text="cents")
        inCents.config(bg=background_color, fg="white")
        inCents.pack()

        outside_noise_filter_level = tk.Label(bottomFrame, text="Pitch Detection Threshold")
        outside_noise_filter_level.config(bg=background_color, fg="white")
        outside_noise_filter_level.pack()

        outside_noise_scale = tk.Scale(bottomFrame1, from_=0, to_=40, orient=tk.HORIZONTAL)
        outside_noise_scale.config(bg=background_color, fg="white")
        outside_noise_scale.pack()

        inCents = tk.Label(bottomFrame2, text="decibals")
        inCents.config(bg=background_color, fg="white")
        inCents.pack()

        doneButton = ttk.Button(bottomestFrame, text="Apply",
                                command=lambda: self.update_pitch_settings(pitch_sensitivity_scale.get(),
                                                                      outside_noise_scale.get(), tuner_settings_window,
                                                                      obj))
        doneButton.pack()

        tuner_settings_window.lift(master)
