#include "bridge.h"

TunerStream *create_stream(int sample_rate)
{
    return new TunerStream(sample_rate);
}

void start_stream(TunerStream *handle)
{
    handle->start();
}

void pause_stream(TunerStream* handle)
{
    handle->pause();
}

void resume_stream(TunerStream* handle)
{
    handle->resume();
}

void stop_stream(TunerStream* handle)
{
    handle->kill();
}

bool read_stream(TunerStream* handle, double* val)
{
    return handle->fetch_freq(*val);
}
