import tkinter as tk
from array import array
import pickle
import zlib


class SaveWindow(tk.Toplevel):
    def __init__(self, mainWindow, root, obj):
        print("will create the save window")