import audiere
from config import *

class Audio_Audiere():
	def __init__(self):
		self.audio = audiere.open_device()
	
	def open_file(self, fname):
		return Sound_Audiere(self.audio, fname)

class Sound_Audiere():
	def __init__(self, audio, fname):
		self.audio = audio
		self.audiofile = self.audio.open_file(fname, AUDIO_STREAM_FROM_DISK)
	
	def play(self):
		self.audiofile.play()
	
	def stop(self):
		self.audiofile.stop()
	
	def is_playing(self):
		return self.audiofile.playing
	
	def position(self):
		return self.audiofile.position
	
	def length(self):
		return self.audiofile.length
