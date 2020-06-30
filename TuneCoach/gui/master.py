from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.PitchDisplay import *
from tkinter import *
from TuneCoach.python_bridge.Session import *
from TuneCoach.python_bridge.AudioManager import *
import time


def space_pressed(event, mainWindow):
    mainWindow.toggle_pause()


def kill_pressed(event, mainWindow):
    print("Killing")
    print("")
    # end = time.time()
    # elapsed_time = end - start
    # minutes = int(elapsed_time) // 60
    # seconds = int(elapsed_time) % 60

    # print("Here are the results of this session:")
    # print("-------------------------------------")
    # if minutes == 0:
    #     print("This session lasted", seconds, "seconds.")
    # elif minutes == 1:
    #     print("This session lasted", minutes, "minute and", seconds, "seconds.")
    # else:
    #     print("This session lasted", minutes, "minutes and", seconds, "seconds.")
    # print("")
    mainWindow.currentPracticeSession.display_all_data()
    mainWindow.audio_manager.destroy()


def cleanup(mainWindow):
    if mainWindow.audio_manager is not None:
        mainWindow.audio_manager.destroy()
    mainWindow.master.destroy()

def score_update(mainWindow):
    if not mainWindow.isPaused:
        mainWindow.myDiagnosticObject.overallScoreLabel.config(text="Overall Score: %.2f" % mainWindow.currentPracticeSession.get_overall())
        mainWindow.myDiagnosticObject.update_plot(int(mainWindow.currentPracticeSession.get_overall()), mainWindow)
        print(mainWindow.currentPracticeSession.get_overall())
    mainWindow.master.after(500, lambda: score_update(mainWindow))

def piano_update(mainWindow):
    mainWindow.myHistoryObject.update(mainWindow.currentPracticeSession)
    mainWindow.master.after(20, lambda: piano_update(mainWindow))


def main():
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    our_window = MainWindow(root)
    root.bind('<space>', lambda event, arg=our_window: space_pressed(event, arg))
    root.bind('q', lambda event, arg=our_window: kill_pressed(event, arg))
    root.wm_protocol("WM_DELETE_WINDOW", lambda w=our_window: cleanup(w))
    score_update(our_window)
    piano_update(our_window)
    root.mainloop()


if __name__ == "__main__":
    main()
