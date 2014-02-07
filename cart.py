# Copyright (c) 2009 - 2013 Thomas Preece
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

from Tkinter import *
from config import *

RATE = float(SAMPLERATE) + 0.0

class NullSound():
	def __init__(self):
		self.length = 0
		self.position = 0
		self.playing = False

class Cart(Canvas):
	def __init__(self, controller, audio, json):
		self.controller = controller
		self.audio = audio
		self.set_json(json)
		self.setup_display()
		self.bind('<Button-1>', self.onClick)
	
	def set_json(self, json):
		self.json = json
		
		print json
		
		if json is None:
			self.bgcolor = EMPTY_COLOR
			self.fgcolor = EMPTY_COLOR
			self.title = ''
			self.subtitle = ''
			self.audiofile = ''
			self.sound = NullSound()
			self.click_enabled = False
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
				self.audiofile = json['audiofile']
			except KeyError:
				try:
					self.audiofile = json['aid'] + AUDIOEXT
				except KeyError:
					self.audiofile = ''
			print self.audiofile
			if self.audiofile != '':
				try:
					self.sound = self.audio.open_file(AUDIODIR + self.audiofile)
				except:
					self.audiofile = None
			
			self.click_enabled = True
	
	def get_json(self):
		json = {}
		json['color'] = self.bgcolor
		json['fgcolor'] = self.fgcolor
		json['title'] = self.title
		json['subtitle'] = self.subtitle
		json['audiofile'] = self.audiofile
	
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
		
		# change elements depending on whether the audio is playing
		if (self.sound.playing):
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
		if not self.click_enabled: return False
		
		if self.sound.playing:
			self.stop()
		else:
			self.play()
	
	def play(self):
		#if (self.stopother!=-1):
		#	self.controller.stop(self.stopother)
		self.sound.play()
		#self.controller.fire_cmd(self.cmd)
		self.flash_on = True
		self.ticks_left = 1
		self.update()
		#if (self.submit!=0):
		#	submit_play(self.submit)
	
	def stop(self):
		self.sound.stop()
		self.update()









