import sys
from config import *

AUDIERE = 1
GSTREAMER = 2

chosen_library = 0

has_audiere = False
has_gstreamer = False

try:
	import audio_audiere
	has_audiere = True
except:
	pass

try:
	import audio_gstreamer
	has_gstreamer = True
except:
	pass

if PREFER_GSTREAMER and has_gstreamer:
	print 'Using GStreamer...'
	chosen_library = GSTREAMER
elif has_audiere:
	print 'Using Audiere...'
	chosen_library = AUDIERE
else:
	print 'No audio libraries available!'
	sys.exit(1)

class Audio():
	def __init__(self):
		if chosen_library == GSTREAMER:
			self.audio = audio_gstreamer.Audio_GStreamer()
		elif chosen_library == AUDIERE:
			self.audio = audio_audiere.Audio_Audiere()
		else:
			pass
	
	def open_file(self, fname):
		return self.audio.open_file(fname)





