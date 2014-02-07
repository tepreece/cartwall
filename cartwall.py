#!/usr/bin/python

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

import json
import string
import sys
import os
from Tkinter import *
from playstopaudio import playstopaudio

from config import *
import conffile
import cart

BTNCOL = range(5)
BTNHL = range(5)

class Gui:
	def __init__(self, master):
		global BTNCOL, BTNHL
		# save the master
		self.master = master
		
		# set up hotkeys
		self.hotkeys = {}
		
		# open the audio device
		self.audio = playstopaudio.audio(AUDIO_LIBRARIES)
		
		# create the frames
		self.frames = []
		
		self.frames.append(Frame(bg='black', width=500, height=500))
		self.frames.append(Frame(bg='black', width=500, height=500))
		self.frames.append(Frame(bg='black', width=500, height=500))
		self.frames.append(Frame(bg='black', width=500, height=500))
		self.frames.append(Frame(bg='black', width=500, height=500))
		
		# open and process the config file
		self.carts = [[], [], [], [], []]
		f = open(CONFIGFILE, 'r')
		self.json = json.load(f)
		f.close()
		
		# create the carts
		for x in xrange(5):
			for row in xrange(ROWS):
				for col in xrange(COLS):
					i = row*COLS + col
					i_ = str(i+1)
					try:
						j = self.json[x][i_]
					except KeyError:
						j = None
					self.carts[x].append(cart.Cart(self, self.audio, j))
					self.carts[x][i].grid(in_=self.frames[x], row=row, column=col)
					#break
				#break
			#break
		
		# create the buttons
		self.buttons = []
		
		bfont = BTN_FONT
		smallbfont = SMALLBTN_FONT
		
		# we have to define the lambda functions outside of the loop
		# because otherwise the "i" is taken from the loop's scope and will
		# always be set to 4 when the function actually runs
		select_page_lambda = (
			lambda: self.select_page(0),
			lambda: self.select_page(1),
			lambda: self.select_page(2),
			lambda: self.select_page(3),
			lambda: self.select_page(4),
		)
		
		for i in xrange(5):
			try:
				BTNCOL[i] = self.json[i]['color']
			except KeyError:
				BTNCOL[i] = BTN_COLOR
			try:
				BTNHL[i] = self.json[i]['highlight']
			except KeyError:
				BTNHL[i] = BTN_HL
			
			self.buttons.append(Button(
				text=self.json[i]['title'],
				width=1, height=BTN_HEIGHT, borderwidth=BTN_BORDER,
				takefocus=False,
				font=bfont, wraplength=BTN_WRAPLENGTH,
				bg=BTNCOL[i],
				activebackground=BTNCOL[i],
				command=select_page_lambda[i]
			))
		
		self.buttons.append(Button(
			text=REFRESH,
			width=REFRESH_WIDTH, height=SMALLBTN_HEIGHT, borderwidth=SMALLBTN_BORDER,
			takefocus=False,
			font=smallbfont, wraplength=SMALLBTN_WRAPLENGTH,
			bg=SMALLBTN_COLOR,
			activebackground=SMALLBTN_HL,
			command=refresh
		))
		self.buttons.append(Button(
			text=LOGOUT,
			width=LOGOUT_WIDTH, height=SMALLBTN_HEIGHT, borderwidth=SMALLBTN_BORDER,
			takefocus=False,
			font=smallbfont, wraplength=SMALLBTN_WRAPLENGTH,
			bg=SMALLBTN_COLOR,
			activebackground=SMALLBTN_HL,
			command=logout
		))
				
		# put the GUI together
		self.frames[0].grid(row=0, column=0, rowspan=6)
		
		for i in xrange(5):
			self.buttons[i].grid(row=i, column=1, columnspan=2, sticky=N+S+E+W)
		self.buttons[5].grid(row=5, column=1, columnspan=1, sticky=N+S+E+W)
		self.buttons[6].grid(row=5, column=2, columnspan=1, sticky=N+S+E+W)
		self.activeframe = self.frames[0]
		self.activebutton = self.buttons[0]
		self.activeindex = 0
		self.select_page(0)
		
		# start timer
		self.tick()
		
	def select_page(self, idx):
		# remove the old active components
		self.activeframe.grid_forget()
		self.activebutton.configure(relief=RAISED, background=BTNCOL[self.activeindex], activebackground=BTNCOL[self.activeindex])
		
		# set the active components
		self.activeframe = self.frames[idx]
		self.activebutton = self.buttons[idx]
		self.activeindex = idx
		
		# place/update the new active components
		self.activeframe.grid(row=0, column=0, rowspan=6)
		self.activebutton.configure(relief=SUNKEN, background=BTNHL[idx], activebackground=BTNHL[idx])
	
	def tick(self):
		for x in xrange(5):
			for cart in self.carts[x]:
				cart.tick()
		self.master.after(100, self.tick)
	
	def stop(self, item, page=-1):
		# It's usually a fair assumption that the intended page
		# is the currently active page, if it's not specified.
		# In fact, that's all the Cart object can do so far...
		if page==-1:
			page = self.activeindex
		self.carts[page][item].stop()
	
	def fire_cmd(self, cmd):
		try:
			run_command(cmd)
		except NameError:
			pass
	
	def submit_play(self, audiofile):
		try:
			submit_play(audiofile)
		except NameError:
			pass
		

# create the GUI and launch
root = Tk()
exitcode = 0

def refresh():
	global root, exitcode
	print 'refresh'
	exitcode = 1
	root.quit()

def logout():
	global root, exitcode
	print 'logout'
	exitcode = 0
	root.quit()

cart.load_images()
app = Gui(root)
root.title('Cartwall')
root.mainloop()

sys.exit(exitcode)
