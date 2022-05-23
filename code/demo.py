from Soundstage import Soundstage
from Speakers import BasicSpeaker, AmbisonicSpeaker, HRTFSpeaker
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

a = AmbisonicSpeaker("../sounds/flute.wav", size)
myStage.add_speaker(a)

s1 = BasicSpeaker(np.array([300, 0]), "../sounds/bark.wav")
myStage.add_speaker(s1)

s2 = BasicSpeaker(np.array([-300, 0]), "../sounds/metallic-beat-short.wav")
myStage.add_speaker(s2)
myStage.rotate(45)

s3 = HRTFSpeaker(np.array([200, 100]), "../sounds/roar.wav")
myStage.add_speaker(s3)

s4 = HRTFSpeaker(np.array([-400, -100]), "../sounds/geese.wav")
myStage.add_speaker(s4)

myStage.plot()

# myStage.rotate(160)

myStage.play()

# s1.rotate(90)
# myStage.plot()
# myStage.play()

# s1.rotate(90)
# myStage.plot()
# myStage.play()