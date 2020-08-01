import tkinter as tk
from TuneCoach.gui.constants import *
from TuneCoach.python_bridge.pitch_utilities import *
import tkinter.ttk as ttk


# Tuner settings window
class TunerSettingsWindow:
    def input_check(self, new_cents, f_note, f_oct, t_note, t_oct, window):
        keytype = KeySignatureType[self.ktype.get().upper()]
        low = string_to_pitch_class(f_note)
        high = string_to_pitch_class(t_note)
        from_midi = pitch_with_octave(low, int(f_oct))
        to_midi = pitch_with_octave(high, int(t_oct))

        if from_midi >= to_midi: 
            self.range_label.pack_forget()
            style = ttk.Style()
            style.configure("Red.TLabel", foreground="red")
            self.range_label = ttk.Label(self.range_frame1, text="Note Range:")
            self.range_label.configure(style="Red.TLabel")
            self.range_label.pack(expand=False, side=tk.LEFT, padx=15)

        else:
            self.update_tuner_settings(new_cents, self.current_key_signature, from_midi, to_midi, window)

    def update_tuner_settings(self, cent_threshold, key_signature, from_midi, to_midi, oldSettingsView):
        self.mainWindow.controller.update_tuner_settings(cent_threshold, key_signature, from_midi, to_midi)
        oldSettingsView.destroy()

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        data = mainWindow.controller.session.data
        tuner_settings_window = tk.Toplevel(self.mainWindow.master)
        tuner_settings_window.title("Tuner Settings")
        tuner_settings_window.geometry("400x300")
        tuner_settings_window.minsize(width = 400, height = 300)
        tuner_settings_window.maxsize(width  = 400, height = 300)

        cent_frame = ttk.Frame(tuner_settings_window)
        key_sig_frame = ttk.Frame(tuner_settings_window)
        radio_button_frame = ttk.Frame(tuner_settings_window)
        key_type_frame = ttk.Frame(tuner_settings_window)
        self.range_frame1 = ttk.Frame(tuner_settings_window)
        range_frame2 = ttk.Frame(tuner_settings_window)
        done_frame = ttk.Frame(tuner_settings_window)

        # putting the frames into a grid layout
        cent_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        key_sig_frame.grid(row=1, column=0, sticky="nsew")
        radio_button_frame.grid(row=1, column=1, sticky="nsew")
        key_type_frame.grid(row=1, column=2, sticky="nsew")
        self.range_frame1.grid(row=2, column=0, sticky="nsew")
        range_frame2.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.invalid = False
        done_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # setting up grid weights.
        tuner_settings_window.grid_rowconfigure(0, weight=1)
        tuner_settings_window.grid_rowconfigure(1, weight=1)
        tuner_settings_window.grid_rowconfigure(2, weight=1)
        tuner_settings_window.grid_columnconfigure(0, weight=1, uniform='c')
        tuner_settings_window.grid_columnconfigure(1, weight=1, uniform='c')
        tuner_settings_window.grid_columnconfigure(2, weight=1, uniform='c')

        centsitivity = ttk.Label(cent_frame, text="Acceptable Error (cents):")
        centsitivity.pack(anchor=tk.CENTER, pady=15)

        v = tk.DoubleVar()
        v.set(data.green_thresh)
        cent_scale = tk.Scale(cent_frame, from_=1, to=25, orient=tk.HORIZONTAL, variable=v)
        cent_scale.config(bg="#F4F4F4", fg="black")
        cent_scale.pack(anchor=tk.CENTER)

        sig_label = ttk.Label(key_sig_frame, text="Key Signature:")
        sig_label.pack(expand=False, side=tk.LEFT, padx=15)

        self.range_label = ttk.Label(self.range_frame1, text="Note Range:")
        self.range_label.pack(expand=False, side=tk.LEFT, padx=15)

        # TODO: extract into keysignature and allow for better initialization, create circle-of-fifths-based data structure
        self.major_key_names = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
        self.major_accidentals = [Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.SHARP,
                                        Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]
        self.major_numbers = [0, 5, 2, 3, 4, 1, 6, 1, 4, 3, 2, 5] # number of sharps/flats in each key
        self.minor_key_names = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
        self.minor_accidentals = [Accidental.FLAT, Accidental.SHARP, Accidental.FLAT, Accidental.FLAT,
                                    Accidental.SHARP, Accidental.FLAT, Accidental.SHARP, Accidental.FLAT,
                                        Accidental.SHARP, Accidental.SHARP, Accidental.FLAT, Accidental.SHARP]
        self.minor_numbers = [3, 4, 1, 6, 1, 4, 3, 2, 5, 0, 5, 2]

        self.current_key_signature = data.key_signature
        current_type = data.key_signature.ktype
        self.root = tk.IntVar(value=self.current_key_signature.raw_value)
        self.ktype = tk.StringVar(value=current_type.value)
        self.radio_buttons = []

        # Grid of key signature buttons
        for i in range(0, 12):
            name = ""
            if current_type == KeySignatureType.MINOR:
                name = self.minor_key_names[i]
            else:
                name = self.major_key_names[i]
            button = tk.Radiobutton(radio_button_frame, text=name, indicatoron=0, variable=self.root, value=i, command=self.selection_changed)
            button.grid(row=i//4, column=i%4, sticky='news')
            self.radio_buttons.append(button)

        radio_button_frame.grid_rowconfigure(0, weight=1, uniform="row")
        radio_button_frame.grid_rowconfigure(1, weight=1, uniform="row")
        radio_button_frame.grid_rowconfigure(2, weight=1, uniform="row")
        radio_button_frame.grid_columnconfigure(0, weight=1, uniform="col")
        radio_button_frame.grid_columnconfigure(1, weight=1, uniform="col")
        radio_button_frame.grid_columnconfigure(2, weight=1, uniform="col")
        radio_button_frame.grid_columnconfigure(3, weight=1, uniform="col")

        major_button = tk.Radiobutton(key_type_frame, text="Major", indicatoron=0, width=6, variable=self.ktype, value="Major", command=self.selection_changed)
        major_button.pack(expand=True, side=tk.TOP)
        minor_button = tk.Radiobutton(key_type_frame, text="Minor", indicatoron=0, width=6, variable=self.ktype, value="Minor", command=self.selection_changed)
        minor_button.pack(expand=True, side=tk.BOTTOM)


        # MIDI RANGE SELECTION
        self.from_note = tk.StringVar()
        from_octave = tk.IntVar()
        self.to_note = tk.StringVar()
        to_octave = tk.IntVar()

        self.from_note_menu = ttk.OptionMenu(range_frame2, self.from_note, self.major_key_names[0], *self.major_key_names)
        self.from_note_menu.config(width=2)
        self.from_note_menu.pack(side=tk.LEFT)
        from_octave_menu = ttk.OptionMenu(range_frame2, from_octave, 2, 2, 3, 4, 5, 6, 7)
        from_octave_menu.pack(side=tk.LEFT)

        to_text = ttk.Label(range_frame2, text="to", width=4)
        to_text.configure(anchor="center")
        to_text.pack(side=tk.LEFT)

        self.to_note_menu = ttk.OptionMenu(range_frame2, self.to_note, *self.major_key_names)
        self.to_note_menu.config(width=2)
        self.to_note_menu.pack(side=tk.LEFT)
        to_octave_menu = ttk.OptionMenu(range_frame2, to_octave, 2, 2, 3, 4, 5, 6, 7)
        to_octave_menu.pack(side=tk.LEFT)

        self.from_note.set(data.lowest_note)
        self.to_note.set(data.highest_note)
        from_octave.set(data.lowest_octave)
        to_octave.set(data.highest_octave)

        self.refresh_om()

        done_button = ttk.Button(done_frame, text="Apply", command=lambda: self.input_check(cent_scale.get(), self.from_note.get(), from_octave.get(), self.to_note.get(), to_octave.get(), tuner_settings_window))
        done_button.pack()
        tuner_settings_window.lift(self.mainWindow.master)

    def selection_changed(self, redraw=True):
        index = self.root.get()
        keytype = KeySignatureType[self.ktype.get().upper()]
        num_accidentals = 0
        if keytype == KeySignatureType.MINOR:
            accidental = self.minor_accidentals[index]
            name = self.minor_key_names[index]
            num_accidentals = self.minor_numbers[index]
        else:
            accidental = self.major_accidentals[index]
            name = self.major_key_names[index]
            num_accidentals = self.major_numbers[index]
            
        self.current_key_signature = KeySignature(name, index, accidental, num_accidentals, keytype)

        if redraw:
            self.refresh_om()
            if self.ktype.get() == "Minor":
                names = self.minor_key_names
            else:
                names = self.major_key_names
            for i in range(0, 12):
                self.radio_buttons[i].config(text=names[i])

    def refresh_om(self):
        low = string_to_pitch_class(self.from_note.get())
        high = string_to_pitch_class(self.to_note.get())

        self.from_note_menu['menu'].delete(0, 'end')
        self.to_note_menu['menu'].delete(0, 'end')

        notes = [self.current_key_signature.get_display_for(n) for n in range(0,12)]
        start = self.current_key_signature.raw_value
        notes = notes[start:] + notes[:start] # rotate so current root is first

        for note in notes:
            self.from_note_menu['menu'].add_command(label=note, command=tk._setit(self.from_note, note))
            self.to_note_menu['menu'].add_command(label=note, command=tk._setit(self.to_note, note))

        self.from_note.set(self.current_key_signature.get_display_for(low))
        self.to_note.set(self.current_key_signature.get_display_for(high))

