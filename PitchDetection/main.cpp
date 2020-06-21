#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <ctime>
#include "processing_utilities.h"
#include "TunerStream.h"
#include "FeedbackSystem.h"

/* TODO:
 Octave numbers

*/

int main(){
    cout << "Please enter a threshold for intonation forgiveness in cents: ";
    int threshold;
    cin >> threshold;
    cout << endl;
    FeedbackSystem data(threshold);

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
    clock_t clk;

    std::thread reader([&]{
        clk = clock();
        while(t.isAlive()) {
            // Pauses, resumes, and stops program based on input
            if(cin.get() == ' '){
                if(!t.isPaused()){
                    t.pause();
                    cout << "PAUSING" << endl;
                }
                else{
                    t.resume();
                    cout << "RESUMING" << endl;
                }
            }
            if(cin.get() == 'q'){
                clk = clock() - clk;
                t.kill();
                cout << "KILLING" << endl;
            }

            double freq;
            std::string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
            while(!t.fetch_freq(freq));
            if (freq != 0) {
                int midi = (int)round(hz_to_midi(freq));
                std::string name = notes[midi % 12];
                double desired_hz = closest_in_tune_frequency(freq);
                double cent = cents(desired_hz, freq);
                data.collectData(midi % 12, cent);
                std::cout << name << "    " << freq << "    " << cent << "  cents" << "    " << data.getOverall() << std::endl;
            }
        }
    });

    std::thread gui([&]{
        while(t.isAlive()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(150));
            std::cout << "PEEK: " << t.peek() << std::endl;
        }
    });

    int minutes = int(clk) / 60;
    int seconds = int(clk) % 60;

    t.start();
    stopper.join();
    reader.join();
    gui.join();
    cout << "This session lasted " << minutes << " and " << seconds << " seconds" << endl;
    data.displayData();
    return 0;
}