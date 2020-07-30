import math
from enum import Enum
from dataclasses import dataclass


class Accidental(Enum):
    FLAT = "♭"
    SHARP = "♯"
    NATURAL = "♮"


class KeySignatureType(Enum):
    MAJOR = "Major"
    MINOR = "Minor"

class Notes:
    FLAT_NOTES = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
    SHARP_NOTES = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
    NOTE_DICT = {
        "C": 0,
        "C♯": 1,
        "D♭": 1,
        "D": 2,
        "D♯": 2, 
        "E♭": 3, 
        "E": 4, 
        "F": 5,
        "F♯": 6, 
        "G♭": 6, 
        "G": 7,
        "G♯": 8, 
        "A♭": 8, 
        "A": 9, 
        "A♯": 10,
        "B♭": 10,
        "B": 11
    }

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

def pitch_with_octave(pitch_class, octave):
    return 12 * (octave + 1) + pitch_class

def pitch_class_to_name(pitch, acc):
    if acc == Accidental.FLAT:
        return Notes.FLAT_NOTES[pitch]
    elif acc == Accidental.SHARP:
        return Notes.SHARP_NOTES[pitch]

def cents(target, actual):
    return 1200.0 * math.log(actual/target, 2)


def closest_in_tune_frequency(hz):
    return midi_to_hz(hz_to_midi(hz))


def string_to_pitch_class(string):
    return Notes.NOTE_DICT.get(string, 0) #TODO: more robust error handling
