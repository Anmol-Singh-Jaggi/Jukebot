#!/usr/bin/env python2
'''
Convert midi pattern to matrix and back.
Currently full support provided for midi-format 0 only.
Use for format 1 and 2 at your own risk !
'''
import midi
from copy import copy
from pprint import pprint


def midi_to_sequence(filepath):
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
    #pprint(pattern, open('pattern_correct', 'w'))

    tempo_event = None

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

        # Find the tempo-event in the track.
        # This is not required for RNN training.
        # But is required to generate coherent music.
        for i in xrange(min(10, len(track))):
            if isinstance(track[i], midi.SetTempoEvent):
                tempo_event = track[i]
                break

    return state_matrix, (pattern.resolution, tempo_event)


def get_next_different_state(state_matrix, index):
    """
    Helper for sequence_to_midi().
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
    Helper for sequence_to_midi().
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


def sequence_to_midi(state_matrix, filepath, meta_info=None):
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
    resolution, tempo_event = meta_info if meta_info else None

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
    filepath = 'debug.mid'
    state_matrix, meta_info = midi_to_sequence(filepath)
    pattern = sequence_to_midi(state_matrix, 'out.mid', meta_info)
    #pprint(pattern, open('pattern_gen', 'w'))


if __name__ == '__main__':
    main()
