import tkinter as tk


class RemoveWindow(tk.Toplevel):
    def __init__(self, mainWindow, root, obj):
        print("will create the remove window")