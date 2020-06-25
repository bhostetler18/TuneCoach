# import gui
from gui import *
from pitchDisplay import *
from tkinter import *
from FeedbackSystem import *
from AudioManager import *
import time
sys.path.insert(1, '../python_bridge')


def space_pressed(event, audio_manager):
    if audio_manager.is_paused():
        print("Resuming")
        audio_manager.resume()
    else:
        print("Pausing")
        audio_manager.pause()


def kill_pressed(event, audio_manager, data, start):
    print("Killing")
    end = time.time()
    elapsed_time = end - start
    minutes = int(elapsed_time) // 60
    seconds = int(elapsed_time) % 60

    print("Here are the results of this session:")
    print("-------------------------------------")
    if minutes == 0:
        print("This session lasted", seconds, "seconds.")
    else:
        print("This session lasted", minutes, "minutes and", seconds, "seconds.")
    print("")
    data.display_all_data()
    audio_manager.destroy()


def main():
    start = time.time()
    data = FeedbackSystem(threshold)
    start = time.time()
    root = Tk()
    root.title("TuneCoach")
    manager = AudioManager(data)
    manager.start_capture()
    manager.start_reader()
    ourWindow = main_window(root, manager, data)
    root.bind('<space>', lambda event, arg=manager: space_pressed(event, arg))
    root.bind('q', lambda event, arg=manager: kill_pressed(event, arg, data, start))
    root.mainloop()


if __name__ == "__main__":
    main()
