#!/usr/bin/env python2
import midi
from copy import copy
from pprint import pprint


def compress_state(state):
    ret = []
    for pitch, volume in enumerate(state):
        if volume > 0:
            ret.append(pitch)
    return ret


def compress_state_matrix(state_matrix):
    ret = []
    for state in state_matrix:
        ret.append(compress_state(state))
    return ret


def load_midi(filename):
    state_matrix = []
    state = [0] * 128

    pattern = midi.read_midifile(filename)
    pprint(pattern)

    for evt in pattern[0]:
        if isinstance(evt, midi.EndOfTrackEvent):
            break
        elif isinstance(evt, midi.NoteEvent):
            if evt.tick > 0:
                for i in xrange(evt.tick):
                    state_matrix.append(copy(state))
            if isinstance(evt, midi.NoteOffEvent) or evt.data[1] == 0:
                state[evt.pitch] = 0
            else:
                state[evt.pitch] = evt.data[1]

    return state_matrix


def main():
    filename = 'music/e1.midi'
    state_matrix = load_midi(filename)
    pprint(compress_state_matrix(state_matrix))


if __name__ == '__main__':
    main()
