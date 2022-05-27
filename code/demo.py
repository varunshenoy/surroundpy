from Soundstage import Soundstage
from Speakers import BasicSpeaker, AmbisonicSpeakers, HRTFSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

flute = Track("../sounds/flute.wav")
bark = Track("../sounds/bark.wav")
metal = Track("../sounds/metallic-beat-short.wav")
roar = Track("../sounds/roar.wav")
geese = Track("../sounds/geese.wav")

a = AmbisonicSpeakers(flute, size)

s1 = BasicSpeaker(np.array([300, 0]), bark)

s2 = BasicSpeaker(np.array([-300, 0]), metal)

s3 = HRTFSpeaker(np.array([200, 100]), roar)

s4 = HRTFSpeaker(np.array([-400, -100]), geese)

myStage.add_speakers([a, s1, s2, s3, s4])

myStage.plot()

myStage.play(save_name="full_demo.wav")