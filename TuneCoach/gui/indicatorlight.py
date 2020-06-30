import tkinter as tk


class IndicatorLight(tk.Canvas):
	def __init__(self, parent, size=20):
		super().__init__(parent, width=size, height=size)
		self._parent = parent
		self.light = self.create_oval(0.15*size, 0.15*size, 0.85*size, 0.85*size, fill='red', width=0, state=tk.HIDDEN)
		self._isOn = False
		self._flashing = False
		self._job = None

		self.pausedCircle = self.create_oval(0, 0, size, size, fill='#72d2e0', width=0)
		self.line1 = self.create_line(0.35*size, 0.35*size, 0.35*size, 0.65*size, width=size/4.5, capstyle=tk.ROUND)
		self.line2 = self.create_line(0.65*size, 0.65*size, 0.65*size, 0.35*size, width=size/4.5, capstyle=tk.ROUND)

	def start_flashing(self):
		if not self._flashing:
			self._flashing = True
			self.itemconfig(self.pausedCircle, state=tk.HIDDEN)
			self.itemconfig(self.line1, state=tk.HIDDEN)
			self.itemconfig(self.line2, state=tk.HIDDEN)
			self._flash()

	def _flash(self):
		if self._flashing:
			state = tk.HIDDEN if self._isOn else tk.NORMAL
			self.itemconfig(self.light, state=state)
			self._isOn = not self._isOn
			self._job = self._parent.after(800, self._flash)

	def stop(self):
		if self._job is not None:
			self._parent.after_cancel(self._job)
		self._flashing = False
		self.itemconfig(self.light, state=tk.HIDDEN)
		self.itemconfig(self.pausedCircle, state=tk.NORMAL)
		self.itemconfig(self.line1, state=tk.NORMAL)
		self.itemconfig(self.line2, state=tk.NORMAL)
		self._isOn = False
