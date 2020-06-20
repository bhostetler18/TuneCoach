#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include "processing_utilities.h"
#include "TunerStream.h"

int main()
{
    TunerStream t(44100);
    std::thread stopper([&]{
        std::this_thread::sleep_for(std::chrono::milliseconds(1200));
        std::cout << "PAUSING" << std::endl;
        t.pause();
        std::this_thread::sleep_for(std::chrono::milliseconds(5000));
        std::cout << "RESUMING" << std::endl;
        t.resume();
        std::this_thread::sleep_for(std::chrono::milliseconds(5000));
        std::cout << "KILLING" << std::endl;
        t.kill();
    });

    std::thread reader([&]{
        while(t.isAlive()) {
            double freq;
            std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
            while(!t.fetch_freq(freq));
            if (freq != 0) {
                int midi = (int)round(hz_to_midi(freq));
                std::string name = notes[midi % 12];
                double desired_hz = closest_in_tune_frequency(freq);
                double cent = cents(desired_hz, freq);
                std::cout << name << "    " << freq << "    " << cent << "  cents" << std::endl;
            }
        }
    });

    std::thread gui([&]{
        while(t.isAlive()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(150));
            std::cout << "PEEK: " << t.peek() << std::endl;
        }
    });

    t.start();
    stopper.join();
    reader.join();
    gui.join();

    return 0;
}