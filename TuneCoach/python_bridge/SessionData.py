import collections
from TuneCoach.python_bridge.pitch_utilities import *
from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.Timer import *
import math
import datetime
import pickle
import os
from pathlib import Path

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
    def __init__(self, cent_range):
        self._in_tune_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._pitch_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._freq_history = []
        self._cents = 0.0
        self._overall = 0
        self._overall_count = 0
        self.threshold = cent_range
        self._timestamp = datetime.date.today()
        self._recent_notes = collections.deque([])
        self.display_buffer = collections.deque([])
        self.has_new_data = False

        self.key_signature = KeySignature("C", 0, Accidental.SHARP, KeySignatureType.MAJOR)

        self.from_note = "C"
        self.from_octave = 2
        self.to_note = "B"
        self.to_octave = 7

        self.timer = Timer()
        self.timer.start()
        self.timer.pause()

        # Potential data storage
        self._note_history = []
        self._cent_history = []
        self._score_history = []


    @staticmethod
    def get_existing_sessions():
        session_list = []
        for file in os.listdir("./user_sessions"):
            session_list.append(file)
        return session_list

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
    def empty(self):
        return self._overall_count == 0
    
    def update_score_history(self):
        new_score = self.get_overall()
        self._score_history.append(new_score)
        if len(self._score_history) > 10:
                self._score_history.pop(0)

    # Takes in frequency and calculates and stores all data
    def collect_data(self, hz):
        self.has_new_data = True
        self._freq_history.append(hz)
        midi = hz_to_midi(hz)
        index = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        octave = 2 + math.floor(math.log2(desired_hz / 65.4))

        # Gets counts of everything to calculate accuracy
        if abs(cent) <= self.threshold:
            self._in_tune_count[index] += 1
            self._overall += 1
        self._pitch_count[index] += 1
        self._overall_count += 1
        self._cents += abs(cent)

        self.display_buffer.append((index, cent))
        if len(self.display_buffer) > 64:
            self.display_buffer.popleft()

        # Only inserts a note if it's different than the last
        if len(self._recent_notes) == 0 or index != self._recent_notes[-1]:
            self._recent_notes.append(index)

        # If deque is full, pop
        if len(self._recent_notes) > 8:
            self._recent_notes.popleft()

