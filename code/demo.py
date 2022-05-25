from Soundstage import Soundstage
from Speakers import BasicSpeaker, AmbisonicSpeaker, HRTFSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

flute = Track("../sounds/flute.wav")
bark = Track("../sounds/bark.wav")
metal = Track("../sounds/metallic-beat-short.wav")
roar = Track("../sounds/roar.wav")
geese = Track("../sounds/geese.wav")

a = AmbisonicSpeaker(flute, size)
myStage.add_speaker(a)

s1 = BasicSpeaker(np.array([300, 0]), bark)
myStage.add_speaker(s1)

s2 = BasicSpeaker(np.array([-300, 0]), metal)
myStage.add_speaker(s2)
myStage.rotate(45)

s3 = HRTFSpeaker(np.array([200, 100]), roar)
myStage.add_speaker(s3)

s4 = HRTFSpeaker(np.array([-400, -100]), geese)
myStage.add_speaker(s4)

myStage.plot()

myStage.rotate(160)

myStage.play()