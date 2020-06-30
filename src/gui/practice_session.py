import datetime


# class to create practice session objects. Will hold all the data for each practice session
class practice_session:
    def __init__(self, name):
        # note history can hold numbers corresponding to the appropriate notes. 1 = C, 2 = C#... I think it would be
        # cool to add in a break point to signify a stop in the practice sesion, like a 13 or something.
        self._noteHistory = []
        # pitches can hold a int value of how off the cents are for the note in noteHistory of the same index.
        self._notePitches = []
        self._scoreList = []
        self._scoreIndex = []
        self._name = name
        self._date = datetime.date.today()
        self._pitch_count = [0,0,0,0,0,0,0,0,0,0,0,0]
        self._pitch_class = [0,0,0,0,0,0,0,0,0,0,0,0]
        self._overall = 0
        self._total_count = 0
        self._cents = 0
        # see about adding raw data
