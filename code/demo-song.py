from Soundstage import Soundstage
from Speakers import BasicSpeaker, AmbisonicSpeakers, HRTFSpeaker, Track
import numpy as np

size = np.array([1000, 1000])
myStage = Soundstage(size)

vocals = Track("../sounds/11_LeadVox.wav")
guitar = Track("../sounds/09_AcousticGtr1.wav")
drums = Track("../sounds/03_Overheads.wav")
bass = Track("../sounds/08_Bass.wav")

a = AmbisonicSpeakers(bass, size)

s1 = HRTFSpeaker(np.array([100, 100]), vocals)

s2 = HRTFSpeaker(np.array([-100, 100]), guitar)

s3 = HRTFSpeaker(np.array([0, 200]), drums)
myStage.add_speakers([a, s1, s2, s3])

myStage.plot(title="Ambisonics Example")


myStage.play(save_name="ambisonics.wav")