#pragma once
#include <cstring>
#include <cmath>
#include <iostream>

//Some functions are templated in case we ever want to change away from floating point audio samples


/* Calculates the normalized square difference function for a time lag in [lag_start, lag_stop).
 * For example, output[52] will contain the NSDF with tau of 52 once this is run.
 * Ensure 'output' has allocated space for (lag_stop - lag_start) values.
 * 'buffer' of size 'length' should contain the audio samples
 * The optimized version always runs with lag_start = 0
 * See https://www.researchgate.net/publication/230554927_A_smarter_way_to_find_pitch
 */
template <typename T>
void normalized_square_difference(T* buffer, int length, int lag_start, int lag_stop, T* output);
template <typename T>
void normalized_square_difference_optimized(T* buffer, int length, int lag_stop, T* output);

/* Populates 'peaks' with the sample location [0, length) of local maxima in arr (if any).
 * Pass in the length of 'arr' with 'length'. Only the highest local maximum between zero crossings
 * is kept. Zeroes indicate a lack of a maximum.
 *
 * To avoid memory allocation issues, 'peaks' must be a
 * pre-allocated array of fixed length psize. 64 seems to be more than enough as most of the
 * detected maxima are just overtones and will be discarded later.
 * */
template <typename T>
void find_peaks(T* arr, int length, int* peaks, int psize);


/* Given 'nsdf' values and 'peaks' array containing a maximum of 'psize' peak locations, this
 * will choose a the best time lag and return the corresponding detected frequency.
 * 'threshold' should be in [0, 1]. 0.9 seems to work well.
 * Returns 0 if no candidate pitch is detected.
 */
template<typename T>
double choose_fundamental(T* nsdf, int* peaks, int psize, double sample_rate, double threshold);


/* Returns the adjusted location of a peak (at sample location 'peak') detected within 'arr'. Since
 * the peak location is quantized to an integer, it probably isn't the true location. This function returns
 * 'peak' plus or minus an offset in [-0.5, 0.5].
 * This actually has a large impact on the accuracy of detected pitches.
 * See https://ccrma.stanford.edu/~jos/sasp/Quadratic_Peak_Interpolation.html
 */
template <typename T>
double parabolic_interpolation(T* arr, int peak);


// Converts a sample number/lag amount to the pitch in Hz it represents.
double lag_to_hertz(double lag, double sample_rate);

// Converts a frequency to the time lag needed to detect it
int hertz_to_lag(double hertz, double sample_rate);

// Converts a frequency to the corresponding MIDI note designation (unrounded).
double hz_to_midi(double hz);


// Converts a MIDI note # to the corresponding frequency
double midi_to_hz(int midi);


/* Returns the difference in cents between the 'target' frequency and 'actual' (Hz).
 * Positive indicates sharp, negative flat.
 */
double cents(double target, double actual);

// Returns the closest (equal tempered) in-tune frequency to 'hz'
double closest_in_tune_frequency(double hz);

template <typename T>
//TODO: this can definitely be optimized, even without the FFT trick
void normalized_square_difference(T* buffer, int length, int lag_start, int lag_stop, T* output) {
    std::memset(output, 0.0, (lag_stop - lag_start) * sizeof(output[0]));
    for (int lag = lag_start; lag < lag_stop; ++lag)
    {
        T ac = 0;
        T m = 0;
        for (int offset = 0; offset < length - lag; ++offset)
        {
            ac += buffer[offset] * buffer[offset + lag];
            m += buffer[offset] * buffer[offset] + buffer[offset + lag] * buffer[offset + lag];
        }
        T n = 2 * ac / m;
        if (std::isnan(n)) output[lag] = 0;
        else output[lag] = n;
    }
}

template <typename T>
void normalized_square_difference_optimized(T* buffer, int length, int lag_stop, T* output) {
    std::memset(output, 0.0, lag_stop * sizeof(output[0]));
    T ac = 0;
    T m1 = 0;
    T m2 = 0;
    T n = 0;
    int offset;
    int lag;
    //Initial population with tau/lag = 0
    for (offset = 0; offset < length; ++offset)
    {
        ac += buffer[offset] * buffer[offset];
    }
    m1 = ac;
    m2 = ac;
    output[0] = 1;

    for (lag = 1; lag < lag_stop; ++lag)
    {
        ac = 0;
        for (offset = 0; offset < length - lag; ++offset)
        {
            ac += buffer[offset] * buffer[offset + lag];
        }
        m1 -= buffer[length - lag] * buffer[length - lag];
        m2 -= buffer[lag - 1] * buffer[lag - 1];
        n = 2 * ac / (m1 + m2);
        if (std::isnan(n)) output[lag] = 0;
        else output[lag] = n;
    }
}

template <typename T>
void find_peaks(T* arr, int length, int* peaks, int psize)
{
    //Clear any peaks from previous calls
    std::memset(peaks, 0, psize * sizeof(peaks[0]));

    int peak_index = 0;
    float current_max = 0;
    int current_max_pos = 0;
    int pos = 0;

    //Skip over the initial peak and zero crossing
    while (pos < length && arr[pos] >= 0.0) pos++;
    while (pos < length && arr[pos] <= 0.0) pos++;

    while (pos < length - 1)
    {
        if (arr[pos] < 0.0 && arr[pos - 1] >= 0.0) //Downward zero crossing
        {
            if (peak_index == psize) return; //Exceeded requested number of peaks
            peaks[peak_index++] = current_max_pos;
            current_max = 0;
        }
        else if (arr[pos] > arr[pos-1] && arr[pos] > arr[pos+1] && arr[pos] > current_max) {
            current_max = arr[pos];
            current_max_pos = pos;
        }
        pos++;
    }
}

template <typename T>
double choose_fundamental(T* nsdf, int* peaks, int psize, double sample_rate, double threshold)
{
    for (int i = 0; i < psize; ++i)
    {
        int peak_location = peaks[i];
        if (peak_location == 0) return 0;
        if (nsdf[peak_location] >= threshold)
        {
            double corrected = parabolic_interpolation(nsdf, peak_location);
            return lag_to_hertz(corrected, sample_rate);
        }
    }
    return 0;
}


template <typename T>
double parabolic_interpolation(T* arr, int peak)
{
    double a = arr[peak - 1];
    double b = arr[peak];
    double c = arr[peak + 1];

    double offset = (a - c) / (2.0 * (a - 2.0 * b + c));
    if (std::isnan(offset)) return peak;
    return peak + offset;
}