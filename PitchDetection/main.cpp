#include <iostream>
#include <cmath>
#include <pulse/simple.h>
#include <chrono>
#include "processing_utilities.h"
#include "PitchDetector.h"

int main()
{
    int rc;
    int sample_rate = 44100;

    pa_simple *server;
    pa_sample_spec sample_format;
    sample_format.format = PA_SAMPLE_FLOAT32LE;
    sample_format.channels = 1;
    sample_format.rate = sample_rate;
    int err;
    server = pa_simple_new(nullptr,               // Use the default server.
                      "TuneCoach",           // Our application's name.
                      PA_STREAM_RECORD,
                      nullptr,               // Use the default device.
                      "Audio capture",            // Description of our stream.
                      &sample_format,                // Our sample format.
                      nullptr,               // Use default channel map
                      nullptr,               // Use default buffering attributes.
                      &err
    );

    const int buffer_size = 2048;
    float buffer[buffer_size];
    PitchDetector p(sample_rate, buffer_size, 60.0);

    std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};

    while (true)
    {
        rc = pa_simple_read(server, buffer, buffer_size*4, nullptr);
        if (rc) break; // TODO error checking for underrun and other issues

        double detected_hz = p.get_frequency(buffer);
        if (detected_hz != 0) {
            double note = hz_to_midi(detected_hz);
            int midi = (int) round(note);
            std::string name = notes[midi % 12];
            double desired_hz = midi_to_hz(midi);
            double cent = cents(desired_hz, detected_hz);
            std::cout << name << "    " << detected_hz << "    " << cent << "  cents" << std::endl;
        }
    }

    pa_simple_free(server);
    return 0;
}