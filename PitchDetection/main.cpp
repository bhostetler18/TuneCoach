#define ALSA_PCM_NEW_HW_PARAMS_API
#include <alsa/asoundlib.h>
#include <iostream>
#include <cmath>
#include "processing_utilities.h"
#include <typeinfo>

int main() //initial ALSA setup based on https://www.linuxjournal.com/article/6735
{
    //ALSA parameters
    int rc;
    snd_pcm_t *handle;
    snd_pcm_hw_params_t *params;
    int dir = 0;
    float *buffer;

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

    /* Signed 16-bit little-endian float format */
    snd_pcm_hw_params_set_format(handle, params,
                                 SND_PCM_FORMAT_FLOAT_LE);

    /* One channel (mono) */
    snd_pcm_hw_params_set_channels(handle, params, 1);

    /* Set sample rate near 44100 (sample_rate will be overwritten if a different rate is set) */
    unsigned int sample_rate = 44100;
    snd_pcm_hw_params_set_rate_near(handle, params,
                                    &sample_rate, &dir);
    std::cout << "SAMPLE RATE: " << sample_rate << std::endl;

    /* Set period size near 2048 frames. */
    snd_pcm_uframes_t frames = 2048;
    snd_pcm_hw_params_set_period_size_near(handle,
                                           params, &frames, &dir);
    std::cout << "BUFFER LENGTH: " << sample_rate << std::endl;

    /* Write the parameters to the driver */
    rc = snd_pcm_hw_params(handle, params);
    if (rc < 0) {
        std::cout << snd_strerror(rc) << std::endl;
        exit(1);
    }

    /* Use a buffer large enough to hold one period */
    snd_pcm_hw_params_get_period_size(params,
                                      &frames, &dir);
    std::cout << frames << std::endl;
    int size = (int)frames * 2; /* 2 bytes/sample, 1 channel */
    buffer = new float[size];

    //Pitch detection parameters and storage
    std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
    double lowest_freq = 65.406;
    const int nsdf_size = hertz_to_lag(lowest_freq, sample_rate);
    auto* nsdf = new float[nsdf_size]; //allocate memory for nsdf results to avoid constant reallocation
    int maxima[64]; //For now 64 seems fine (see the find_peaks function)

    while (true)
    {
        rc = snd_pcm_readi(handle, buffer, frames);
        assert(rc == frames); // rc should be set to the number of frames read
        // TODO error checking for underrun and other issues

        normalized_square_difference(buffer, 2048, 0, nsdf_size, nsdf);
        find_peaks(nsdf, nsdf_size, maxima, 64);
        double detected_hz = choose_fundamental(nsdf, maxima, 64, sample_rate, 0.8);
        if (detected_hz != 0)
        {
            double note = hz_to_midi(detected_hz);
            int midi = (int)round(note);
            std::string name = notes[midi%12];
            double desired_hz = 440.0 * pow(2.0, (float)(midi - 69)/12.0);
            double cent = cents(desired_hz, detected_hz);
            std::cout << name << "    " << detected_hz << "    " << cent << "  cents" << std::endl;
        }
    }

    snd_pcm_drain(handle);
    snd_pcm_close(handle);
    free(buffer);

    return 0;
}
