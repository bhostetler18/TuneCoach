#include "PitchDetector.h"
#include "processing_utilities.h"

PitchDetector::PitchDetector(int sample_rate, int buffer_size, double lowest_freq)
{
    this->sample_rate = sample_rate;
    this->buffer_size = buffer_size;
    this->nsdf_size = hertz_to_lag(lowest_freq, sample_rate);
    this->nsdf = new float[nsdf_size]; //allocate memory for nsdf results to avoid constant reallocation
    this->hz_min = lowest_freq;
    this->hz_max = 4000.0; //default for now (slightly sharp B7)
}

double PitchDetector::get_frequency(float *buffer)
{
    normalized_square_difference_optimized(buffer, buffer_size, nsdf_size, nsdf);
    find_peaks(nsdf, nsdf_size, maxima, 64);
    double detected_hz = choose_fundamental(nsdf, maxima, 64, sample_rate, threshold);
    //no need to check hz_min as pitch finding algorithm can't return less than hz_min due to the size of the nsdf
    if (detected_hz > hz_max) return 0;
    return detected_hz;
}

void PitchDetector::set_threshold(double t)
{
    this->threshold = std::min(1.0, std::max(0.0, t));
}

void PitchDetector::set_frequency_cap(double cap)
{
    this->hz_max = cap;
}

PitchDetector::~PitchDetector()
{
    delete[] this->nsdf;
}

