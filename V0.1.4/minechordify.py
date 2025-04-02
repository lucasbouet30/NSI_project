import requests
import os

class Chord :
    def __init__(self, chord):
        self.base = "https://tombatossals.github.io/react-chords/media/guitar/chords"
        self.chord = chord
        self.root = chord[0]
        self.enhancement = chord[1:]
        self.link = self.base + "/" + self.root + "/" + self.enhancement + "/xxxx.svg"
        self.html = f'<img src = "{self.link}" alt="{self.chord}"/>'

    def format_number(self,n):
        temp = self.link
        return temp.replace("xxxx", str(n))

    def format_html(self, n):
        temp = self.html
        temp_ = temp.replace("xxxx",str(n))
        return temp_

# tests
#a = Chord("Emajor")
#a.init_()
#print(a.format_html(2))
