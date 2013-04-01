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





