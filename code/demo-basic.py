from Soundstage import Soundstage
from Speakers import BasicSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

bark = Track("../sounds/bark.wav")

s1 = BasicSpeaker(np.array([300, 0]), bark)
myStage.add_speaker(s1)
s1.plot(title="Dog Barking at (300m, 0m)")

myStage.plot()
myStage.play(save_name="basic_demo.wav")