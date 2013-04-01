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

class AudioCart(Canvas):
	def __init__(self, controller, audio, fname, bg=BG_COLOR, cap1='CART', cap2='', stopother=-1, cmd="", submit=0):		
		# set up various things
		#audio
		try:
			self.audio = audio.open_file(fname)
		except:
			sys.exit(2)
		
		# control
		self.controller = controller
		self.stopother = stopother
		self.cmd = cmd
		self.submit = submit
		
		# display elements
		self.bgcol = bg
		
		# EOF flashing
		self.ticks_left = 1
		self.flash_on = True
		
		# create the canvas
		Canvas.__init__(self, width=CART_WIDTH, height=CART_HEIGHT)
		
		# create canvas elements
		self.bgrect = self.create_rectangle(
			1, 1, 
			self.cget("width"), self.cget("height"),
			fill=self.bgcol
		)
		
		self.stopicon = self.create_rectangle(
			STOP_X1, STOP_Y1,
			STOP_X2, STOP_Y2,
			fill=FG_COLOR,
			state=NORMAL
		)
		
		self.playicon = self.create_polygon(
			PLAY_X1, PLAY_Y1,
			PLAY_X2, PLAY_Y2,
			PLAY_X3, PLAY_Y3,
			fill=FG_COLOR,
			state=HIDDEN
		)
		
		self.create_text(CAP1_X, CAP1_Y, text=cap1, anchor=NW, font=CAP1_FONT)
		self.create_text(CAP2_X, CAP2_Y, text=cap2, anchor=NW, font=CAP2_FONT)
		self.timer = self.create_text(TIMER_X, TIMER_Y, text="-X", anchor=SE, font=TIMER_FONT)
		
		if (self.stopother!=-1):
			self.create_image(STOPOTHER_X, STOPOTHER_Y, image=stopotherimage, anchor=SW)
		
		if (self.submit):
			self.create_image(SUBMIT_X, SUBMIT_Y, image=submitimage, anchor=SW)
		
		if (self.cmd != ''):
			self.create_image(COMMAND_X, COMMAND_Y, image=commandimage, anchor=SW)
		
		# bind a click event
		self.bind('<Button-1>', self.onClick)

		# make sure the display is up-to-date
		self.update()
	
	def play(self):
		if (self.stopother!=-1):
			self.controller.stop(self.stopother)
		self.audio.play()
		self.controller.fire_cmd(self.cmd)
		self.flash_on = True
		self.ticks_left = 1
		self.update()
		if (self.submit!=0):
			submit_play(self.submit)
	
	def stop(self):
		self.audio.stop()
		self.update()
	
	def tick(self):
		self.update()
	
	def update(self):
		position = 0
		color = 0
		
		# change elements depending on whether the audio is playing
		if (self.audio.is_playing()):
			self.itemconfig(self.stopicon, state=HIDDEN)
			self.itemconfig(self.playicon, state=NORMAL)
			color = PLAY_COLOR
			position = self.audio.position()
		else:
			self.itemconfig(self.stopicon, state=NORMAL)
			self.itemconfig(self.playicon, state=HIDDEN)
			color = self.bgcol
			position = 0
		
		# work out human-readable time remaining
		pos = (self.audio.length() - position) / RATE
		time = '-%1.1f' % pos
		if SHOW_MINUTES and pos > 60:
			minutes, seconds = divmod(pos, 60)			
			tenths = (seconds - int(seconds)) * 10
			time = '-%d:%02d.%d' % (minutes, seconds, tenths)
		if time=='--0.0':
			time = '-0.0'
		self.itemconfig(self.timer, text=time)
		
		# deal with EOF flashing
		if (pos<=EOF_TIME):
			self.ticks_left -= 1
			if (self.ticks_left == 0):
				self.ticks_left = 4
				self.flash_on = not self.flash_on
				
		if (self.audio.is_playing() and not self.flash_on):
			color=EOF_COLOR
		
		# set the correct color
		self.itemconfig(self.bgrect, fill=color)
	
	def onClick(self, event):
		if (self.audio.is_playing()):
			self.stop()
		else:
			self.play()

class CommandCart(Canvas):
	def __init__(self, controller, cmd, bg=BG_COLOR, cap1="", cap2="", stopother=-1):
		self.controller = controller
		self.stopother = stopother
		self.cmd = cmd
		self.ticks_left = 0
		self.bgcol = bg
		
		Canvas.__init__(self, width=CART_WIDTH, height=CART_HEIGHT)
		self.bgcol = bg
		self.bgrect = self.create_rectangle(
			1, 1, 
			self.cget("width"), self.cget("height"),
			fill=self.bgcol)
		
		self.create_text(CAP1_X, CAP1_Y, text=cap1, anchor=NW, font=CAP1_FONT)
		self.create_text(CAP2_X, CAP2_Y, text=cap2, anchor=NW, font=CAP2_FONT)
		
		if (self.stopother!=-1):
			self.create_image(STOPOTHER_X, STOPOTHER_Y, image=stopotherimage, anchor=SW)
		
		if (self.cmd != ''):
			self.create_image(COMMAND_X, COMMAND_Y, image=commandimage, anchor=SW)
		
		# bind a click event
		self.bind('<Button-1>', self.onClick)
	
	def play(self):
		if (self.stopother!=-1):
			self.controller.stop(self.stopother)
		self.controller.fire_cmd(self.cmd)
		self.ticks_left = 10
		self.itemconfig(self.bgrect, fill=PLAY_COLOR)
	
	def stop(self):
		pass
	
	def tick(self):
		if self.ticks_left==0:
			self.itemconfig(self.bgrect, fill=self.bgcol)
		elif self.ticks_left > 0:
			self.ticks_left -= 1
	
	def onClick(self, event):
		if self.ticks_left==0:
			self.play()

class DummyCart(Canvas):
	def __init__(self):
		Canvas.__init__(self, width=CART_WIDTH, height=CART_HEIGHT)
		self.create_rectangle(
			0, 0,
			CART_WIDTH, CART_HEIGHT,
			fill=EMPTY_COLOR,
			state=NORMAL
		)
	
	def play(self):
		pass
	
	def stop(self):
		pass
	
	def tick(self):
		pass

def load_images():
	global stopotherimage, submitimage, commandimage
	stopotherimage = PhotoImage(file=STOPOTHER_IMAGE)
	submitimage = PhotoImage(file=SUBMIT_IMAGE)
	commandimage = PhotoImage(file=COMMAND_IMAGE)

stopotherimage = None
submitimage = None
commandimage= None


