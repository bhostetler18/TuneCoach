#main gui for our project, tuneCoach. Made by the group , Jamm , James , Joe Gravelle, Jenny Baik, Gavin Gui

from tkinter import *

def main():
    
    #some important variables

    background_color = "#575759"
    
    #menu option functions, will work on flushing out

    def new_practice_session():
        print("command to start a new practice session")

    def end_practice_session():
        print("command to end practice sesion")

    def load_practice_session():
        print("command to load practice session")   

    def change_layout():
        print("this will change the layout")

    def tuner_settings():
        print("function to display tuner settings menu")

    def user_settings():
        print("function to display menu to change user settings")

    def change_layout():
        print("function to display menu to change the window layout")

    def load_faq():
        print("function to load app faq")

    def load_tutorial():
        print("funciton to load a tutorial for how to use the app")
    

    #initializing the main tkinter window. It will span the whole screen for now.
   
    root = Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.title("TuneCoach")
    root.geometry(f'{screen_width}x{screen_height}')
    
    #adding menu options to the top of the screen.

    menubar = Menu(root)

    root.config(menu=menubar)

    file_menu = Menu(menubar)

    #file menubar
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Practice Session", command = new_practice_session)
    file_menu.add_separator
    file_menu.add_command(label="End Practice Session", command = end_practice_session)
    file_menu.add_separator
    file_menu.add_command(label="Load Practice Session", command = load_practice_session)
    file_menu.add_separator
    file_menu.add_command(label="Exit", command = root.quit)
    
    #settings menubar
    settings_menu = Menu(menubar)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Tuner Settings", command = tuner_settings)
    settings_menu.add_separator
    settings_menu.add_command(label="User Settings", command = user_settings)
    settings_menu.add_separator

    #view menubar
    view_menu = Menu(menubar)
    menubar.add_cascade(label="View", menu = view_menu)
    view_menu.add_command(label="Change layout", command = change_layout)
    view_menu.add_separator

    #help menubar
    help_menu = Menu(menubar)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="FAQ", command = load_faq)
    help_menu.add_separator
    help_menu.add_command(label="Tutorial", command = load_tutorial)
    help_menu.add_separator

   #creating frames to organize the screen.
    
    bottomFrame = Frame(root, bd = 5, relief = RAISED, bg = background_color)
    leftFrame = Frame(root, bd = 5, relief = RAISED ,bg =  background_color)
    rightFrame = Frame(root, bd = 5, relief = RAISED, bg = background_color)

    #putting the frames into a grid layout

    bottomFrame.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew")
    leftFrame.grid(row = 0, column = 0, sticky = "nsew")
    rightFrame.grid(row = 0, column = 1, sticky = "nsew")

    #setting up grid weights.

    root.grid_rowconfigure(0, weight=5)
    root.grid_rowconfigure(1, weight=4)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    #i think that here we can work on creating the funcitonality for each individual frame, ex: tuner, pitch history, information.

    #adding the temporary label to the session history section.
    session_diagnostics = Label(bottomFrame, text = "Session History", font=("Calibri", 20))
    session_diagnostics.config(bg = background_color, fg = "white")
    session_diagnostics.pack()
    
    #adding the temporary label to the session Session Diagnostics section.
    info_header = Label(leftFrame, text = "Session Diagnostics", font=("Calibri", 20))
    info_header.config(bg = background_color, fg = "white")
    info_header.pack()

    #adding temporary label to the Pitch Detector Section
    tuner_header = Label(rightFrame, text = "Pitch Detector", font=("Calibri", 20))
    tuner_header.config(bg = background_color, fg = "white")
    tuner_header.pack()


    # display the main window

    root.mainloop()

main()