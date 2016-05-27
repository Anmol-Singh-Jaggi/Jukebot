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


def load_midi(filepath):
    state_matrix = []
    state = [0] * 128

    pattern = midi.read_midifile(filepath)
    pprint(pattern)

    for event in pattern[0]:
        if isinstance(event, midi.EndOfTrackEvent):
            break
        elif isinstance(event, midi.NoteEvent):
            if event.tick > 0:
                state_matrix += event.tick * [copy(state)]
            if isinstance(event, midi.NoteOffEvent) or event.data[1] == 0:
                state[event.pitch] = 0
            else:
                state[event.pitch] = event.data[1]

    return state_matrix


def main():
    filepath = 'music/e1.midi'
    state_matrix = load_midi(filepath)
    pprint(compress_state_matrix(state_matrix))


if __name__ == '__main__':
    main()
