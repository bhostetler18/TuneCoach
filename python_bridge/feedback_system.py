from queue import Queue
from processing_utilities import *
import math


class feedback_system:
    def __init__(self, cent_range):
        self._notes = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
        self._pitch_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._pitch_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._cents = 0.0
        self._overall = 0
        self._overallCount = 0
        self._threshold = cent_range
        self._recent_notes = Queue(maxsize=8)

    def get_overall(self):
        return (100.0 * self._overall) / self._overall

    def get_recent_notes(self):
        return self._recent_notes

    def collect_data(self, hz):
        midi = hz_to_midi(hz)
        index = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        name = pitch_class_to_name(pitch_class, Accidental.SHARP)
        print(f"{name}: {round(hz, 2)} Hz ({round(cent)} cents)")

        if abs(cent) <= self._threshold:
            self._pitch_class[index] += 1
            self._overall += 1
        self._pitch_count[index] += 1
        self._overallCount += 1
        self._cents += abs(cent)

        # If queue is full, pop
        if self._recent_notes.full():
            self._recent_notes.get()

        # Only inserts a note if it's different than the last
        d = self._recent_notes.queue
        if name != d[0]:
            self._recent_notes.put(self._notes[index])

    def display_all_data(self):
        avg_cents = self._cents / self._overallCount

        print("These are your accuracies for each pitch class:")
        for i in range(12):
            pitch_error = (100.0 * self._pitch_class[i]) / self._pitch_count[i]
            if math.isnan(pitch_error):
                print(self._notes[i], "was not played/sung in the session.")
            else:
                print("%s was in tune for %.4f %% of the time." % (self._notes[i], pitch_error))

        print("")
        if math.isnan(self.get_overall()):
            print("There was no audio input.")
        else:
            print("Overall:")
            print("You were in tune for %.4f %% of the time." % self.get_overall())
            print("You were off by an an average of %.4f cents." % avg_cents)
