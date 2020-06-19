#include "processing_utilities.h"

//NOTE: many of the more useful templated functions are only present in processing_utilities.h

double lag_to_hertz(double lag, double sample_rate)
{
    return sample_rate/lag;
}

int hertz_to_lag(double hertz, double sample_rate)
{
    return (int)(sample_rate/hertz);
}

double hz_to_midi(double hz)
{
    return (12.0 * log2(hz / 440.0) + 69.0);
}

double midi_to_hz(int midi)
{
    return 440.0 * pow(2.0, (double)(midi - 69)/12.0);
}

double cents(double target, double actual)
{
    return 1200.0 * log2(actual/target);
}

double closest_in_tune_frequency(double hz)
{
    int closest_note = (int)round(hz_to_midi(hz));
    return midi_to_hz(closest_note);
}