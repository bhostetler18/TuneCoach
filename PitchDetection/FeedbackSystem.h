#ifndef PITCHDETECTION_FEEDBACKSYSTEM_H
#define PITCHDETECTION_FEEDBACKSYSTEM_H
#include <string>
#include <iostream>
using namespace std;

class FeedbackSystem {
public:
    FeedbackSystem();
    static double percentError(double actual, double theoretical);
    void collectData(int index, double detected, double desired, double cent);
    double displayOverall();
    void displayData();

private:
    string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
    double pitchClass[12] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    int pitchCount[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    double cents;
    double overall;
};


#endif
