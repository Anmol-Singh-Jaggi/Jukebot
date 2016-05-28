#!/usr/bin/env python2
import midi
from copy import copy
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


def load_midi(filepath):
    """
    Loads a midi file and outputs the corresponding 'state_matrix'.
    state_matrix[tick][pitch] = volume
    Each row corresponds to the state of notes in a tick.
    :param filepath: The path of the midi file.
    :type filepath: str
    :returns: The state-matrix and some meta-info (resolution, tempo_event)
    :return_type: (2-D list, (int, SetTempoEvent or None))
    """
    state_matrix = []

    pattern = midi.read_midifile(filepath)
    pprint(pattern, open('pattern_correct', 'w'))

    for track in pattern:
        # Null state
        state = [0] * 128
        for event in track:
            if isinstance(event, midi.EndOfTrackEvent):
                # Append the final state 1 time as EndOfTrackEvent has tick = 1
                state_matrix += [copy(state)]
                break
            elif isinstance(event, midi.NoteEvent):
                if event.tick > 0:
                    # A change in state has happened.
                    # Append the current state to the state_matrix.
                    state_matrix += event.tick * [copy(state)]
                if isinstance(event, midi.NoteOffEvent):
                    # Make the volume of the pitch to be 0
                    state[event.pitch] = 0
                else:
                    state[event.pitch] = event.data[1]

    # Find the tempo-event in the pattern.
    # This is not required for RNN training.
    # But is required to generate coherent music.
    tempo_event = None
    for i in xrange(10):
        if isinstance(pattern[0][i], midi.SetTempoEvent):
            tempo_event = pattern[0][i]
            break

    return state_matrix, (pattern.resolution, tempo_event)


def get_next_different_state(state_matrix, index):
    """
    Helper for dump_midi().
    Find the index of the next state which is different from the input state.
    :param state_matrix: The state-matrix.
    :type state_matrix: 2-D list
    :returns: The index of the (chronological) next state which is different
    from the input state.
    :return_type: int
    """
    for i in xrange(index + 1, len(state_matrix)):
        if state_matrix[i] != state_matrix[index]:
            return i
    return len(state_matrix)


def state_diff(current_state, next_state):
    """
    Helper for dump_midi().
    Finds the notes that have changed state (ON/OFF) between 2 states (ticks).
    :param current_state: The first state.
    :type current_state: list
    :param next_state: The chronologically second state.
    :type next_state: list
    :returns: The set of notes which have been changed b/w 2 states.
    :return_type: ((int, int), (int, int))
    """
    notes_on = []
    notes_off = []

    for pitch, (volume1, volume2) in enumerate(zip(current_state, next_state)):
        if volume1 == 0 and volume2 > 0:
            notes_on.append([pitch, volume2])
        elif volume1 > 0 and volume2 == 0:
            notes_off.append([pitch, volume2])

    return (notes_on, notes_off)


def dump_midi(state_matrix, filepath, meta_info=None):
    """
    Converts a state_matrix to the corresponding 'pattern'
    and writes the pattern as a midi file.
    :param state_matrix: The state matrix.
    :type state_matrix: 2-D list
    :param filepath: The path of the output midi file.
    :type filepath: str
    :param meta_info: Resolution and tempo-event of the pattern.
    :type meta_info: (int, SetTempoEvent or None) or None
    :returns: The pattern corresponding to the state matrix.
    :return_type: list
    """
    resolution = meta_info[0] if meta_info else None
    tempo_event = meta_info[1] if meta_info else None

    pattern = midi.Pattern(resolution=resolution)
    track = midi.Track()
    pattern.append(track)
    if tempo_event:
        track.append(tempo_event)

    # Append the very first tick (which will only have NoteOn events)
    notes_on, _ = state_diff([0] * 128, state_matrix[0])
    for note in notes_on:
        track.append(midi.NoteOnEvent(tick=0, channel=0, data=note))

    # Append the rest of the ticks
    current_state_index = 0
    while current_state_index < len(state_matrix):
        next_state_index = get_next_different_state(
            state_matrix, current_state_index)
        ticks_elapsed = next_state_index - current_state_index

        current_state = state_matrix[current_state_index]
        next_state = state_matrix[next_state_index] if next_state_index < len(
            state_matrix) else [0] * 128
        notes_on, notes_off = state_diff(current_state, next_state)

        for note in notes_on:
            track.append(midi.NoteOnEvent(
                tick=ticks_elapsed, channel=0, data=note))
            # The rest of the events are happening simultaneously,
            # so set time_elapsed (tick) = 0 for them
            ticks_elapsed = 0

        for note in notes_off:
            track.append(midi.NoteOffEvent(
                tick=ticks_elapsed, channel=0, data=note))
            ticks_elapsed = 0

        current_state_index = next_state_index

    track.append(midi.EndOfTrackEvent(tick=1))
    midi.write_midifile(filepath, pattern)

    return pattern


def main():
    filepath = 'music/alb_esp1.mid'
    state_matrix, meta_info = load_midi(filepath)
    pattern = dump_midi(state_matrix, 'out.mid', meta_info)
    #pprint(pattern, open('pattern_gen', 'w'))


if __name__ == '__main__':
    main()
