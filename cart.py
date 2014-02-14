# Copyright (c) 2009 - 2014 Thomas Preece
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import carteditor

from Tkinter import *
from config import *

RATE = float(SAMPLERATE) + 0.0

def load_images():
	global stopotherimage, submitimage, commandimage
	stopotherimage = PhotoImage(file=STOPOTHER_IMAGE)
	submitimage = PhotoImage(file=SUBMIT_IMAGE)
	commandimage = PhotoImage(file=COMMAND_IMAGE)

stopotherimage = None
submitimage = None
commandimage= None

class NullSound():
	def __init__(self):
		self.length = 5
		self.position = 0
		self._playing = False
		self.is_nullsound = True
	
	def play(self):
		self._playing = True
		self.position = 0
	
	def stop(self):
		self._playing = False
		self.position = 0
	
	def __getattr__(self, attr):
		if attr == 'playing':
			self.position += 1
			if self.position > self.length:
				self._playing = False
			return self._playing

class Cart(Canvas):
	def __init__(self, controller, audio, json):
		self.controller = controller
		self.audio = audio
		self.set_json(json)
		self.setup_display()
		self.bind('<Button-1>', self.onClick)
		self.bind('<Button-3>', self.popup)
		
		self.menu = Menu(self, tearoff=0)
		self.menu.add_command(label='Edit...', command=self.edit)
		self.menu.add_command(label='Clear', command=self.clear)
	
	def set_json(self, json):
		self.json = json
		
		if json is None:
			self.bgcolor = EMPTY_COLOR
			self.fgcolor = EMPTY_COLOR
			self.title = ''
			self.subtitle = ''
			self.stopother = -1
			self.command = ''
			self.submit_play = False
			self.audiofile = ''
			self.sound = NullSound()
		else:
			try:
				self.bgcolor = json['color']
			except KeyError:
				self.bgcolor = BG_COLOR
			try:
				self.fgcolor = json['fgcolor']
			except KeyError:
				self.fgcolor = FG_COLOR
			
			try:
				self.title = json['title']
			except KeyError:
				try:
					self.title = json['line1']
				except KeyError:
					self.title = ''
			try:
				self.subtitle = json['subtitle']
			except KeyError:
				try:
					self.subtitle = json['subtitle']
				except KeyError:
					self.subtitle = ''
			
			try:
				self.stopother = json['stopother']
			except KeyError:
				try:
					self.stopother = json['stops']
				except KeyError:
					self.stopother = -1
			
			try:
				self.command = json['command']
			except KeyError:
				self.command = ''
			
			try:
				self.submit_play = (json['submit_play'] in ('True', 'true')) or (int(json['submit_play'] != 0))
			except KeyError:
				self.submit_play = False
			
			try:
				self.audiofile = json['audiofile']
			except KeyError:
				try:
					self.audiofile = json['aid'] + AUDIOEXT
				except KeyError:
					self.audiofile = ''
			self.loadaudio()	
			
			self.click_enabled = True
	
	def get_json(self):
		json = {}
		json['color'] = self.bgcolor
		json['fgcolor'] = self.fgcolor
		json['title'] = self.title
		json['subtitle'] = self.subtitle
		json['audiofile'] = self.audiofile
		
		return json
	
	def loadaudio(self):
		try:
			self.sound = self.audio.open_file(AUDIODIR + self.audiofile)
		except:
			self.sound = NullSound()
	
	def setup_display(self):
		# create the canvas
		Canvas.__init__(self, width=CART_WIDTH, height=CART_HEIGHT)
		
		# create canvas elements
		self._bgrect = self.create_rectangle(
			1, 1, 
			self.cget("width"), self.cget("height"),
			fill=self.bgcolor
		)
		
		self._stopicon = self.create_rectangle(
			STOP_X1, STOP_Y1,
			STOP_X2, STOP_Y2,
			fill=self.fgcolor,
			state=NORMAL
		)
		
		self._playicon = self.create_polygon(
			PLAY_X1, PLAY_Y1,
			PLAY_X2, PLAY_Y2,
			PLAY_X3, PLAY_Y3,
			fill=self.fgcolor,
			state=HIDDEN
		)
		
		self._stopimage = self.create_image(STOPOTHER_X, STOPOTHER_Y, image=stopotherimage, anchor=SW)
		
		self._submitimage = self.create_image(SUBMIT_X, SUBMIT_Y, image=submitimage, anchor=SW)
		
		self._commandimage = self.create_image(COMMAND_X, COMMAND_Y, image=commandimage, anchor=SW)
		
		self._title = self.create_text(CAP1_X, CAP1_Y, text=self.title, anchor=NW, font=CAP1_FONT, fill=self.fgcolor)
		self._subtitle = self.create_text(CAP2_X, CAP2_Y, text=self.subtitle, anchor=NW, font=CAP2_FONT, fill=self.fgcolor)
		self._timer = self.create_text(TIMER_X, TIMER_Y, text="-X", anchor=SE, font=TIMER_FONT, fill=self.fgcolor)
		
		# EOF flashing
		self.ticks_left = 1
		self.flash_on = True
		
		self.update()
	
	def tick(self):
		self.update()
	
	def update(self):
		position = 0
		color = 0
		
		# show and hide images
		stopstate = (self.stopother == -1) and HIDDEN or NORMAL
		submitstate = (self.submit_play) and NORMAL or HIDDEN
		commandstate = (self.command == '') and HIDDEN or NORMAL
		
		self.itemconfig(self._stopimage, state=stopstate)
		self.itemconfig(self._submitimage, state=submitstate)
		self.itemconfig(self._commandimage, state=commandstate)
		
		nullsound = False
		try:
			nullsound = self.sound.is_nullsound
		except:
			nullsound = False
		
		if nullsound:
			self.itemconfig(self._stopicon, state=HIDDEN)
			self.itemconfig(self._playicon, state=HIDDEN)
			self.itemconfig(self._timer, state=HIDDEN)
			
			if self.sound.playing:
				color = PLAY_COLOR
			else:
				color = self.bgcolor
		else:
			# change elements depending on whether the audio is playing
			if self.sound.playing:
				self.itemconfig(self._stopicon, state=HIDDEN)
				self.itemconfig(self._playicon, state=NORMAL)
				color = PLAY_COLOR
				position = self.sound.position
			else:
				self.itemconfig(self._stopicon, state=NORMAL)
				self.itemconfig(self._playicon, state=HIDDEN)
				color = self.bgcolor
				position = 0
		
			# work out human-readable time remaining
			pos = self.sound.length - position
			time = '-%1.1f' % pos
			if SHOW_MINUTES and pos > 60:
				minutes, seconds = divmod(pos, 60)			
				tenths = (seconds - int(seconds)) * 10
				time = '-%d:%02d.%d' % (minutes, seconds, tenths)
			if time=='--0.0':
				time = '-0.0'
			self.itemconfig(self._timer, state=NORMAL)
			self.itemconfig(self._timer, text=time)
		
			# deal with EOF flashing
			if (pos<=EOF_TIME):
				self.ticks_left -= 1
				if (self.ticks_left == 0):
					self.ticks_left = 4
					self.flash_on = not self.flash_on
				
			if self.sound.playing and not self.flash_on:
				color=EOF_COLOR
		
		# set the correct color
		self.itemconfig(self._bgrect, fill=color)
		
		# set the title and subtitle
		self.itemconfig(self._title, text=self.title)
		self.itemconfig(self._subtitle, text=self.subtitle)
	
	def onClick(self, event):
		if self.sound.playing:
			self.stop()
		else:
			self.play()
	
	def popup(self, event):
		if ALLOW_EDITING:
			self.menu.post(event.x_root, event.y_root)
	
	def play(self):
		if self.stopother != -1:
			self.controller.stop(self.stopother)
		self.sound.play()
		self.flash_on = True
		self.ticks_left = 1
		self.update()
		
		# do these last, as they may take a while
		self.controller.fire_cmd(self.command)
		if self.submit_play:
			self.controller.submit_play(self.audiofile)
	
	def stop(self):
		self.sound.stop()
		self.update()
	
	def edit(self):
		carteditor.CartEditor(self.controller.master, self)
	
	def clear(self):
		self.bgcolor = EMPTY_COLOR
		self.fgcolor = EMPTY_COLOR
		self.title = ''
		self.subtitle = ''
		self.stopother = -1
		self.command = ''
		self.submit_play = False
		self.audiofile = ''
		self.sound = NullSound()
		self.controller.set_modified(True)









