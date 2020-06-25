# import gui
from gui import *
from pitchDisplay import *
from tkinter import *
from FeedbackSystem import *
from AudioManager import *
sys.path.insert(1, '../python_bridge')


def space_pressed(event, audio_manager):
    if audio_manager.is_paused():
        print("Resuming")
        audio_manager.resume()
    else:
        print("Pausing")
        audio_manager.pause()

def kill_pressed(event, audio_manager, data):
    print("Killing")
    data.display_all_data()
    audio_manager.destroy()


def main():
    threshold = int(input("Enter threshold in cents: "))
    data = FeedbackSystem(threshold)
    root = Tk()
    root.title("TuneCoach")
    manager = AudioManager(data)
    manager.start_capture()
    manager.start_reader()
    ourWindow = main_window(root, manager)
    root.bind('<space>', lambda event, arg=manager: space_pressed(event, arg))
    root.bind('q', lambda event, arg=manager: kill_pressed(event, arg, data))
    root.mainloop()

if __name__ == "__main__":
    main()
