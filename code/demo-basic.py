from Soundstage import Soundstage
from Speakers import BasicSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

bark = Track("../sounds/bark.wav")

s1 = BasicSpeaker(np.array([300, 0]), bark)
myStage.add_speaker(s1)

myStage.plot()
myStage.play()