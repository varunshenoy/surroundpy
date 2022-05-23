import numpy as np
from utils import pad, read, play_audio, get_audio, nround
from pydub.playback import play
import matplotlib.pyplot as plt

class BasicSpeaker:
    def __init__(self, point, fn, is_ambisonic=False, signal=None, sr=0):
        self.point = point
        self.ear_dist = 10
        self.signal=None
        self.is_ambisonic = is_ambisonic
        if is_ambisonic:
            self.sound=signal
            self.signal= signal
            self.sr = sr
            return
        
        self.fn = fn
        self.sr, self.sound = self.calculate_sound()

    def rotate(self, theta):
        # rotates point by theta about origin
        theta = np.deg2rad(theta)

        x = self.point[0]
        y = self.point[1]

        x_ = x * np.cos(theta) - y * np.sin(theta)
        y_ = y * np.cos(theta) + x * np.sin(theta)
        
        self.point = np.array([x_, y_])
        self.sr, self.sound = self.calculate_sound()

    def calculate_sound(self):
        c = 340 # speed of sound in air (m/s)
        ear_dist = self.ear_dist # for exaggeration (more like 0.2)
        l_ear = np.array([-ear_dist, 0.])
        r_ear = np.array([ear_dist, 0.])

        l_dist = np.linalg.norm(self.point - l_ear)
        l_t = l_dist/c

        r_dist = np.linalg.norm(self.point - r_ear)
        r_t = r_dist / c

        if not self.is_ambisonic:
            sr, x = read(self.fn)
        else:
            sr = self.sr
            x = self.signal
        
        # pad l and r
        # TODO: Support single channel audio
        l_pad, left = pad(x[:, 0], l_t)
        r_pad, right = pad(x[:, 1], r_t)

        if l_pad > r_pad:
            # pad r in back
            _, right = pad(right, 0, front=False, samples=l_pad - r_pad)
        elif l_pad < r_pad:
            # pad l in back
            _, left = pad(left, 0, front=False, samples=r_pad - l_pad)

        assert (left.shape == right.shape)
        
        sound = np.array([left, right]).T
        return sr, sound
        
    def play(self):
        play_audio(self.sr, self.sound)

    def get_audio(self):
        return get_audio(self.sr, self.sound)

    def plot(self):
        sr, sound = self.calculate_sound()
        plt.figure(figsize=(16,10))
        plt.plot(sound)
        plt.title("Sample MP3 loading into Numpy")
        plt.show()

class AmbisonicSpeaker():
    def __init__(self, fn, size, theta=60, phi=30, use_HTRF=False):
        self.fn = fn
        self.speakers = []
        self.size = size
        self.theta = theta
        self.phi = phi
        self.use_HTRF = use_HTRF

        self.calculate_sound()
        

    def calculate_sound(self):
        size = self.size/2
        theta = np.deg2rad(self.theta)
        phi = np.deg2rad(self.phi)

        self.point = np.array([0, 0, 0])
        sr, S = read(self.fn)
        
        W = S * 1/np.sqrt(2)
        X = S * np.cos(theta) * np.cos(phi)
        Y = S * np.sin(theta) * np.cos(phi)
        Z = S * np.sin(phi)

        LF = (2 * W + X + Y) * np.sqrt(8) / 10
        LB = (2 * W - X + Y) * np.sqrt(8) / 10
        RF = (2 * W + X - Y) * np.sqrt(8) / 10
        RB = (2 * W - X - Y) * np.sqrt(8) / 10

        if self.use_HTRF:
            LF_speaker = HRTFSpeaker(np.array([-size[0], size[1]]), None, is_ambisonic=True, signal=LF, sr=sr)
            LB_speaker = HRTFSpeaker(np.array([-size[0], -size[1]]), None, is_ambisonic=True, signal=LB, sr=sr) 
            RF_speaker = HRTFSpeaker(np.array([size[0], size[1]]), None, is_ambisonic=True, signal=RF, sr=sr)
            RB_speaker = HRTFSpeaker(np.array([size[0], -size[1]]), None, is_ambisonic=True, signal=RB, sr=sr)
        else:
            LF_speaker = BasicSpeaker(np.array([-size[0], size[1]]), None, is_ambisonic=True, signal=LF, sr=sr)
            LB_speaker = BasicSpeaker(np.array([-size[0], -size[1]]), None, is_ambisonic=True, signal=LB, sr=sr) 
            RF_speaker = BasicSpeaker(np.array([size[0], size[1]]), None, is_ambisonic=True, signal=RF, sr=sr)
            RB_speaker = BasicSpeaker(np.array([size[0], -size[1]]), None, is_ambisonic=True, signal=RB, sr=sr)

        self.speakers = [LF_speaker, LB_speaker, RF_speaker, RB_speaker]

        return LF_speaker, LB_speaker, RF_speaker, RB_speaker

    def get_audio(self):
        mixed = self.speakers[0].get_audio()
        for s in self.speakers[1:]:
            mixed = mixed.overlay(s.get_audio())
        return mixed


    def rotate(self, theta):
        for s in self.speakers:
            s.rotate(theta)


class HRTFSpeaker(BasicSpeaker):
    def calculate_sound(self, elev=0, plot_ir=False):

        # calculate angle
        x = self.point[0]
        y = self.point[1]

        deg = nround(np.rad2deg(np.arctan2(x, y)))
        sgn = deg/abs(deg)
        deg = abs(deg)

        # pick correct file
        fname = f"../hrtf/elev{nround(elev, base=10)}/H0e{str(deg).zfill(3)}a.wav"

        sr, hrir = read(fname)
        hrir = np.divide(hrir, hrir.max() * 5, casting="unsafe")

        if plot_ir:
            plt.figure()
            plt.plot(hrir)
            plt.title(f"HTIR Function at {deg} degrees")
            plt.show()
            # play_audio(sr, hrir)

        if sgn < 0:
            hrir = np.flip(hrir, axis=1)
            if plot_ir:
                plt.figure()
                plt.plot(hrir)
                plt.title(f"HTIR Function at {deg} degrees")
                plt.show()
            # play_audio(sr, hrir)
            

        # convolve signal with impulse
        if not self.is_ambisonic:
            sr, x = read(self.fn)
        else:
            sr = self.sr
            x = self.signal

        if x.shape[1] > 1:
            x_mono = np.mean(x, axis=1)
        else:
            x_mono = x

        # play_audio(sr, x_mono)

        s_L = np.convolve(x_mono, hrir[:,0])
        s_R = np.convolve(x_mono, hrir[:,1])
        
        mix = np.vstack([s_L, s_R]).transpose()
        return sr, mix