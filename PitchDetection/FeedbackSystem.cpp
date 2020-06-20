#include "FeedbackSystem.h"

FeedbackSystem::FeedbackSystem() {
    C = 0.0, Db = 0.0, D = 0.0, Eb = 0.0, E = 0.0, F = 0.0;
    Gb = 0.0, G = 0.0, Ab = 0.0, A = 0.0, Bb = 0.0, B = 0.0;

    C_cnt = 0, Db_cnt = 0, D_cnt = 0, Eb_cnt = 0, E_cnt = 0, F_cnt = 0;
    Gb_cnt = 0, G_cnt = 0, Ab_cnt = 0, A_cnt = 0, Bb_cnt = 0, B_cnt = 0;

    cents = 0.0;
    overall = 0.0;
}

double FeedbackSystem::percentError(double actual, double theoretical) {
    return abs((actual - theoretical) / theoretical);
}

void FeedbackSystem::collectData(const string &note, double detected, double desired, double cent) {
    cents += abs(cent);
    double error = percentError(detected, desired);
    overall += error;

    if(note == "C"){
        C += error;
        C_cnt++;
    }
    else if(note == "Db"){
        Db += error;
        Db_cnt++;
    }
    else if(note == "D"){
        D += error;
        D_cnt++;
    }
    else if(note == "Eb"){
        Eb += error;
        Eb_cnt++;
    }
    else if(note == "E"){
        E += error;
        E_cnt++;
    }
    else if(note == "F"){
        F += error;
        F_cnt++;
    }
    else if(note == "Gb"){
        Gb += error;
        Gb_cnt++;
    }
    else if(note == "G"){
        G += error;
        G_cnt++;
    }
    else if(note == "Ab"){
        Ab += error;
        Ab_cnt++;
    }
    else if(note == "A"){
        A += error;
        A_cnt++;
    }
    else if(note == "Bb"){
        Bb += error;
        Bb_cnt++;
    }
    else if(note == "B"){
        B += error;
        B_cnt++;
    }
}

double FeedbackSystem::displayOverall() {
    int tot_cnt = C_cnt + Db_cnt + D_cnt + Eb_cnt + E_cnt + F_cnt + Gb_cnt + G_cnt + Ab_cnt + A_cnt + Bb_cnt + B_cnt;
    double overall_err = 100 - ((100.0/tot_cnt) * overall);
    return overall_err;
}

void FeedbackSystem::displayData() {
    int tot_cnt = C_cnt + Db_cnt + D_cnt + Eb_cnt + E_cnt + F_cnt + Gb_cnt + G_cnt + Ab_cnt + A_cnt + Bb_cnt + B_cnt;
    double avgCents = cents/tot_cnt;
    double C_err = 100 - ((100.0/C_cnt) * C);
    double Db_err = 100 - ((100.0/Db_cnt) * Db);
    double D_err = 100 - ((100.0/D_cnt) * D);
    double Eb_err = 100 - ((100.0/Eb_cnt) * Eb);
    double E_err = 100 - ((100.0/E_cnt) * E);
    double F_err = 100 - ((100.0/F_cnt) * F);
    double Gb_err = 100 - ((100.0/Gb_cnt) * Gb);
    double G_err = 100 - ((100.0/G_cnt) * G);
    double Ab_err = 100 - ((100.0/Ab_cnt) * Ab);
    double A_err = 100 - ((100.0/A_cnt) * A);
    double Bb_err = 100 - ((100.0/Bb_cnt) * Bb);
    double B_err = 100 - ((100.0/B_cnt) * B);
    double overall_err = 100 - ((100.0/tot_cnt) * overall);

    cout << "Here are the results of this session:" << endl;
    cout << endl;
    cout << "These are your accuracies for each pitch class:" << endl;
    cout << "C was in tune for " << C_err << "% of the time." << endl;
    cout << "Db was in tune for " << Db_err << "% of the time." << endl;
    cout << "D was in tune for " << D_err << "% of the time." << endl;
    cout << "Eb was in tune for " << Eb_err << "% of the time." << endl;
    cout << "E was in tune for " << E_err << "% of the time." << endl;
    cout << "F was in tune for " << F_err << "% of the time." << endl;
    cout << "Gb was in tune for " << Gb_err << "% of the time." << endl;
    cout << "G was in tune for " << G_err << "% of the time." << endl;
    cout << "Ab was in tune for " << Ab_err << "% of the time." << endl;
    cout << "A was in tune for " << A_err << "% of the time." << endl;
    cout << "Bb was in tune for " << Bb_err << "% of the time." << endl;
    cout << "B was in tune for " << B_err << "% of the time." << endl;
    cout << "Overall, you were in tune for " << overall_err << "% of the time, and you were off by " << avgCents << " cents." << endl;
}