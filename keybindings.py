from plwm import keys

class keyShorcuts(keys.KeyHandler):
	def M4_t(self, event):
		self.wm.system('sakura')
	def M4_space(self, event):
		self.wm.current_screen.change_layout()
	def M4_F1(self, event):
		self.wm.current_screen.change_view(0)
	def M4_F2(self, event):
		self.wm.current_screen.change_view(1)
	def M4_F3(self, event):
		self.wm.current_screen.change_view(2)
	def M4_F4(self, event):
		self.wm.current_screen.change_view(3)
	def M4_F5(self, event):
		self.wm.current_screen.change_view(4)
	def M4_F6(self, event):
		self.wm.current_screen.redraw_wins()
	def M4_x(self, event):
		act = self.wm.system('dmenu_run &')
	def M4_k(self, event):
		if self.wm.current_client:
			self.wm.current_client.destroy()
	def M4_c(self, event):
		self.wm.current_screen.next_window()
	def M4_w(self, event):
		self.wm.current_screen.change_window()
	def F8(self, event):
		self.wm.current_screen.switch_popup()
	def M4_p(self, event):
		if self.wm.current_client:
			self.wm.current_screen.define_popup(self.wm.current_client)
