cmake_minimum_required(VERSION 3.16)
project(PitchDetection)

set(CMAKE_CXX_STANDARD 14)
#link_libraries(asound)
link_libraries(pulse-simple)
SET(CMAKE_CXX_FLAGS -pthread)
add_definitions(-DUSE_PULSE)

add_executable(PitchDetection main.cpp processing_utilities.h processing_utilities.cpp PitchDetector.cpp PitchDetector.h
        CircularBuffer.h bridge.h TunerStream.cpp TunerStream.h bridge.cpp)
