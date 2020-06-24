#include <iostream>
#include "TunerStream.h"

TunerStream::TunerStream(int sample_rate)
{
    this->sample_rate = sample_rate;
    this->alive = true;
    this->paused = true;
    this->was_started = false;
    this->most_recent = 0.0;

#ifdef USE_PULSE
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
    snd_pcm_hw_params_t *params;
    int dir = 0;

    /* Open PCM device for recording (capture). */
    int rc = snd_pcm_open(&handle, "default",
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
                                    &this->sample_rate, &dir);
    std::cout << "SAMPLE RATE: " << this->sample_rate << std::endl;

    /* Set period size near buffer_size frames. */
    snd_pcm_uframes_t frames = audio_buffer_size;
    snd_pcm_hw_params_set_period_size_near(handle,
                                           params, &frames, &dir);
    std::cout << "BUFFER LENGTH: " << frames << std::endl;
    audio_buffer_size = frames;

    /* Write the parameters to the driver */
    rc = snd_pcm_hw_params(handle, params);
    if (rc < 0) {
        std::cout << snd_strerror(rc) << std::endl;
        exit(1);
    }

    /* Use a buffer large enough to hold one period */
    //buffer_size = (int)frames * 2; /* 2 bytes/sample, 1 channel */
#endif

    this->audio_buffer = new float[audio_buffer_size];
    p = new PitchDetector(sample_rate, audio_buffer_size, 60.0);
}

void TunerStream::start()
{
    if (was_started)
    {
        std::cout << "Don't do that" << std::endl;
        return;
    }
    was_started = true;
    paused = false;
    int rc;
#ifdef USE_ALSA
    snd_pcm_uframes_t frames = audio_buffer_size;
#endif
    while (alive)
    {
        while (!paused)
        {
#ifdef USE_PULSE
            rc = pa_simple_read(server, audio_buffer, audio_buffer_size*4, nullptr);
            if(rc) break;
#endif
#ifdef USE_ALSA
            rc = snd_pcm_readi(handle, audio_buffer, frames);
            if (rc != audio_buffer_size) break;
#endif
            double detected_hz = p->get_frequency(audio_buffer);
            this->buffer.write(detected_hz);
            this->most_recent = detected_hz;
        }
        this->most_recent = 0.0;
    }
}

void TunerStream::pause()
{
    this->paused = true;
    this->most_recent = 0.0;
}

void TunerStream::resume()
{
    this->paused = false;
}

void TunerStream::kill()
{
    this->paused = true;
    this->alive = false;
}

bool TunerStream::isAlive()
{
    return alive;
}

bool TunerStream::isPaused()
{
    return paused;
}

bool TunerStream::fetch_freq(double &hz)
{
    return this->buffer.read(hz);
}

double TunerStream::peek()
{
    return most_recent;
}


TunerStream::~TunerStream()
{
    std::cout << "DESTROYED TUNER STREAM" << std::endl;
#ifdef USE_PULSE
    pa_simple_free(server);
#endif
#ifdef USE_ALSA
    snd_pcm_drain(handle);
    snd_pcm_close(handle);
#endif
    delete[] this->audio_buffer;
    delete p;
}



