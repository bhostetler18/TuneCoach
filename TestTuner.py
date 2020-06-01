import struct
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import signal
import pyaudio

SAMPLE_RATE = 44100
FRAME_SIZE = 8192
NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def hz_to_midi_note(freq):
    return int(12 * math.log2(freq / 440) + 69)


def midi_note_to_pitch_class(midi):  # ignore octaves for now
    raw = midi % 12
    return NOTE_NAMES[raw]


def autocorrelation(buffer):
    max_lag = int(SAMPLE_RATE / 65.41)  # set lower bound for HZ here
    arr = [0] * max_lag
    for lag in range(0, max_lag):
        for offset in range(0, max_lag - lag):
            arr[lag] += buffer[offset] * buffer[offset + lag]
    max = arr[0]  # autocorrelation is maximum when signal compared to itself
    threshold = 0.4 * max  # arbitrary for now
    peaks, _ = signal.find_peaks(arr, height=threshold)  # this peak finding is likely the source of
    # some of the inaccuracy

    if len(peaks) > 0:
        # plottable = np.asarray(arr)
        # plt.plot(plottable)
        # plt.show()
        # print(peaks)
        return SAMPLE_RATE / peaks[0]
    return 0


def nsdf(buffer):
    max_lag = int(SAMPLE_RATE / 65.41)
    n = [0] * max_lag
    for lag in range(0, max_lag):
        ac = 0.0
        m = 0.0
        for offset in range(0, max_lag - lag):
            ac += buffer[offset] * buffer[offset + lag]
            m += buffer[offset] * buffer[offset] + buffer[offset + lag] * buffer[offset + lag]
        if m != 0:
            n[lag] = 2 * ac / m
    plottable = np.asarray(n)
    plt.plot(plottable)
    plt.show()


def callback(input_data, frame_count, time_info, flags):
    # raw = list(struct.unpack(f'{FRAME_SIZE}h', input_data))
    raw = [x / 32768 for x in list(struct.unpack(f'{FRAME_SIZE}h', input_data))]
    hz = autocorrelation(raw)
    if hz != 0:
        midi = hz_to_midi_note(hz)
        pitch = midi_note_to_pitch_class(midi)
        print(f"{round(hz, 2)} Hz, MIDI Note: {midi}, {pitch}")
    return input_data, pyaudio.paContinue


stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=SAMPLE_RATE,
                                input=True,
                                output=False,
                                stream_callback=callback,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

while stream.is_active():
    pass

