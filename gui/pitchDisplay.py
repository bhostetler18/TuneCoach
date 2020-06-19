from tkinter import *


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

        super().__init__()
        self.frame = Frame(master)
        self.frame.pack()

        self.title = 'Pitch Information'
        self.label = Label(master, text="Hello World")
        self.label.pack()

        # self.otherLabel = Label(self.frame, text="uh") # different from having master passed in
        # self.otherLabel.pack()

        self.display_data()


    def update_pitch(self): # event as parameter
        self._pitchValue = 'G'# hardcoded str(event.char)

    def update_hertz(self):
        self._hertzValue = 0

    def update_cents(self):
        self._centsValue = 0 # perfectly in tune hardcoded - str(event.char)

    def display_data(self): #event
        print("updating data based on realtime changes")
        self.update_cents()
        self.update_hertz()
        self.update_pitch()

if __name__ == "__main__":
    root = Tk()
    root.title("TuneCoach")
    pitch = PitchDisplay(root)
    root.mainloop()