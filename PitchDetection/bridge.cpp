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

void kill_stream(TunerStream* handle)
{
    handle->kill();
    delete handle;
}

bool is_alive(TunerStream* handle)
{
    return handle->isAlive();
}

bool read_stream(TunerStream* handle, double* val)
{
    return handle->fetch_freq(*val);
}

double peek_stream(TunerStream* handle)
{
    return handle->peek();
}
