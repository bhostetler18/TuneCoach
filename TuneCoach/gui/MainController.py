from TuneCoach.python_bridge import SessionData, AudioManager
from TuneCoach.gui.Session import Session, load_session, save_session

class MainController:
    def __init__(self, view):
        self.view = view
        self.threshold = None
        self.session = Session(SessionData(15), None)
        self.audio_manager = AudioManager(self.session.data)
        self.threshold = 15
        self.yellow_threshold = 35
        self.paused = True
        self.should_save = False
    
    def cleanup(self):
        if self.should_save and self.view.ask_should_save() and not self.save():
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
            self.should_save = True
            self.view.update_history(self.session.data)
        if not self.paused:
            self.view.after(20, lambda: self.update_history())

    def update_pitch(self):
        print(self.view.pitch_display.needs_update())
        self.view.update_pitch(self.audio_manager.peek(), self.session.data)
        print(self.view.pitch_display.needs_update())
        if not self.paused or self.view.pitch_display.needs_update():
            self.view.after(10, self.update_pitch)
    
    def update_tuner_settings(self, cent_threshold, key_signature, f_note, f_oct, t_note, t_oct):
        self.session.data.threshold = cent_threshold
        self.session.data.key_signature = key_signature
        self.session.data.from_note = f_note
        self.session.data.from_octave = f_oct
        self.session.data.to_note = t_note
        self.session.data.to_octave = t_oct
        self.view.update_threshold(cent_threshold)


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
            self.should_save = True # when we pause, we're ready to save new data
            
            self.view.pause()
            self.audio_manager.pause()
            self.session.data.timer.pause()


    def force_pause(self):
        if not self.paused and not self.audio_manager.is_paused():
            # print("Pausing")
            self.should_save = True
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
            self.view.update_diagnostics(self.session.data)
            self.view.update_history(self.session.data)
    
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
        self.should_save = False

    def save(self):
        if not self.should_save:
            return True
        
        if self.session.path is None:
            return self.save_as()
        
        self.force_pause()
        self._save()
        return True

    def new_session(self):
        if self.should_save:
            self.save()
        data = SessionData(self.threshold)
        self.session = Session(data)
        self.setup_session()

    def load_from(self):
        # if current sesion isn't saved, ask if we should save. If we should
        # try to save. If the user cancels, don't bother to save
        if self.should_save and self.view.ask_should_save():
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
            self.should_save = False