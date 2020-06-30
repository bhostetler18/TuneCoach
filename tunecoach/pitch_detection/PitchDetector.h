#pragma once

class PitchDetector
{
public:
    PitchDetector(int sample_rate, int buffer_size, double lowest_freq);

    double get_frequency(float* buffer);
    void set_threshold(double t);
    void set_frequency_cap(double cap);

    PitchDetector& operator=(const PitchDetector&) = delete;
    PitchDetector(const PitchDetector&) = delete;
    ~PitchDetector();

private:
    int sample_rate;
    int buffer_size;

    int nsdf_size;
    float* nsdf;
    int maxima[64];

    double threshold = 0.8;
    double hz_min;
    double hz_max;
};