#include "FeedbackSystem.h"

FeedbackSystem::FeedbackSystem() {
    cents = 0.0;
    overall = 0;
    overallCount = 0;
}

void FeedbackSystem::collectData(int index, double cent) {
    if(abs(cent) <= 5){
        pitchClass[index]++;
        overall++;
    }
    pitchCount[index]++;
    overallCount++;
    cents += abs(cent);
}

double FeedbackSystem::getOverall() {
    return (100.0 * overall)/overallCount;
}

void FeedbackSystem::displayData() {
    double pitchError[12];
    for(int i = 0; i < 11; i++){
        pitchError[i] = (100.0 * pitchClass[i]) / pitchCount[i];
    }
    double avgCents = cents/overallCount;

    cout << "Here are the results of this session:" << endl;
    cout << endl;
    cout << "These are your accuracies for each pitch class:" << endl;

    for(int i = 0; i < 11; i++){
        if(isnan(pitchError[i])){
            cout << notes[i] << " was not played/sung in the session." << endl;
        }
        else{
            cout << notes[i] << " was in tune for " << pitchError[i] << "% of the time." << endl;
        }
    }
    cout << endl;
    cout << "Overall:" << endl;
    cout << "You were in tune for " << getOverall() << "% of the time." << endl;
    cout << "You were off by an average of " << avgCents << " cents." << endl;
}