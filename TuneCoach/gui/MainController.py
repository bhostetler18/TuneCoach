from TuneCoach.python_bridge import SessionData, AudioManager
from TuneCoach.gui.Session import Session, load_session, save_session

class MainController:
    def __init__(self, view):
        self.view = view

        self.session = Session(SessionData(15), None)
        self.audio_manager = AudioManager(self.session.data)
        self.threshold = 15
        self.yellow_threshold = 35
        self.paused = True
        self.saved = False
    
    def cleanup(self):
        if not self.saved and self.view.ask_should_save() and not self.save():
            return False
    
        self.audio_manager.destroy()
        return True

    def update_diagnostics(self):
        if not self.paused:
            self.view.update_diagnostics(self.session.data)
        if not self.paused:
            self.view.after(500, self.update_diagnostics)

    def update_history(self):
        if self.session.data.has_new_data:
            self.session.data.has_new_data = False # TODO lock
            self.saved = False
            self.view.update_history(self.session.data)
        if not self.paused:
            self.view.after(20, lambda: self.update_history())

    def update_pitch(self):
        self.view.update_pitch(self.audio_manager.peek())
        if not self.paused:
            self.view.after(10, self.update_pitch)
        
    def toggle_pause(self):
        if self.audio_manager.is_paused():
            # print("Resuming")
            self.paused = False
            self.view.resume()
            self.audio_manager.resume()
            self.update_history()
            self.update_diagnostics()
            self.update_pitch()
            self.session.data.timer.resume()
        else:
            # print("Pausing")
            self.paused = True
            self.saved = False # when we pause, we're ready to save new data
            
            self.view.pause()
            self.audio_manager.pause()
            self.session.data.timer.pause()


    def force_pause(self):
        if not self.paused and not self.audio_manager.is_paused():
            # print("Pausing")
            self.paused = True
            self.view.pause()
            self.audio_manager.pause()
            self.session.data.timer.pause()

    def setup_session(self):
        
        self.reset_everything()

        if self.audio_manager is not None:
            self.audio_manager.kill()
        
        self.audio_manager = AudioManager(self.session.data)
        self.view.update_session_name(self.session.name)

        if not self.session.data.empty:
            self.update_diagnostics()
            self.update_history()
    
    def reset_everything(self):
        self.force_pause()
        self.view.clear()
        
    
    def save_as(self):
        self.force_pause()
        path, cancel = self.view.perform_save_as()
        if cancel:
            return False

        self.session = self.session.with_path(path)
        # notify session name change
        self.view.update_session_name(self.session.name)
        self._save()
        return True # we did save

    def _save(self):
        save_session(self.session)
        self.view.success(f'Session saved to "{self.session.path}" successfully', title="Session Saved")
        self.saved = True

    def save(self):
        if self.saved:
            return True
        
        if self.session.path is None:
            return self.save_as()
        
        self.force_pause()
        self._save()
        return True

    def new_session(self):
        if not self.saved:
            self.save()
        data = SessionData(self.threshold)
        self.session = Session(data)
        self.setup_session()

    def load_from(self):
        # if current sesion isn't saved, ask if we should save. If we should
        # try to save. If the user cancels, don't bother to save
        if not self.saved and self.view.ask_should_save():
            self.save()

        path, cancel = self.view.perform_load()
        if cancel:
            return False
        
        session = load_session(path)


        if session is None:
            self.view.error(f'Session located at "{path}" is invalid!', title="Invalid session")
        else:
            self.session = session
            self.setup_session()
            self.saved = True