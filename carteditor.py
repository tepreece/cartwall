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

from Tkinter import *
from config import *

class CartEditor():
	def __init__(self, root, cart):
		self.root = root
		self.cart = cart
		
		self.top = Toplevel()
		self.top.title('Edit Cart')
		
		body = Frame(self.top)
				
		Label(body, text='Title:').grid(in_=body, row=0, column=0, sticky=E)
		self.title = Entry(body)
		self.title.grid(in_=body, row=0, column=1)
		self.title.insert(0, cart.title)
		
		Label(body, text='Subtitle:').grid(in_=body, row=1, column=0, sticky=E)
		self.subtitle = Entry(body)
		self.subtitle.grid(in_=body, row=1, column=1)
		self.subtitle.insert(0, cart.subtitle)
		
		Label(body, text='Audio Directory:').grid(in_=body, row=2, sticky=E)
		Label(body, text=AUDIODIR).grid(in_=body, row=2, column=1, sticky=W)
		
		Label(body, text='Audio File:').grid(in_=body, row=3, sticky=E)
		self.audiofile = Entry(body)
		self.audiofile.grid(in_=body, row=3, column=1)
		self.audiofile.insert(0, cart.audiofile)
		
		Label(body, text='BG Color:').grid(in_=body, row=4, sticky=E)
		self.bgcolor = Entry(body)
		self.bgcolor.grid(in_=body, row=4, column=1)
		self.bgcolor.insert(0, cart.bgcolor)
		
		Label(body, text='FG Color:').grid(in_=body, row=5, sticky=E)
		self.fgcolor = Entry(body)
		self.fgcolor.grid(in_=body, row=5, column=1)
		self.fgcolor.insert(0, cart.fgcolor)
		
		Label(body, text='Stop Cart:').grid(in_=body, row=6, sticky=E)
		self.stopother = Entry(body)
		self.stopother.grid(in_=body, row=6, column=1)
		if cart.stopother >= 0:
			self.stopother.insert(0, str(cart.stopother))
		
		Label(body, text='Command:').grid(in_=body, row=7, sticky=E)
		self.command = Entry(body)
		self.command.grid(in_=body, row=7, column=1)
		self.command.insert(0, cart.command)
		
		self.submit_play = IntVar()
		Checkbutton(body, text="Submit Play", variable=self.submit_play)\
			.grid(in_=body, row=8, column=1, sticky=W)
		self.submit_play.set(cart.submit_play and 1 or 0)
		
		box = Frame(self.top)

		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		
		self.top.bind("<Return>", self.ok)
		self.top.bind("<Escape>", self.cancel)
		
		body.pack(padx=5, pady=5)
		box.pack()
		
		self.top.transient(self.root)
		self.top.grab_set()
		self.root.wait_window(self.top)
	
	def ok(self, event=None):
		self.cart.title = self.title.get()
		self.cart.subtitle = self.subtitle.get()
		self.cart.audiofile = self.audiofile.get()
		self.cart.bgcolor = self.bgcolor.get()
		self.cart.fgcolor = self.fgcolor.get()
		self.cart.command = self.command.get()
		stopother = self.stopother.get()
		self.cart.submit_play = (self.submit_play.get() and True or False)
		
		try:
			intstopother = int(stopother)
		except:
			intstopother = -1
		if intstopother < 0: intstopother = -1
		self.cart.stopother = intstopother
		
		self.cart.loadaudio()
		self.cart.update()
		self.cart.controller.set_modified(True)
		self.top.destroy()
	
	def cancel(self, event=None):
		self.top.destroy()



