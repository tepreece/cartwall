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

import pygst
import gst
from config import *

class Audio_GStreamer():
	def __init__(self):
		pass
	
	def open_file(self, fname):
		return Sound_GStreamer(fname)

class Sound_GStreamer():
	def __init__(self, fname):
		self.player = gst.element_factory_make("playbin2", fname)
		self.player.set_property("uri", "file://" + fname)
		self.player.set_state(gst.STATE_PAUSED)
		
		if gst.STATE_PAUSED in self.player.get_state(): 
			self.length = self.player.query_duration(gst.FORMAT_TIME, None)[0] / float(1000000000)
		self.player.set_state(gst.STATE_NULL)
	
	def play(self):
		self.player.set_state(gst.STATE_PLAYING)
	
	def stop(self):
		self.player.set_state(gst.STATE_NULL)
	
	def is_playing(self):
		try:
			if (self.player.query_position(gst.FORMAT_TIME, None)[0] < self.player.query_duration(gst.FORMAT_TIME, None)[0]):
				return True
			else:
				return False
		except gst.QueryError:
			return False
	
	def position(self):
		try:
			position = self.player.query_position(gst.FORMAT_TIME, None)[0] / float(1000000000)
		except gst.QueryError:
			position = 0
		return position
	
	def length(self):
		try:
			duration = self.player.query_duration(gst.FORMAT_TIME, None)[0] / float(1000000000)
		except gst.QueryError:
			duration = self.length
		return duration




