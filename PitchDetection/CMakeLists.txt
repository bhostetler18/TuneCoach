cmake_minimum_required(VERSION 3.16)
project(PitchDetection)

set(CMAKE_CXX_STANDARD 14)
#link_libraries(asound)
link_libraries(pulse-simple)

add_executable(PitchDetection main.cpp processing_utilities.h processing_utilities.cpp)