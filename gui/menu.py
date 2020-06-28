from tkinter import *

class MenuBar:
    def __init__(self, master, title = None):
        if not title:
            self.title = "Menu Bar"
        else:
            self.title = title

        menuBar = Menu(master)
        master.config(menu=menuBar)

        file_submenu = Menu(self)
        self.add_cascade(label="File", menu=file_submenu)
        file_submenu.add_command(label="New Practice Session", command=self.create_new_practice_session)
        file_submenu.add_separator
        file_submenu.add_command(label="End Practice Session", command=self.end_practice_session)
        file_submenu.add_separator
        file_submenu.add_command(label="Load Practice Session", command=self.load_practice_session)
        file_submenu.add_separator
        file_submenu.add_command(label="Exit", command=master.quit)

        settings_submenu = Menu(self)
        self.add_cascade(label="Settings", menu=settings_submenu)
        settings_submenu.add_command(label="Tuner Settings", command=self.change_tuner_settings)
        settings_submenu.add_separator
        settings_submenu.add_command(label="User Settings", command=self.change_user_settings)
        settings_submenu.add_separator

        view_submenu = Menu(self)
        self.add_cascade(label="View", menu=view_submenu)
        view_submenu.add_command(label="Change layout", command=self.change_layout)
        view_submenu.add_separator

        help_submenu = Menu(self)
        self.add_cascde(label="help", menu=help_submenu)
        help_submenu.add_command(label="FAQ", command=self.load_faq)
        help_submenu.add_separator
        help_submenu.add_command(label="Tutorial", command=self.load_tutorial)
        help_submenu.add_separator

    # menu option functions
    def create_new_practice_session(self):
        print("command to start a new practice session")

    def end_practice_session(self):
        print("command to end practice session")

    def load_practice_session(self):
        print("command to load practice session")

    def change_layout(self):
        print("this will change the layout")

    def change_tuner_settings(self):
        print("function to display tuner settings menu")

    def change_user_settings(self):
        print("function to display menu to change user settings")

    def change_layout(self):
        print("function to display menu to change the window layout")

    def load_faq(self):
        print("function to load app faq")

    def load_tutorial(self):
        print("function to load a tutorial for how to use the app")