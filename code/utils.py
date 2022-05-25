import pydub 
import numpy as np
from pydub.playback import play

def pad(signal, time, front=True, samples=-1):
    """
    Pad a signal in the front or back to simmulate delays (i.e. signal enters one ear before another)
    """
    if samples == -1:
        samples = int(time * 1000)
    if front:
        return samples, np.pad(signal, (samples, 0), 'constant')
    else:
        return samples, np.pad(signal, (0, samples), 'constant') 

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def play_audio(sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    play(song) 
    # song.export(f, format="mp3", bitrate="320k")

def get_audio(sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    return song

def nround(x, base=5):
    """
    Rounding function to pick optimal discretized HRTF file
    """
    return base * round(x/base)