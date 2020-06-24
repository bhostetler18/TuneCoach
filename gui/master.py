# import gui
from gui import *
from pitchDisplay import *
from tkinter import *


if __name__ == "__main__":
    root = Tk()
    root.title("TuneCoach")
    ourWindow = main_window(root)
    pitch = PitchDisplay(root)

    lib = load_library()
    handle = lib.create_stream(44100)
    audio = AudioThread(handle, lib)
    audio.start()
    root.after(10, pitch.update_data, handle, lib)
    root.mainloop()

# root = tk.Tk()

# root.mainloop()/