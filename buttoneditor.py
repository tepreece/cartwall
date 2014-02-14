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

class ButtonEditor():
	def __init__(self, root, button):
		self.root = root
		self.button = button
		
		self.top = Toplevel()
		self.top.title('Edit Page')
		
		body = Frame(self.top)
		
		Label(body, text='Title:').grid(in_=body, row=0, column=0, sticky=E)
		self.title = Entry(body)
		self.title.grid(in_=body, row=0, column=1)
		self.title.insert(0, button.title)
		
		Label(body, text='Color:').grid(in_=body, row=4, sticky=E)
		self.color = Entry(body)
		self.color.grid(in_=body, row=4, column=1)
		self.color.insert(0, button.color)
		
		Label(body, text='Highlight:').grid(in_=body, row=5, sticky=E)
		self.highlight = Entry(body)
		self.highlight.grid(in_=body, row=5, column=1)
		self.highlight.insert(0, button.highlight)
		
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
		self.button.controller.set_modified(True)
		self.button.title = self.title.get()
		self.button.color = self.color.get()
		self.button.highlight = self.highlight.get()
		
		if self.button.active:
			col = self.button.highlight
		else:
			col = self.button.color
		
		self.button.config(text=self.button.title, bg=col, activebackground=col)
		
		self.top.destroy()
	
	def cancel(self, event=None):
		self.top.destroy()
		
		
		
		
