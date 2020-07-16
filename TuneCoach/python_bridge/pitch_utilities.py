import math
from enum import Enum


class Accidental(Enum):
    FLAT = "b"
    SHARP = "#"

class KeySignatureType(Enum):
    MAJOR = "Major"
    MINOR = "Minor"

class KeySignature:
    def __init__(self, root, raw_value, accidental, ktype):
        self.root = root
        self.raw_value = raw_value
        self.accidental = accidental
        self.ktype = ktype
    
    def get_display_for(self, raw_value):
        return pitch_class_to_name(raw_value, self.accidental)

    def get_name(self):
        root_str = self.get_display_for(self.raw_value)
        return f"{root_str} {self.ktype.value}"


def get_accidentals(key_sig):
    order_sharps = []


def hz_to_midi(hz):
    return int(round(12.0 * math.log(hz/440.0, 2) + 69.0))


def midi_to_hz(midi):
    return 440.0 * 2.0**((midi - 69)/12.0)


def midi_to_pitch_class(midi):
    return midi % 12


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