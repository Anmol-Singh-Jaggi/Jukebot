#!/usr/bin/env python2
'''
Convert integer-model to boolean and back.
'''
from midi_debug import *


def remove_volume_from_state(state):
    """
    Converts the state vector to boolean format.
    Assigns state[pitch] = 1 wherever state[pitch] != 0
    :param state: The state vector.
    :type state: list
    :returns: A tuple of (volume_sum, volume_num) signifying the
     sum of all the non-zero volumes and their frequency respectively.
    :return_type: (int, int)
    """
    volume_sum = 0
    volume_num = 0

    for pitch, volume in enumerate(state):
        if volume > 0:
            volume_sum += volume
            volume_num += 1
            state[pitch] = 1

    return (volume_sum, volume_num)


def remove_volume_from_state_matrix(state_matrix):
    """
    Converts the state-matrix to boolean format.
    Assigns state_matrix[pitch][volume] = 1 wherever
    state_matrix[pitch][volume] != 0
    :param state_matrix: The state-matrix.
    :type state_matrix: 2-D list
    :returns: The average of all the non-zero volumes encountered.
    :return_type: int
    """
    volume_sum = 0
    volume_num = 0

    for idx, state in enumerate(state_matrix):
        volume_sum_state, volume_num_state = remove_volume_from_state(state)

        volume_sum += volume_sum_state
        volume_num += volume_num_state

    volume_avg = (1.0 * volume_sum) / volume_num

    return int(volume_avg)


def insert_volume_into_state(state, volume_new):
    """
    Converts the state vector to integer format from boolean.
    Assigns state[pitch] = volume_new wherever state[pitch] != 0
    :param state: The state vector.
    :type state: list
    :param volume_new: The new volume to be assigned to all the non-zero cells.
    :type volume_new: int
    :returns: None
    """
    for pitch, volume in enumerate(state):
        state[pitch] = state[pitch] * volume_new


def insert_volume_into_state_matrix(state_matrix, volume_new):
    """
    Converts the state-matrix to integer format from boolean.
    Assigns state_matrix[pitch][volume] = volume_new wherever
    state_matrix[pitch][volume] != 0
    :param state_matrix: The state-matrix.
    :type state_matrix: 2-D list
    :param volume_new: The new volume to be assigned to all the non-zero cells.
    :type volume_new: int
    :returns: None
    """
    for idx, state in enumerate(state_matrix):
        insert_volume_into_state(state, volume_new)


def main():
    filepath = 'debug.mid'
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
