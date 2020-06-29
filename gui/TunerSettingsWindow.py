import tkinter as tk
from gui.constants import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def update_pitch_settings(self, newPitch, newFilterLevel, oldSettingsView):
        #obj.update_threshold(newPitch)
        #TODO: need to update threshold with newPitch for current practice session
        self.currentSession.update_threshold(newPitch)
        noise_filter_level = newFilterLevel
        oldSettingsView.destroy()

    def __init__(self, mainWindow):
        self.currentSession = mainWindow.currentPracticeSession
        self.master = mainWindow.master
        tuner_settings_window = tk.Toplevel(self.master)
        tuner_settings_window.geometry("500x300")

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
        tuner_settings_window.grid_rowconfigure(2, weight=5)
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

        pitch_sensitivity_scale = tk.Scale(middle_frame1, from_=0, to_=50, orient=tk.HORIZONTAL)
        pitch_sensitivity_scale.config(bg=background_color, fg="white")
        pitch_sensitivity_scale.pack()

        in_cents = tk.Label(middle_frame2, text="cents")
        in_cents.config(bg=background_color, fg="white")
        in_cents.pack()

        outside_noise_filter_level = tk.Label(bottom_frame, text="Pitch Detection Threshold")
        outside_noise_filter_level.config(bg=background_color, fg="white")
        outside_noise_filter_level.pack()

        outside_noise_scale = tk.Scale(bottom_frame1, from_=0, to_=40, orient=tk.HORIZONTAL)
        outside_noise_scale.config(bg=background_color, fg="white")
        outside_noise_scale.pack()

        in_cents = tk.Label(bottom_frame2, text="decibals")
        in_cents.config(bg=background_color, fg="white")
        in_cents.pack()

        done_button = ttk.Button(bottomest_frame, text="Apply", command=lambda: self.update_pitch_settings(pitch_sensitivity_scale.get(), outside_noise_scale.get(), tuner_settings_window,))
        done_button.pack()
        tuner_settings_window.lift(self.master)
