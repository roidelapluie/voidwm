from plwm import wmanager, focus, border, color, wmevents
from tiling import *
from Xlib import X, Xutil, protocol
from os import system
import keybindings

def debug(t):
	print "DEBUG "+t

class uzblClient(wmanager.Client, border.BorderClient):
	def __init__(self, screen, window, maprequest):
		self.firstConf = True
		self.tilesize = None
		self.allow_resize = False
		self.is_icon = False
		self.border_color_name = 'grey5'
		self.border_focuscolor_name = 'dark slate gray'
		wmanager.Client.__init__(self, screen, window, maprequest)
		self.setborderwidth(1)

	def moveresize(self, x, y, width, height, delayed = 0):
		if self.tilesize:
			w,h = self.follow_size_hints(self.tilesize['width'],
				self.tilesize['height'])
			wmanager.Client.moveresize(self, self.tilesize['x'], self.tilesize['y'],
				w, h)
		else:
			wmanager.Client.moveresize(self, x, y, width, height)

	def configure(self, **keys):
		if self.tilesize:
			w,h = self.follow_size_hints(self.tilesize['width'],
				self.tilesize['height'])
			if w > self.tilesize['width']:
				w = self.tilesize['width']
			if h > self.tilesize['height']:
				h = self.tilesize['height']
			wmanager.Client.configure(self, x=self.tilesize['x'],
				y=self.tilesize['y'], width=w, height=h)
		else:
			wmanager.Client.configure(self, **keys)


	def deiconify(self):
		self.is_icon = False
		wmanager.Client.deiconify(self)

	def iconify(self):
		self.is_icon = True
		wmanager.Client.iconify(self)

class voidScreen(wmanager.Screen, color.Color):
	def __init__(self, wm, screenNo):
		self.just_redraw = False
		self.bureau = 0
		self.nbureaux = 5
		self.popup_u = False
		self.popup = None
		self.bureauxe = [4,1,3,0,4]
		self.bureaux = [[], [], [], [], []]
		wmanager.Screen.__init__(self, wm, screenNo)
		
		self.dispatch.add_handler(wmevents.AddClient, self.on_client_added) 
		self.dispatch.add_handler(wmevents.RemoveClient, self.on_client_removed) 

	def on_client_removed(self, event):
		c = event.client
		client_was_on = []
		i = 0
		for bureau in self.bureaux:
			if bureau.count(c) == 1:
				client_was_on.append(i)
				bureau.remove(c)
			i+=1
		if self.popup == c:
			self.popup = None
		if self.bureau in client_was_on:
			self.just_redraw = True
			self.redraw_wins()

	def on_client_added(self, event):
		c = event.client
		c.bureau = getDesk(c.window,c,self)
		if not c.bureau:
			c.bureau = self.bureau
		if c.bureau == -1:
			c.setborderwidth(0)
			c.raisewindow()
		elif c.bureau == 'p':
			self.define_popup(c)
		else:
			self.bureaux[c.bureau].append(c)
			if c.bureau == self.bureau:
				self.just_redraw = True
				self.redraw_wins()

		if c.bureau not in (self.bureau, 'p', -1):
			c.force_iconified = True
			c.iconify()

	def change_window(self):
		if self.wm.current_client:
			 c = self.bureaux[self.bureau].count(self.wm.current_client)
			 if c != 0:
			 	d = self.bureaux[self.bureau].index(self.wm.current_client)+1
				if d == len(self.bureaux[self.bureau]):
					d = 0
					f = self.bureaux[self.bureau][0]
					self.bureaux[self.bureau].remove(f)
					self.bureaux[self.bureau].append(f)
				self.bureaux[self.bureau].remove(self.wm.current_client)
				self.bureaux[self.bureau].insert(d, self.wm.current_client)
				self.redraw_wins()

	def define_popup(self, c):
		if self.popup:
			if c == self.popup:
				return
			try:
				self.bureaux[self.bureau].remove(c)
				c.bureau = 'p'	
			except:
				pass
			try:
				self.bureaux[self.bureau].append(self.popup)
				self.popup.bureau = self.bureau
			except:
				pass
		self.popup = c
		w = [598,50,550,290]
		c.raisewindow()
		c.tilesize={
			'x':w[0], 'y':w[1],
			'width': w[2], 'height':w[3]}
		c.moveresize(w[0],w[1],w[2],w[3], True)
		self.popup_up()
		self.redraw_wins()

	def switch_popup(self):
		if self.popup_u:
			self.popup_down()
		else:
			self.popup_up()

	def popup_down(self):
		if self.popup:
			self.popup_u = False
			self.popup.iconify()
			self.popup.raiselower()

	def popup_up(self):
		if self.popup:
			self.popup_u = True
			self.popup.deiconify()
			self.popup.raisewindow()

	def next_window(self):
		c = self.bureaux[self.bureau].count(self.wm.current_client)
		if c != 0 and self.bureauxe[self.bureau] in (1,2,3):
			d = self.bureaux[self.bureau].index(self.wm.current_client)+1
			try: self.bureaux[self.bureau][d].raisewindow()
			except:  self.bureaux[self.bureau][0].raisewindow()
			if self.popup_u:
				self.popup_up()
			

	def change_view(self, newview):
		for w in self.bureaux[self.bureau]:
			w.force_iconified = True
			w.iconify()
		self.bureau = newview
		self.redraw_wins()
	
	def change_layout(self):
		self.bureauxe[self.bureau] += 1
		if self.bureauxe[self.bureau] > 4:
			self.bureauxe[self.bureau] = 0
		self.redraw_wins()
		


	def redraw_wins(self):
		layout = getLayout(len(self.bureaux[self.bureau]),self.bureauxe[self.bureau])
		if layout:
			c = 0
			for w in layout:
				self.bureaux[self.bureau][c].force_iconified = False
				self.bureaux[self.bureau][c].deiconify()
				self.bureaux[self.bureau][c].tilesize={
					'x':w[0], 'y':w[1],
					'width': w[2], 'height':w[3]}
				self.bureaux[self.bureau][c].moveresize(w[0],w[1],w[2],w[3])
				c+=1
			if self.popup_u:
				self.popup_up()


class WMConf:
	def __wm_init__(self):
		keybindings.keyShorcuts(self)

class voidWm(wmanager.WindowManager, focus.PointToFocus, WMConf):
	client_class = uzblClient
	screen_class = voidScreen
	def __init__(self, disp, appname, db):
		wmanager.WindowManager.__init__(self, disp, appname, db)

if __name__ == '__main__':
	wmanager.main(voidWm)
