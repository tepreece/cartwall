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

import string
import sys
import os
from Tkinter import *
from playstopaudio import playstopaudio

from config import *
import conffile
from carts import *

APPNAME = '~~CARTWALL~~'

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
		
		if CONFIG_LEGACY:
			# find out which version of the config file we're using
			versionline = string.strip(f.readline())
			(appname, version) = string.split(versionline, None, 1)
			
			if appname != APPNAME:
				# legacy config file
				f.seek(0, 0) # go back to the beginning of the file
				print 'WARNING: using legacy config. Please update your config file.'
				btnconf = conffile.load_buttons_legacy(f)
				conffile.load_carts_legacy(f, self, self.carts)
			else:
				# config file with version number
				btnconf = conffile.load_buttons(f, version)
				conffile.load_carts(f, version, self, self.carts)
		else:
			json = conffile.load_json(f)
			btnconf = conffile.load_buttons_json(json)
			conffile.load_carts_json(json, self. self.carts)
		
		f.close()
		
		# create the buttons
		self.buttons = []	
		
		bfont = BTN_FONT
		smallbfont = SMALLBTN_FONT
		
		BTNCOL = [x[1] for x in btnconf]
		BTNHL = [x[2] for x in btnconf]
		
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
			self.buttons.append(Button(
				text=btnconf[i][0],
				width=1, height=BTN_HEIGHT, borderwidth=BTN_BORDER,
				takefocus=False,
				font=bfont, wraplength=BTN_WRAPLENGTH,
				bg=btnconf[i][1],
				activebackground=btnconf[i][1],
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

		# bind key press
		root.bind('<KeyPress>', self.keyPress)
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
		# it's usually a fair assumption that the intended page
		# is the currently active page, if it's not specified
		if page==-1:
			page = self.activeindex
		self.carts[page][item].stop()
	
	def fire_cmd(self, cmd):
		run_command(cmd)

	def keyPress(self, event):
		try:
			c = str(int(event.char))
			item = self.hotkeys[c]
			page = item[0]
			cart = item[1]
			self.carts[page][cart].onClick(event)
		except:
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

load_images()
app = Gui(root)
root.title('Cartwall')
root.mainloop()

sys.exit(exitcode)
