#include "FeedbackSystem.h"

FeedbackSystem::FeedbackSystem() {
    cents = 0.0;
    overall = 0.0;
}

double FeedbackSystem::percentError(double actual, double theoretical) {
    return abs((actual - theoretical) / theoretical);
}

void FeedbackSystem::collectData(int index, double detected, double desired, double cent) {
    cents += abs(cent);
    double error = percentError(detected, desired);
    overall += error;

    pitchClass[index] += error;
    pitchCount[index]++;
}

double FeedbackSystem::displayOverall() {
    int tot_cnt = 0;
    for(int i = 0; i < 11; i++){
        tot_cnt += pitchCount[i];
    }
    double overall_err = 100 - ((100.0/tot_cnt) * overall);
    return overall_err;
}

void FeedbackSystem::displayData() {
    int tot_cnt = 0;
    double pitchError[12];
    for(int i = 0; i < 11; i++){
        tot_cnt += pitchCount[i];
        pitchError[i] = 100 - ((100.0/pitchCount[i]) * pitchClass[i]);
    }
    double avgCents = cents/tot_cnt;
    double overall_err = 100 - ((100.0/tot_cnt) * overall);

    cout << "Here are the results of this session:" << endl;
    cout << endl;
    cout << "These are your accuracies for each pitch class:" << endl;
    for(int i = 0; i < 11; i++){
        cout << notes[i] << " was in tune for " << pitchError[i] << "% of the time." << endl;
    }
    cout << "Overall, you were in tune for " << overall_err << "% of the time, and you were off by " << avgCents << " cents." << endl;
}