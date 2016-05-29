#!/usr/bin/env python2
import midi
import pprint


file_path = 'out.mid'
pattern = midi.read_midifile(file_path)

print pattern
