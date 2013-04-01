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
from carts import *
from config import *

# 
# LEGACY CONFIG FILE
# 

def load_buttons_legacy(f):
	buttons = []
	
	for i in xrange(5):
		buttons.append((string.strip(f.readline()), LEGACY_BTN_COLOR[i], LEGACY_BTN_HL[i]))
	
	return buttons

def load_carts_legacy(f, controller, carts):
	for x in xrange(5):
		for row in xrange(ROWS):
			for col in xrange(COLS):
				i = row*COLS + col
				carts[x].append(DummyCart())
				carttype = string.strip(f.readline())
				if carttype=='AUDIO':
					aid = string.strip(f.readline())
					bgcol = string.strip(f.readline())
					cap1 = string.strip(f.readline())
					cap2 = string.strip(f.readline())
					stopother = int(string.strip(f.readline()))
					cmd = string.strip(f.readline())
					hotkey = string.strip(f.readline())
					submit = (string.strip(f.readline()))=='true'
					if submit:
						submit_id = aid
					else:
						submit_id = 0

					fname = AUDIODIR+aid+AUDIOEXT
					print fname
					
					carts[x][i] = AudioCart(controller, controller.audio, fname, bgcol, cap1, cap2, stopother, cmd, submit_id)
					controller.hotkeys[hotkey] = (x, i)
				elif carttype=='COMMAND':
					cmd = string.strip(f.readline())
					bgcol = string.strip(f.readline())
					cap1 = string.strip(f.readline())
					cap2 = string.strip(f.readline())
					stopother = int(string.strip(f.readline()))
					hotkey = string.strip(f.readline())

					carts[x][i] = CommandCart(controller, cmd, bgcol, cap1, cap2, stopother)
					controller.hotkeys[hotkey] = (x, i)
				
				carts[x][i].grid(in_=controller.frames[x], row=row, column=col)					

def load_buttons_v02(f):
	buttons = []
	
	for i in xrange(5):
		buttons.append(( \
			string.strip(f.readline()), \
			string.strip(f.readline()), \
			string.strip(f.readline()), \
		))
	
	return buttons


def load_buttons(f, version):
	if version == '0.1':
		return load_buttons_legacy(f)
	elif version == '0.2':
		return load_buttons_v02(f)

def load_carts(f, version, controller, carts):
	if version in ('0.1', '0.2'):
		load_carts_legacy(f, controller, carts)

# 
# JSON CONFIG FILE
# 

def load_json(f):
	return json.load(f)

def load_buttons_json(json):
	buttons = []
	
	for i in xrange(5):
		buttons.append (( \
			json[i]['title'], \
			json[i]['color'], \
			json[i]['highlight'], \
		))
	
	return buttons

def load_carts_json(json, controller, carts):
	for x in xrange(5):
		for row in xrange(ROWS):
			for col in xrange(COLS):
				i = row*COLS + col
				carts[x].append(DummyCart())
				try:
					fname = AUDIODIR+json[x][str(i+1)]['aid']+AUDIOEXT
					if json[x][str(i+1)]['submit'] == "1":
						submit_id = int(json[x][str(i+1)]['aid'])
					else:
						submit_id = 0
					carts[x][i] = AudioCart(self, fname, data[x][str(i+1)]['color'],
						json[x][str(i+1)]['line1'],
						json[x][str(i+1)]['line2'],
						int(json[x][str(i+1)]['stops']),
						0,
						submit_id
					)
				except KeyError, e:
					pass
				
				self.carts[x][i].grid(in_=controller.frames[x], row=row, column=col)





	
