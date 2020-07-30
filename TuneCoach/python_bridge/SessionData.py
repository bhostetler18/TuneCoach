import collections
from TuneCoach.python_bridge.pitch_utilities import *
from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.Timer import *
import math
import datetime
import pickle
import os
from pathlib import Path
from collections import namedtuple

Note = collections.namedtuple('Note', 'hz cents pitch_class octave')

# DO WE STILL NEED THIS HERE? we can move it if you want?
# it doesn't matter but it fits here pretty logically
def save_to_file(session, path):
    with open(path, "wb") as file:
        pickle.dump(session, file)

def load_from_file(path):
    try:
        with open(path, "rb") as file:
            session = pickle.load(file)
            return session
    except Exception as e:
        # print(e)
        return None


class SessionData:
    def __init__(self, green_thresh, yellow_thresh):
        self._in_tune_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._pitch_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.note_history = []
        self._cents = 0.0
        self._overall = 0
        self._overall_count = 0
        self.green_thresh = green_thresh
        self.yellow_thresh = yellow_thresh
        self._timestamp = datetime.date.today()
        self.has_new_data = False

        self.key_signature = KeySignature("C", 0, Accidental.SHARP, 0, KeySignatureType.MAJOR)

        self.midi_range = (36, 107)

        self.timer = Timer()
        self.timer.start()
        self.timer.pause()

        self._score_history = []

    def get_overall(self):
        if self._overall_count == 0:
            return 0
        else:
            return (100.0 * self._overall) / self._overall_count

    @property
    def avg_cents(self):
        if self._overall_count == 0:
            return 0.0
        else:
            return self._cents / self._overall_count

    @property
    def score_history(self): return self._score_history

    @property
    def empty(self):
        return self._overall_count == 0

    @property
    def lowest_octave(self):
        return get_octave(self.midi_range[0])

    @property
    def highest_octave(self):
        return get_octave(self.midi_range[1])
    
    @property
    def lowest_note(self):
        return self.key_signature.get_display_for(self.midi_range[0] % 12)

    @property
    def highest_note(self):
        return self.key_signature.get_display_for(self.midi_range[1] % 12)
    
    def update_score_history(self):
        new_score = self.get_overall()
        self._score_history.append(new_score)
        if len(self._score_history) > 10:
                self._score_history.pop(0)

    def set_thresholds(self, green_thresh, yellow_thresh):
        self.green_thresh = green_thresh
        self.yellow_thresh = yellow_thresh

    # Takes in frequency and calculates and stores all data
    def collect_data(self, hz):
        midi = hz_to_midi(hz)
        if not (self.midi_range[0] <= midi <= self.midi_range[1]):
            return
        
        self.has_new_data = True
        index = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        octave = get_octave(midi)
        self.note_history.append(Note(hz=hz, cents=cent, pitch_class=index, octave=octave))

        # Gets counts of everything to calculate accuracy
        if abs(cent) <= self.green_thresh:
            self._in_tune_count[index] += 1
            self._overall += 1
        elif abs(cent) <= self.yellow_thresh:
            weight = 0.5 # TODO: scale by cent value?
            self._in_tune_count[index] += weight
            self._overall += weight

        self._pitch_count[index] += 1
        self._overall_count += 1
        self._cents += abs(cent)

