#!/usr/bin/env python2
'''
Compress state matrix and back.
'''
from midi_debug import *
from midi_sequence import *


def transpose(grid):
    return map(list, zip(*grid))


def compress_state_matrix(state_matrix):
    ret = []
    columns_present = []

    state_matrix_transposed = transpose(state_matrix)

    for idx, pitch_column in enumerate(state_matrix_transposed):
        if not all(volume == 0 for volume in pitch_column):
            ret.append(list(pitch_column))
            columns_present.append(idx)

    ret = transpose(ret)

    return ret, columns_present


def decompress_state_matrix(state_matrix, columns_present):
    ret = [[0] * 128] * len(state_matrix)
    ret = transpose(ret)

    state_matrix_transposed = transpose(state_matrix)

    for idx, col in enumerate(columns_present):
        ret[col] = list(state_matrix_transposed[idx])

    ret = transpose(ret)

    return ret


def main():
    filepath = 'debug.mid'
    state_matrix, _ = midi_to_sequence(filepath)
    print desparsify_state_matrix(state_matrix)
    print '\n\n\n'

    state_matrix_compressed, columns_present = compress_state_matrix(
        state_matrix)
    print desparsify_state_matrix(state_matrix_compressed)
    print '\n\n\n'
    print columns_present
    print '\n\n\n'

    state_matrix_decompressed = decompress_state_matrix(
        state_matrix_compressed, columns_present)
    print desparsify_state_matrix(state_matrix_decompressed)
    print '\n\n\n'

    assert(state_matrix == state_matrix_decompressed)


if __name__ == '__main__':
    main()
