#ifndef PITCHDETECTION_FEEDBACKSYSTEM_H
#define PITCHDETECTION_FEEDBACKSYSTEM_H
#include <string>
#include <iostream>
using namespace std;

class FeedbackSystem {
public:
    FeedbackSystem();
    static double percentError(double actual, double theoretical);
    void collectData(const string &note, double detected, double desired, double cent);
    double displayOverall();
    void displayData();

private:
    double C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B;
    int C_cnt, Db_cnt, D_cnt, Eb_cnt, E_cnt, F_cnt, Gb_cnt, G_cnt, Ab_cnt, A_cnt, Bb_cnt, B_cnt;
    double cents;
    double overall;
};


#endif
