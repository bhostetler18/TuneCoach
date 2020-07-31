from TuneCoach.python_bridge import SessionData, AudioManager
from TuneCoach.gui.Session import Session, load_session, save_session
from collections import deque



class MainController:
    def __init__(self, view):
        self.view = view

        self.threshold = 15
        self.yellow_threshold = 35
        self.paused = True
        self.should_save = False

        self.queue = deque([])
        self.session = Session(SessionData(self.threshold, self.yellow_threshold), None)
        self.audio_manager = AudioManager(lambda hz: self.queue.append(hz))
    
    def cleanup(self):
        if self.should_save and self.view.ask_should_save() and not self.save():
            return False
    
        self.audio_manager.destroy()
        return True

    def process_queue(self):
        if not self.paused:
            if len(self.queue) != 0:
                top = self.queue.popleft()
                self.session.data.collect_data(top)
                self.update_history()
            self.view.after(20, lambda: self.process_queue())


    def update_diagnostics(self):
        if not self.paused:
            self.view.update_diagnostics(self.session.data)
            self.view.after(500, self.update_diagnostics)

    def update_history(self):
        if self.session.data.has_new_data:
            self.session.data.has_new_data = False # TODO lock
            self.should_save = True
            self.view.update_history(self.session.data)
        # if not self.paused:
        #     self.view.after(20, lambda: self.update_history())

    def update_pitch(self):
        if not self.paused:
            self.view.update_pitch(self.audio_manager.peek(), self.session.data)
        else:
            self.view.update_pitch(0, self.session.data)
        if not self.paused or self.view.pitch_display.needs_update():
            self.view.after(10, self.update_pitch)
    
    def update_tuner_settings(self, cent_threshold, key_signature, from_midi, to_midi):
        self.threshold = cent_threshold
        self.session.data.set_thresholds(cent_threshold, self.yellow_threshold)
        self.session.data.key_signature = key_signature
        self.session.data.midi_range = (from_midi, to_midi)
        self.view.update_threshold(cent_threshold)


    def toggle_pause(self, force=False):
        if self.audio_manager.is_paused() and not force:
            # print("Resuming")
            self.paused = False
            self.view.resume()
            self.audio_manager.resume()
            self.process_queue()
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
            self.flush_queue()

    def flush_queue(self):
        # add remaining data to session
        while len(self.queue) > 0:
            self.session.data.collect_data(self.queue.popleft())

    def setup_session(self):
        
        self.reset_everything()

        if self.audio_manager is not None:
            self.audio_manager.kill()
        
        self.audio_manager = AudioManager(lambda hz: self.queue.append(hz))
        self.view.update_session_name(self.session.name)

        if not self.session.data.empty:
            self.view.update_diagnostics(self.session.data)
            self.view.update_history(self.session.data)
    
    def reset_everything(self):
        self.toggle_pause(True)
        self.view.clear()
        
    
    def save_as(self):
        self.toggle_pause(True)
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
        
        self.toggle_pause(True)
        self._save()
        return True

    def new_session(self):
        if self.should_save:
            self.save()
        data = SessionData(self.threshold, self.yellow_threshold)
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