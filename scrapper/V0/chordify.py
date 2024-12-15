import requests
import os

class Chord :
	def __init__(self, chord):
		self.base = "https://tombatossals.github.io/react-chords/media/chords/guitar"
		self.chord = chord
		self.root = chord[0]
		self.enhancement = chord[1:]
		self.link = self.base + "/" + self.root + "/" + self.enhancement + "/xxxx.svg"

	def init_(self):
		self.html = f'<img src = "{self.link}" alt="{self.chord}"/>'

	def format_html(self, n):
		temp = self.html
		temp_ = temp.replace("xxxx",str(n))
		return temp_

a = Chord("Emajor")
a.init_()
print(a.format_html(2))