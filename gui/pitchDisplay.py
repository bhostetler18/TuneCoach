from tkinter import *
# from math import sin, cos, radians

class PitchDisplay:
    def __init__(self, master, pitch=None, hertz=None, cents=None):
        if not pitch:
            self._pitchValue = 'C' # default display ?
        else:
            self._pitchValue = pitch

        if not hertz:
            self._hertzValue = 261.625565 # middle C - hardcodedstr(event.char)
        else:
            self._hertzValue = hertz

        if not cents:
            self._centsValue = 0 # change
        else:
            self._centsValue = cents

        self._default_cents_bound = 100 # 50 cents below and above is allowed
        super().__init__()
        self.frame = Frame(master)
        self.frame.pack()

        self.title = 'Pitch Information'
        self.label = Label(master, text="Hello World")
        self.label.pack()

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        master.geometry(f'{self.screen_width}x{self.screen_height}')

        self.update_data() # call to update pitch / hertz/ cents data all at once

        self.canvas = Canvas(master, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        print(master.winfo_screenheight(), master.winfo_screenwidth())

        self.display_default_gui()

        # self.canvas.create_oval(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=self._pitchValue)

        self.display_current_gui()

    def display_current_gui(self):
        temp = (self._default_cents_bound/2) - self._centsValue
        offset = (temp / self._default_cents_bound) * 90 #90 degrees, 45 offset from start +x
        startValue = offset + 45
        extentValue = 90 - offset

        display = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.itemconfig(display, fill="black",style=PIESLICE, start=startValue, outline='', extent=extentValue)

    def display_default_gui(self):
        pitch_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(pitch_arc, fill="lightgrey", style=PIESLICE, stipple="gray25", start=45, outline='')

        left_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_red_arc, start=120, width=5, fill="#ffbfbf", extent=15, outline='')

        left_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(left_yellow_arc,  start=95, width=5, fill="#fffeb0", extent=25, outline='')

        green_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(green_arc, start=85, width=5, fill="#ccffbf", extent=10, outline='')

        right_yellow_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4,3*self.screen_height/4)
        self.canvas.itemconfig(right_yellow_arc, start=60, width=5, fill="#fffeb0", extent=25, outline='')

        right_red_arc = self.canvas.create_arc(self.screen_width/4, self.screen_height/4, 3*self.screen_width/4, 3*self.screen_height/4)
        self.canvas.itemconfig(right_red_arc, start=45, width=5, fill="#ffbfbf", extent=15, outline='')

    def update_pitch(self): # event as parameter
        self._pitchValue = 'G'# hardcoded str(event.char)

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self):
        self._centsValue = 0 # perfectly in tune hardcoded - str(event.char)

    def update_data(self): #event
        print("updating data based on realtime changes")
        self.update_cents()
        self.update_hertz()
        self.update_pitch()




if __name__ == "__main__":
    root = Tk()
    root.title("TuneCoach")
    pitch = PitchDisplay(root)
    # root.after(0, pitch.update_pitch, pitch, return_increment_value())

    root.mainloop()