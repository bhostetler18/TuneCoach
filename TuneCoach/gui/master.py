from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.PitchDisplay import *
from tkinter import *
from TuneCoach.python_bridge.AudioManager import *
import time




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



def main():
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    our_window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
