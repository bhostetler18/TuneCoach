import tkinter as tk

class Piano(tk.Canvas):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, kwargs)
		self._parent = parent
		self.configure(bd=0)
		self.configure(bg='black')
		self.configure(highlightthickness=0)
		self.bind("<Configure>", self.draw)

	def draw(self, event):
		print("redraw")
		width = self.winfo_width()
		height = self.winfo_height()
		white_key_height = height/7
		for i in range(0, 8):
			self.create_rectangle(0, white_key_height*i, width, white_key_height*i + white_key_height, fill='white')
