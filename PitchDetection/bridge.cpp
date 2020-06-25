#include <iostream>
#include "bridge.h"

TunerStream *create_stream(int sample_rate)
{
    return new TunerStream(sample_rate);
}

void start_stream(TunerStream *handle)
{
    if (handle) handle->start();
}

void pause_stream(TunerStream* handle)
{
    if (handle) handle->pause();
}

void resume_stream(TunerStream* handle)
{
    if (handle) handle->resume();
}

void kill_stream(TunerStream* handle)
{
    if (handle) handle->kill();
    while (!handle->isSafeToDelete());
    delete handle;
}

bool is_alive(TunerStream* handle)
{
    return handle && handle->isAlive();
}

bool is_paused(TunerStream* handle)
{
    return handle && handle->isPaused();
}

bool read_stream(TunerStream* handle, double* val)
{
    if (handle) return handle->fetch_freq(*val);
    return false;
}

double peek_stream(TunerStream* handle)
{
    if (handle) return handle->peek();
    return 0;
}
