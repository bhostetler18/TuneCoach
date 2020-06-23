import math


def lag_to_hertz(lag, sample_rate):
    return sample_rate / lag


def hertz_to_lag(hertz, sample_rate):
    return int(sample_rate / hertz)


def hz_to_midi(hz):
    return 12.0 * math.log2(hz / 440.0) + 69.0


def midi_to_hz(midi):
    return 440.0 * pow(2.0, float(midi - 69) / 12.0)


def cents(target, actual):
    return 1200.0 * math.log2(actual / target)


def closest_in_tune_frequency(hz):
    closest_note = int(round(hz_to_midi(hz)))
    return midi_to_hz(closest_note)


def dbfs_from_rms(rms):
    return 20.0 * math.log10(rms) + 3.0103
