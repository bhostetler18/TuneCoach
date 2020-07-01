from TuneCoach.python_bridge.SessionData import load_from_file, save_to_file
from pathlib import Path

def save_session(session):
    if session.path is not None:
        save_to_file(session.data, session.path)
    else:
        raise AttributeError('Cannot save a session without a path')

def load_session(path):
    data = load_from_file(path)
    if data is None:
        return None
    return Session(data, path)

class Session:
    def __init__(self, data, path = None):
        self.data = data
        self.path = path
        if self.path is None:
            self.name = "Temporary Session"
        else:
            self.name = Path(self.path).stem
    
    # rather than edit the path and data directly, just create a new
    # Session object with the new parameters. This is cheap because
    # the data is stored separately
    def with_path(self, path):
        return Session(self.data, path)
