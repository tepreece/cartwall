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




