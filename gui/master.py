# import gui
from gui import *
from pitchDisplay import *
from tkinter import *
sys.path.insert(1, '../python_bridge')
from AudioManager import *

def space_pressed(event, audio_manager):
	if audio_manager.is_paused():
		print("Resuming")
		audio_manager.resume()
	else:
		print("Pausing")
		audio_manager.pause()
	

def main():
    root = Tk()
    root.title("TuneCoach")
    manager = AudioManager()
    manager.start_capture()
    ourWindow = main_window(root, manager)
    root.bind('<space>', lambda event, arg=manager: space_pressed(event, arg))
    root.mainloop()

if __name__ == "__main__":
    main()
