import collections
from pitch_utilities import *
import math


class FeedbackSystem:
    def __init__(self, cent_range):
        self._notes = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
        self._pitch_class = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._pitch_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._cents = 0.0
        self._overall = 0
        self._overall_count = 0
        self._threshold = cent_range
        self._recent_notes = collections.deque([])

    def get_overall(self):
        if self._overall_count == 0:
            return 0
        else:
            return (100.0 * self._overall) / self._overall_count

    def get_recent_notes(self):
        return self._recent_notes

    def update_threshold(self, new_threshold):
        self._threshold = new_threshold

    # Takes in frequency and calculates and stores all data
    def collect_data(self, hz):
        midi = hz_to_midi(hz)
        index = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        name = pitch_class_to_name(index, Accidental.SHARP)
        octave = 2 + math.floor(math.log2(desired_hz / 65.4))

        print(f"{name}{octave}: {round(hz, 2)} Hz ({round(cent)} cents)")

        # Gets counts of everything to calculate accuracy
        if abs(cent) <= self._threshold:
            self._pitch_class[index] += 1
            self._overall += 1
        self._pitch_count[index] += 1
        self._overall_count += 1
        self._cents += abs(cent)

        # If deque is full, pop
        if len(self._recent_notes) >= 8:
            self._recent_notes.pop()

        # Only inserts a note if it's different than the last
        if len(self._recent_notes) != 0 and name != self._recent_notes[0]:
            self._recent_notes.append(self._notes[index])

    def display_all_data(self):
        print("These are your accuracies for each pitch class:")
        for i in range(12):
            if self._pitch_count[i] == 0:
                print(self._notes[i], "was not played/sung in the session.")
            else:
                pitch_error = (100.0 * self._pitch_class[i]) / self._pitch_count[i]
                print("%s was in tune for %.2f %% of the time." % (self._notes[i], pitch_error))

        print("")
        if self._overall_count == 0:
            print("There was no audio input.")
        else:
            print("Overall:")
            print("You were in tune for %.2f %% of the time." % self.get_overall())
            avg_cents = self._cents / self._overall_count
            print("You were off by an an average of %.2f cents." % avg_cents)
