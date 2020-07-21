import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.python_bridge.pitch_utilities import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def update_tuner_settings(self, cent_threshold, key_signature, oldSettingsView):
        self.mainWindow.threshold = cent_threshold
        self.mainWindow.pitch_display.set_threshold(cent_threshold)
        self.mainWindow.controller.session.data._threshold = cent_threshold

        self.mainWindow.controller.session.data.key_signature = key_signature

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
        v.set(mainWindow.controller.threshold)

        cent_scale = tk.Scale(middle_frame1, from_=1, to=25, orient=tk.HORIZONTAL, variable=v)
        cent_scale.config(bg=background_color, fg="white")
        cent_scale.pack()

        in_cents = tk.Label(middle_frame2, text="cents")
        in_cents.config(bg=background_color, fg="white")
        in_cents.pack()

        sig_label = tk.Label(bottom_frame, text="Key Signature")
        sig_label.config(bg=background_color, fg="white")
        sig_label.pack()


        self.major_key_names = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        self.major_accidentals = [Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.SHARP,
                                        Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]
        self.minor_key_names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
        self.minor_accidentals = [Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                        Accidental.SHARP, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]

        self.current_key_signature = mainWindow.controller.session.data.key_signature
        current = self.current_key_signature.name.split()
        if current[1] == "Minor":
            index = self.minor_key_names.index(current[0])
        else:
            index = self.major_key_names.index(current[0])
        self.root = tk.IntVar(value=index)
        self.ktype = tk.StringVar(value=current[1])
        self.radio_buttons = []

        # Grid of key signature buttons
        for i in range(0, 12):
            name = self.major_key_names[i]
            button = tk.Radiobutton(bottom_frame1, text=name, indicatoron=0, width=3, variable=self.root, value=i, command=self.selection_changed)
            button.grid(row=i//3 + 1, column=i%3)
            self.radio_buttons.append(button)

        major_button = tk.Radiobutton(bottom_frame2, text="Major", indicatoron=0, width=6, variable=self.ktype, value="Major", command=lambda: self.selection_changed(True))
        major_button.grid(row=1, column=0)
        minor_button = tk.Radiobutton(bottom_frame2, text="Minor", indicatoron=0, width=6, variable=self.ktype, value="Minor", command=lambda: self.selection_changed(True))
        minor_button.grid(row=2, column=0)

        done_button = ttk.Button(bottomest_frame, text="Apply", command=lambda: self.update_tuner_settings(cent_scale.get(), 
                                                                                                           self.current_key_signature,
                                                                                                           tuner_settings_window))

        done_button.pack()
        tuner_settings_window.lift(self.mainWindow.master)

    def selection_changed(self, redraw=False):
        if redraw:
            names = self.major_key_names
            if self.ktype.get() == "Minor":
                names = self.minor_key_names
            for i in range(0, 12):
                self.radio_buttons[i].config(text=names[i])

        index = self.root.get()
        keytype = KeySignatureType[self.ktype.get().upper()]
        if keytype == KeySignatureType.MINOR:
            accidental = self.minor_accidentals[index]
            name = self.minor_key_names[index]
        else:
            accidental = self.major_accidentals[index]
            name = self.major_key_names[index]
            
        self.current_key_signature = KeySignature(name, index, accidental, keytype)


