import numpy as np
from utils import pad, read, play_audio, get_audio, nround
from pydub.playback import play
import matplotlib.pyplot as plt

class Track():
    """
    The fundamental object representation of a sound file used by speakers.
    """
    def __init__(self, signal, sr=None):
        # passed in filename
        if type(signal) is str:
            self.sr, self.signal = read(signal)

        # passed in signal
        elif type(signal) is np.ndarray:
            self.signal = signal
            assert(sr is not None)
            self.sr = sr

class BasicSpeaker:
    """
    A simple binaural speaker model that emulates distance and angle of a sound source.
    """
    def __init__(self, point, track, is_ambisonic=False, signal=None, sr=0):
        assert(type(track) is Track)

        self.point = point
        self.ear_dist = 10
        self.track = track
 
        self.sr, self.sound = self.localize()

    def rotate(self, theta):
        """
        Rotate a speaker about the origin by theta.
        """

        # rotates point by theta about origin
        theta = np.deg2rad(theta)

        x = self.point[0]
        y = self.point[1]

        x_ = x * np.cos(theta) - y * np.sin(theta)
        y_ = y * np.cos(theta) + x * np.sin(theta)
        
        self.point = np.array([x_, y_])
        self.sr, self.sound = self.localize()

    def localize(self):
        """
        Calculate how much to shift right and left channels
        and overall delay based on speaker location.
        """

        c = 340 # speed of sound in air (m/s)
        ear_dist = self.ear_dist # for exaggeration (more like 0.2)
        l_ear = np.array([-ear_dist, 0.])
        r_ear = np.array([ear_dist, 0.])

        l_dist = np.linalg.norm(self.point - l_ear)
        l_t = l_dist/c

        r_dist = np.linalg.norm(self.point - r_ear)
        r_t = r_dist / c

        sr  = self.track.sr
        x = self.track.signal
        
        # pad l and r
        r_channel = 1 if x.shape[1] > 1 else 0 # support mono audio
        l_pad, left = pad(x[:, 0], l_t)
        r_pad, right = pad(x[:, r_channel], r_t)

        if l_pad > r_pad:
            # pad r in back
            _, right = pad(right, 0, front=False, samples=l_pad - r_pad)
        elif l_pad < r_pad:
            # pad l in back
            _, left = pad(left, 0, front=False, samples=r_pad - l_pad)

        assert (left.shape == right.shape)
        
        sound = np.array([left, right]).T
        return sr, sound

    def delay(self, t):
        """
        Apply a delay to a speaker by t seconds.
        """

        x = self.track.signal
        samples, left = pad(x[:, 0], t)
        samples, right = pad(x[:, 1], t)
        self.sound = np.array([left, right]).T
        return self.sound
        
    def play(self):
        """
        Play the audio for a single speaker
        """
        play_audio(self.sr, self.sound)

    def get_audio(self):
        """
        Fetch the audio signal for a speaker.
        """
        return get_audio(self.sr, self.sound)

    def plot(self, title="Track Signal"):
        """
        Plot the left and right channels of a song.
        """
        sr, sound = self.localize()
        plt.figure(figsize=(16,10))
        plt.plot(sound[:,0], label="Left")
        plt.plot(sound[:,1], label="Right")
        plt.legend()
        plt.title(title)
        plt.show()

class AmbisonicSpeaker():
    """
    Encode/decode signals into/from an ambisonic sound representation for immersive surround sound
    """
    def __init__(self, track, size, theta=60, phi=30, use_HTRF=False):
        self.speakers = []
        self.size = size
        self.theta = theta
        self.phi = phi
        self.use_HTRF = use_HTRF
        self.track = track
        
        self.localize()
        

    def localize(self):
        """
        Construct four speakers to represent the LF, LB, RF, and RB speakers in an ambisonic layout.
        """
        size = self.size/2
        theta = np.deg2rad(self.theta)
        phi = np.deg2rad(self.phi)

        sr  = self.track.sr
        S = self.track.signal

        # Ambisonic encoding        
        W = S * 1/np.sqrt(2)
        X = S * np.cos(theta) * np.cos(phi)
        Y = S * np.sin(theta) * np.cos(phi)
        Z = S * np.sin(phi)

        # Ambisonic decoding
        LF = (2 * W + X + Y) * np.sqrt(8) / 10
        LB = (2 * W - X + Y) * np.sqrt(8) / 10
        RF = (2 * W + X - Y) * np.sqrt(8) / 10
        RB = (2 * W - X - Y) * np.sqrt(8) / 10

        # Speakers can use HRTF or simple accoustics
        if self.use_HTRF:
            LF_speaker = HRTFSpeaker(np.array([-size[0], size[1]]), Track(LF, sr=sr))
            LB_speaker = HRTFSpeaker(np.array([-size[0], -size[1]]), Track(LB, sr=sr)) 
            RF_speaker = HRTFSpeaker(np.array([size[0], size[1]]), Track(RF, sr=sr))
            RB_speaker = HRTFSpeaker(np.array([size[0], -size[1]]), Track(RB, sr=sr))
        else:
            LF_speaker = BasicSpeaker(np.array([-size[0], size[1]]), Track(LF, sr=sr))
            LB_speaker = BasicSpeaker(np.array([-size[0], -size[1]]), Track(LB, sr=sr)) 
            RF_speaker = BasicSpeaker(np.array([size[0], size[1]]), Track(RF, sr=sr))
            RB_speaker = BasicSpeaker(np.array([size[0], -size[1]]), Track(RB, sr=sr))

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
    """
    An improvement on the BasicSpeaker that uses head-related transfer functions (HRTF) for more accurate
    and anatomically better sound localization. 
    """

    def localize(self, elev=0, plot_ir=False):
        """
        An improvement on the BasicSpeaker that uses head-related transfer functions (HRTF) for more accurate
        and anatomically better sound localization. 
        """

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

        # visualize left/right localization via plotting
        if plot_ir:
            plt.figure()
            plt.plot(hrir)
            plt.title(f"HTIR Function at {deg} degrees")
            plt.show()

        # the HRTF is symmetric, so we may need to flip the signal depending on 
        # the sign of the angle
        if sgn < 0:
            hrir = np.flip(hrir, axis=1)
            if plot_ir:
                plt.figure()
                plt.plot(hrir)
                plt.title(f"HTIR Function at {deg} degrees")
                plt.show()
            
        sr = self.track.sr
        x = self.track.signal

        # convert track into mono
        if x.shape[1] > 1:
            x_mono = np.mean(x, axis=1)
        else:
            x_mono = x

        # convolve signal with impulse
        s_L = np.convolve(x_mono, hrir[:,0])
        s_R = np.convolve(x_mono, hrir[:,1])
        
        mix = np.vstack([s_L, s_R]).transpose()
        return sr, mix