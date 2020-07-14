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
		self.delete("all")
		width = self.winfo_width()
		height = self.winfo_height()
		key_gap = 1
		white_key_height = height/7
		black_key_height = height/14
		black_key_width = width*0.6
		for i in range(0, 8):
			self.create_rectangle(0, (white_key_height)*i + key_gap/2, width, (white_key_height)*(i+1) - key_gap/2, fill='white')
			if i not in {0,4,7}:
				self.create_rectangle(0, (white_key_height)*(i) - black_key_height/2, black_key_width, white_key_height*(i)+black_key_height/2, fill='black')
			
		