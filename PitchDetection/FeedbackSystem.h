#ifndef PITCHDETECTION_FEEDBACKSYSTEM_H
#define PITCHDETECTION_FEEDBACKSYSTEM_H
#include <string>
#include <iostream>
#include <cmath>
#include <queue>
using namespace std;

class FeedbackSystem {
public:
    explicit FeedbackSystem(int threshold);
    void collectData(int index, double cent);
    double getOverall() const;
    queue<string> getRecentNotes();
    void displayData();


private:
    string notes[12] = {"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"};
    int pitchClass[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int pitchCount[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    double cents;
    int overall;
    int overallCount;
    int threshold;
    queue<string> recentNotes;
};


#endif
