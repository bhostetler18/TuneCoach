import collections
from pitch_utilities import *


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
        return (100.0 * self._overall) / self._overall_count

    def get_recent_notes(self):
        return self._recent_notes

    def collect_data(self, hz):
        midi = hz_to_midi(hz)
        index = midi_to_pitch_class(midi)
        desired_hz = closest_in_tune_frequency(hz)
        cent = cents(desired_hz, hz)
        name = pitch_class_to_name(index, Accidental.SHARP)
        print(f"{name}: {round(hz, 2)} Hz ({round(cent)} cents)")

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
        avg_cents = self._cents / self._overall_count

        print("These are your accuracies for each pitch class:")
        for i in range(12):
            if self._pitch_count[i] == 0:
                print(self._notes[i], "was not played/sung in the session.")
            else:
                pitch_error = (100.0 * self._pitch_class[i]) / self._pitch_count[i]
                print("%s was in tune for %.4f %% of the time." % (self._notes[i], pitch_error))

        print("")
        if self._overall_count == 0:
            print("There was no audio input.")
        else:
            print("Overall:")
            print("You were in tune for %.4f %% of the time." % self.get_overall())
            print("You were off by an an average of %.4f cents." % avg_cents)
