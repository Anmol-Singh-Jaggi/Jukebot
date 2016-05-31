#!/usr/bin/env python2
'''
Generate custom midi files for debugging.
'''
import midi


pattern = midi.Pattern()
track = midi.Track()
pattern.append(track)


track.append(midi.NoteOnEvent(tick=0, channel=0, data=[48, 105]))
track.append(midi.NoteOnEvent(tick=0, channel=0, data=[60, 105]))
track.append(midi.NoteOffEvent(tick=2, channel=0, data=[60, 0]))
track.append(midi.NoteOnEvent(tick=1, channel=0, data=[60, 80]))
track.append(midi.NoteOffEvent(tick=2, channel=0, data=[48, 0]))
track.append(midi.NoteOffEvent(tick=0, channel=0, data=[60, 0]))
track.append(midi.NoteOnEvent(tick=1, channel=0, data=[48, 95]))
track.append(midi.NoteOnEvent(tick=0, channel=0, data=[65, 95]))
track.append(midi.NoteOffEvent(tick=2, channel=0, data=[65, 0]))


eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)


print pattern
midi.write_midifile("debug.mid", pattern)
