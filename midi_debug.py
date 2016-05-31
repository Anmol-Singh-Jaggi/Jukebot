#!/usr/bin/env python2
'''
Utilities for debugging midi.
'''
import midi
from pprint import pprint


def compress_state(state):
    """
    Outputs the list of notes which are ON in the current state.
    Used mainly for printing/debugging.
    :param state: A sparse vector containing notes and their volumes.
    state[pitch] = volume
    :type state: list
    :returns: A list of the notes which are ON in the input state.
    :return_type: list
    """
    ret = []
    for pitch, volume in enumerate(state):
        if volume > 0:
            ret.append(pitch)
    return ret


def compress_state_matrix(state_matrix):
    """
    Outputs a 2-D matrix of notes which are ON in the states.
    Used mainly for printing/debugging.
    :param state_matrix: A sparse matrix containing notes and their volumes.
    state_matrix[state_index][pitch] = volume
    :type state_matrix: 2-D list
    :returns: A matrix of the notes which are ON in a state.
    :return_type: str
    """
    ret = ""
    for idx, state in enumerate(state_matrix):
        ret += str(idx) + ".) " + str(compress_state(state)) + "\n"
    return ret


def main():
    file_path = 'out.mid'
    pattern = midi.read_midifile(file_path)
    print pattern


if __name__ == '__main__':
    main()
