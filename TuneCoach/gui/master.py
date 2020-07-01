from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.PitchDisplay import *
from tkinter import *
from TuneCoach.python_bridge.AudioManager import *
import time


def space_pressed(event, mainWindow):
    mainWindow.toggle_pause()

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


def cleanup(mainWindow):
    if not mainWindow.save_practice_session(ask=True):
        return # do not close if we're saving and then we cancel
    if mainWindow.audio_manager is not None:
        mainWindow.audio_manager.destroy()
    mainWindow.master.destroy()



def main():
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    our_window = MainWindow(root)
    root.bind('<space>', lambda event, arg=our_window: space_pressed(event, arg))
    root.wm_protocol("WM_DELETE_WINDOW", lambda w=our_window: cleanup(w))
    root.mainloop()


if __name__ == "__main__":
    main()
