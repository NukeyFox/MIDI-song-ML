import instruments
import random
import simpleaudio as sa
from scipy.io.wavfile import write
import numpy as np
import re

class beat_manager():
    def __init__(self, drum_sounds):
        self.drum_sounds = drum_sounds
        self.drum_patterns = []

    def define_pattern(self, inputs):
        pass

    def generate_beat(self, tempo):
        pass

class melody_manager():
    def __init__(self, chords, chords_transitions, melody, instruments, depth = 2, seed = 0):
        self.depth = depth
        self.instruments = instruments
        self.chords = chords
        self.melody = melody
        self.current_state = 0 
        random.seed(seed)
    
    def generate_next_chord(self, inputs):
        options = self.chords[inputs]
        return options

    def generate_next_note(self, inputs):
        if inputs not in self.melody.keys():
            return random.randint(0,len(self.chords))
        options = self.melody[inputs]
        return random.choice(options)

    def generate_song(self, pitch, intruments, tempo, duration):
        #tempo in bpm 
        pass


def read_transition_from_file(file_name):
    transitions = {}
    p = re.compile(r'\d+')
    f = open(file_name,'r')
    lines = f.read()
    f.close()
    for line in lines:
        in_out = line.split(" = ")
        output = output[1]
        inputs = map(lambda x : int(x), p.findall(in_out[0]))
        output = map(lambda x : int(x), p.findall(in_out[1]))
        transitions[tuple(inputs)] = output
    return transitions

#m = song_manager(major_chords, major_instr, [])
#read_transition_from_file("/hardcoded.txt")

    