import numpy as np
import simpleaudio as sa
from scipy.io.wavfile import write

def save_wav(file_name, audio, fs = 44100):
    song = audio.array
    write(file_name, fs, song)

#duration in seconds
def sine_wave(freq, duration, fs = 44100):
    t = np.linspace(0, duration, int(duration*fs), False)
    return np.sin(freq * t * 2 * np.pi)

def square_wave(freq, duration, fs = 44100):
    return np.sign(sine_wave(freq, duration, fs))

def saw_wave(freq, duration, fs = 44100):
    w1 = sine_wave(freq, duration, fs)
    w2 = -sine_wave(freq*2, duration, fs)/2
    w3 = sine_wave(freq*3, duration, fs)/3
    w4 = -sine_wave(freq*4, duration, fs)/4
    w5 = sine_wave(freq*4, duration, fs)/5
    w6 = -sine_wave(freq*4, duration, fs)/6
    return (1/2 - (w1 + w2 + w3 + w4 + w5 + w6))

def triangle_wave(freq, duration, fs = 44100):
    return 2/np.pi * np.arcsin(sine_wave(freq, duration, fs))

def noise(duration, fs=44100):
    return np.random.uniform(size = int(duration * fs))*2-1

def simple_play(audio, fs = 44100):
    if isinstance(audio, Tone):
        audio = audio.array
    sound = audio * (2**15 - 1) / np.max(np.abs(audio))
    sound = sound.astype(np.int16)
    play_obj = sa.play_buffer(sound, 1, 2, fs)
    play_obj.wait_done()

def apply(array, f, fs = 44100):
    duration = len(array)/fs
    t = f(np.linspace(0, duration, int(duration*fs), False))
    return np.multiply(t, array)

def fade_out(array, f, fs=44100):
    duration = len(array)/fs
    return (array, lambda x: x / duration, fs)

def noise_snare(duration, fs = 44100):
    return apply(noise(duration, fs), lambda x : np.power(x+1, -10))

class Tone:
    def __init__(self, array, volume = 1, fs = 44100):
        self.duration = len(array)/fs
        print("Duration: " + str(self.duration))
        self.array = array * volume

    def __add__(self, other, fs = 44100):
        return Tone(np.append(self.array, other.array), fs = 44100)

    def __mul__(self, other, fs = 44100):
        if self.duration == other.duration:
            return Tone(self.array + other.array, fs = 44100)
    
    def blend(self, other, time, fs = 44100):
        if time <= self.duration:
            d = int(other.duration*fs)
            t = int(time*fs)
            t1 = self.array[:t]
            t2 = self.array[t:d+t] + other.array
            t3 = self.array[d+t:]
            return Tone(np.append(np.append(t1, t2), t3), fs = 44100)

class Drum(Tone):
    pass

print(noise_snare(0.3))

a = Tone(triangle_wave(220, 0.5))
c = Tone(triangle_wave(261, 0.5))
d = Tone(triangle_wave(293, 0.5)) 
e = Tone(triangle_wave(329, 0.5)) 
f = Tone(triangle_wave(349, 0.5))
g = Tone(triangle_wave(220, 0.5))
c_bass = Tone(saw_wave(130, 1), 0.7)
d_bass = Tone(saw_wave(146, 1), 0.7)
e_bass = Tone(saw_wave(164, 1), 0.7)

t = (e_bass + c_bass + d_bass + c_bass) * (c + e + g + f + d + a + e + c)
d1 = Tone(noise_snare(0.3), volume = 2)
t = t.blend(d1, 0)
t = t.blend(d1, 1)
t = t.blend(d1, 2)
t = t + t
simple_play(t) 

save_wav("test1.wav", t)