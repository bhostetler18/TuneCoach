#pragma once
#include <atomic>
#include <cstddef>

template <typename T, uint32_t size>
class CircularBuffer
{
public:
    CircularBuffer();
    bool write(T data);
    bool read(T& out);

private:
    T* _buff;
    uint32_t capacity;
    uint32_t mask;
    std::atomic_uint32_t read_idx;
    std::atomic_uint32_t write_idx;

};

template <typename T, uint32_t size>
CircularBuffer<T, size>::CircularBuffer() : capacity(size), mask(size-1), read_idx(0), write_idx(0)
{
    static_assert(size && !(size & (size - 1)), "Buffer size must be a power of 2");
    _buff = new T[size];
}

template<typename T, uint32_t size>
bool CircularBuffer<T, size>::write(T data) {
    int next = (write_idx + 1) & mask;
    if (next == read_idx) return false;
    _buff[write_idx] = data;
    write_idx = next;
    return true;
}

template<typename T, uint32_t size>
bool CircularBuffer<T, size>::read(T& out) {
    if (read_idx == write_idx) return false;
    out = _buff[read_idx];
    read_idx = (read_idx + 1) & mask;
    return true;
}

