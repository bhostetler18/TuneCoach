# import gui
from gui import *
from pitchDisplay import *
from tkinter import *

def main():
    root = Tk()
    root.title("TuneCoach")
    ourWindow = main_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
