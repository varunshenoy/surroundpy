from Soundstage import Soundstage
from Speakers import HRTFSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

roar = Track("../sounds/roar.wav")
bell = Track("../sounds/bell.wav")

s1 = HRTFSpeaker(np.array([300, 100]), roar)
myStage.add_speaker(s1)

s2 = HRTFSpeaker(np.array([-300, -100]), bell)
myStage.add_speaker(s2)

myStage.plot()
myStage.play()