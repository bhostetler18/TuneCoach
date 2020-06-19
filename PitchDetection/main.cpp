#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include "processing_utilities.h"
#include "PitchDetector.h"
#include "CircularBuffer.h"

#ifdef USE_PULSE
    #include <pulse/simple.h>
#endif
#ifdef USE_ALSA
#define ALSA_PCM_NEW_HW_PARAMS_API
    #include <alsa/asoundlib.h>
#endif

int main()
{
    int rc;
    unsigned int sample_rate = 44100;
    int buffer_size = 2048;
    float* buffer;

#ifdef USE_PULSE
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
#endif
#ifdef USE_ALSA
    snd_pcm_t *handle;
    snd_pcm_hw_params_t *params;
    int dir = 0;

    /* Open PCM device for recording (capture). */
    rc = snd_pcm_open(&handle, "default",
                      SND_PCM_STREAM_CAPTURE, 0);
    if (rc < 0) {
        std::cout << snd_strerror(rc) << std::endl;
        exit(1);
    }

    /* Allocate a hardware parameters object. */
    snd_pcm_hw_params_alloca(&params);

    /* Fill it in with default values. */
    snd_pcm_hw_params_any(handle, params);

    /* Set the desired hardware parameters. */

    /* Interleaved mode */
    snd_pcm_hw_params_set_access(handle, params,
                                 SND_PCM_ACCESS_RW_INTERLEAVED);

    /* Signed 32-bit little-endian float format */
    snd_pcm_hw_params_set_format(handle, params,
                                 SND_PCM_FORMAT_FLOAT_LE);

    /* One channel (mono) */
    snd_pcm_hw_params_set_channels(handle, params, 1);

    /* Set sample rate near 44100 (sample_rate will be overwritten if a different rate is set) */
    snd_pcm_hw_params_set_rate_near(handle, params,
                                    &sample_rate, &dir);
    std::cout << "SAMPLE RATE: " << sample_rate << std::endl;

    /* Set period size near buffer_size frames. */
    snd_pcm_uframes_t frames = buffer_size;
    snd_pcm_hw_params_set_period_size_near(handle,
                                           params, &frames, &dir);
    std::cout << "BUFFER LENGTH: " << frames << std::endl;
    buffer_size = frames;

    /* Write the parameters to the driver */
    rc = snd_pcm_hw_params(handle, params);
    if (rc < 0) {
        std::cout << snd_strerror(rc) << std::endl;
        exit(1);
    }

    /* Use a buffer large enough to hold one period */
    //buffer_size = (int)frames * 2; /* 2 bytes/sample, 1 channel */
#endif

    buffer = new float[buffer_size];
    PitchDetector p(sample_rate, buffer_size, 60.0);

    std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};

//    CircularBuffer<double, 256> c;
//    std::thread read_thread( [&] () {
//        while(true) {
//            std::this_thread::sleep_for(std::chrono::milliseconds(15));
//            double a = 7;
//            while (!c.read(a)) {
//                //std::cout << "NO DATA" << std::endl;
//            }
//            std::cout << a << std::endl;
//        }
//    });

    int count = 0;
    while (true)
    {
#ifdef USE_PULSE
        rc = pa_simple_read(server, buffer, buffer_size*4, nullptr);
        if(rc) break;
#endif
#ifdef USE_ALSA
        rc = snd_pcm_readi(handle, buffer, frames);
        if (rc != buffer_size) break;
#endif
        double detected_hz = p.get_frequency(buffer);
//        if (!c.write(detected_hz)) {
//            std::cout << "OVERFLOW" << std::endl;
//        }
//        count++;
//        std::cout << "written " << count << std::endl;
        if (detected_hz != 0) {
            int midi = (int)round(hz_to_midi(detected_hz));
            std::string name = notes[midi % 12];
            double desired_hz = closest_in_tune_frequency(detected_hz);
            double cent = cents(desired_hz, detected_hz);
            std::cout << name << "    " << detected_hz << "    " << cent << "  cents" << std::endl;
        }
    }


#ifdef USE_PULSE
    pa_simple_free(server);
#endif
#ifdef USE_ALSA
    snd_pcm_drain(handle);
    snd_pcm_close(handle);
#endif

    delete[] buffer;

    return 0;
}