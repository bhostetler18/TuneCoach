import math
from enum import Enum
from dataclasses import dataclass


class Accidental(Enum):
    FLAT = "b"
    SHARP = "#"
    NATURAL = "♮"


class KeySignatureType(Enum):
    MAJOR = "Major"
    MINOR = "Minor"


@dataclass
class KeySignature:
    root: str
    raw_value: int
    accidental: Accidental
    num_accidentals: int
    ktype: KeySignatureType
    
    # raw_value should be in [0,11]
    def get_display_for(self, raw_value):
        # TODO: don't create these on every function call
        flat_order = [11, 4, 9, 2, 7, 0, 5] # BEADGCF
        sharp_order = list(reversed(flat_order)) # FCGDAEB
        notes = { 0:"C", 2:"D", 4:"E", 5:"F", 7:"G", 9:"A", 11:"B"}
        flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        print(type(self.num_accidentals))
        relevant_accidentals = []
        if self.accidental == Accidental.SHARP:
            relevant_accidentals = sharp_order[:self.num_accidentals]
        elif self.accidental == Accidental.FLAT:
            relevant_accidentals = flat_order[:self.num_accidentals]

        if raw_value in relevant_accidentals:
            return notes[raw_value] + Accidental.NATURAL.value
        else:
            return pitch_class_to_name(raw_value, self.accidental)

    @property
    def name(self):
        root_str = self.get_display_for(self.raw_value)
        return f"{root_str} {self.ktype.value}"


def hz_to_midi(hz):
    return int(round(12.0 * math.log(hz/440.0, 2) + 69.0))


def midi_to_hz(midi):
    return 440.0 * 2.0**((midi - 69)/12.0)


def midi_to_pitch_class(midi):
    return int(midi % 12)


def get_octave(midi):
    return int(midi/12) - 1


def pitch_class_to_name(pitch, acc):
    flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    if acc == Accidental.FLAT:
        return flat[pitch]
    elif acc == Accidental.SHARP:
        return sharp[pitch]


def cents(target, actual):
    return 1200.0 * math.log(actual/target, 2)


def closest_in_tune_frequency(hz):
    return midi_to_hz(hz_to_midi(hz))


def note_to_midi(notes, note, octave):
    base = 12 + notes.index(note)
    adj = 12 * int(octave)
    return base + adj
