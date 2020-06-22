#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
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
    auto start = chrono::steady_clock::now();

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
                t.kill();
                cout << "KILLING" << endl;
            }
        }

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
                data.collectData(midi % 12, cent);
                std::cout << name << "    " << freq << "    " << cent << "  cents" << "    " << data.getOverall() << std::endl;
            }
        }
    });



    t.start();
    stopper.join();
    reader.join();

    auto end = chrono::steady_clock::now();
    int time = chrono::duration_cast<chrono::seconds>(end - start).count();
    int minutes = time / 60;
    int seconds = time % 60;

    cout << "Here are the results of this session:" << endl;
    cout << "-------------------------------------" << endl;
    if(minutes == 0){
        cout << "This session lasted " << seconds << " seconds." << endl;
    }
    else{
        cout << "This session lasted " << minutes << " minutes and " << seconds << " seconds." << endl;
    }
    cout << endl;

    data.displayData();
    return 0;
}