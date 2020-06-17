#define ALSA_PCM_NEW_HW_PARAMS_API
#include <alsa/asoundlib.h>
#include <iostream>
#include <cmath>
#include "processing_utilities.h"
#include <pulse/simple.h>
#include <chrono>

int main()
{
    int rc;
    unsigned int sample_rate = 44100;

    pa_simple *s;
    pa_sample_spec ss;
    ss.format = PA_SAMPLE_FLOAT32LE;
    ss.channels = 1;
    ss.rate = sample_rate;
    int err;
    s = pa_simple_new(nullptr,               // Use the default server.
                      "TuneCoach",           // Our application's name.
                      PA_STREAM_RECORD,
                      nullptr,               // Use the default device.
                      "Audio capture",            // Description of our stream.
                      &ss,                // Our sample format.
                      nullptr,               // Use default channel map
                      nullptr,               // Use default buffering attributes.
                      &err
    );

    float buffer[4096];

    //Pitch detection parameters and storage
    std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
    double lowest_freq = 65.406;
    const int nsdf_size = hertz_to_lag(lowest_freq, sample_rate);
    auto* nsdf = new float[nsdf_size]; //allocate memory for nsdf results to avoid constant reallocation
    // TODO: potentially put this back on the stack and hardcode nsdf_size for efficiency

    int maxima[64]; //For now 64 seems fine (see the find_peaks function)

    while (true)
    {
        rc = pa_simple_read(s, buffer, 2048, nullptr);
        assert(rc == 0);   // TODO error checking for underrun and other issues

        normalized_square_difference_optimized(buffer, 2048, nsdf_size, nsdf);
        find_peaks(nsdf, nsdf_size, maxima, 64);
        double detected_hz = choose_fundamental(nsdf, maxima, 64, sample_rate, 0.8);
        if (detected_hz != 0) {
            double note = hz_to_midi(detected_hz);
            int midi = (int) round(note);
            std::string name = notes[midi % 12];
            double desired_hz = midi_to_hz(midi);
            double cent = cents(desired_hz, detected_hz);
            std::cout << name << "    " << detected_hz << "    " << cent << "  cents" << std::endl;
        }
    }

//    snd_pcm_drain(handle);
//    snd_pcm_close(handle);
//    free(buffer);

    return 0;
}
