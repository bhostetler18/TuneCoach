from TuneCoach.gui.MainWindow import *
from TuneCoach.gui.PitchDisplay import *
from tkinter import *
from TuneCoach.python_bridge.AudioManager import *
import time


def main():
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    our_window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
