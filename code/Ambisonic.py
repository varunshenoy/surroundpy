import numpy as np
from utils import pad, read, play_audio

class AmbisonicSpeaker():
    def __init__(self, fn):
        self.fn = fn

    def calculate_sound(self, theta, phi, size):
        theta = np.deg2rad(theta)
        phi = np.deg2rad(phi)

        self.point = np.array([0, 0, 0])
        sr, S = read(self.fn)
        
        W = S * 1/np.sqrt(2)
        X = S * np.cos(theta) * np.cos(phi)
        Y = S * np.sin(theta) * np.cos(phi)
        Z = S * np.sin(phi)

        LF = (2 * W + X + Y) * np.sqrt(8)
        LB = (2 * W - X + Y) * np.sqrt(8)
        RF = (2 * W + X - Y) * np.sqrt(8)
        RB = (2 * W - X - Y) * np.sqrt(8)

        LF_speaker = BasicSpeaker(-size[0], size[1], None, is_ambisonic=True, signal=LF, sr=sr)
        LB_speaker = BasicSpeaker(-size[0], -size[1], None, is_ambisonic=True, signal=LB, sr=sr) 
        RF_speaker = BasicSpeaker(size[0], size[1], None, is_ambisonic=True, signal=RF, sr=sr)
        RB_speaker = BasicSpeaker(size[0], -size[1], None, is_ambisonic=True, signal=RB, sr=sr)

        return LF_speaker, LB_speaker, RF_speaker, RB_speaker