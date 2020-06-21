#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <ctime>
#include "processing_utilities.h"
#include "TunerStream.h"
#include "FeedbackSystem.h"

/* TODO:
 * Octave numbers
 * Fix input interrupt
*/

int main(){
    cout << "Please enter a threshold for intonation forgiveness in cents: ";
    int threshold;
    cin >> threshold;
    cout << endl;
    FeedbackSystem data(threshold);
    clock_t clk;

    TunerStream t(44100);

    std::thread stopper([&]{
        char in;
        while(t.isAlive()){
            cin.get(in);
            if(in == ' '){
                if(!t.isPaused()){
                    t.pause();
                    cout << "PAUSING" << endl;
                }
                else{
                    t.resume();
                    cout << "RESUMING" << endl;
                }
            }
            if(in == 'q'){
                clk = clock() - clk;
                t.kill();
                cout << "KILLING" << endl;
            }
        }

    });


    std::thread reader([&]{
        if(t.isAlive()){
            clk = clock();
        }
        while(t.isAlive()) {
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

    //clk = clock() - clk;
    int minutes = int(clk) / 60;
    int seconds = int(clk) % 60;

    t.start();
    stopper.join();
    reader.join();
    cout << "This session lasted " << minutes << " and " << seconds << " seconds" << endl;
    data.displayData();
    return 0;
}