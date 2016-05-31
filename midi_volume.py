#!/usr/bin/env python2
'''
Convert integer-model to boolean and back.
'''
from midi_debug import *


def remove_volume_from_state(state):
    volume_sum = 0
    volume_num = 0

    for pitch, volume in enumerate(state):
        if volume > 0:
            volume_sum += volume
            volume_num += 1
            state[pitch] = 1

    return (volume_sum, volume_num)


def remove_volume_from_state_matrix(state_matrix):
    volume_sum = 0
    volume_num = 0

    for idx, state in enumerate(state_matrix):
        volume_sum_state, volume_num_state = remove_volume_from_state(state)

        volume_sum += volume_sum_state
        volume_num += volume_num_state

    volume_avg = (1.0 * volume_sum) / volume_num

    return int(volume_avg)


def insert_volume_into_state(state, volume_new):
    for pitch, volume in enumerate(state):
        state[pitch] = state[pitch] * volume_new


def insert_volume_into_state_matrix(state_matrix, volume_new):
    for idx, state in enumerate(state_matrix):
        insert_volume_into_state(state, volume_new)


def main():
    filepath = 'music/debug.mid'
    state_matrix, _ = midi_to_sequence(filepath)
    print desparsify_state_matrix(state_matrix)
    print '\n\n\n'

    volume_avg = remove_volume_from_state_matrix(state_matrix)
    print desparsify_state_matrix(state_matrix)
    print '\n\n\n'
    print volume_avg
    print '\n\n\n'

    insert_volume_into_state_matrix(state_matrix, volume_avg)
    print desparsify_state_matrix(state_matrix)
    print '\n\n\n'


if __name__ == '__main__':
    main()
