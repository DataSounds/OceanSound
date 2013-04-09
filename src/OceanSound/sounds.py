#/usr/bin/env python
# -*- coding: utf-8 -*-

from StringIO import StringIO
from bisect import bisect

import numpy as np

from sebastian.lilypond.interp import parse
from sebastian.midi.write_midi import SMF


def note_classes(arr, scale):
    a = np.nanmin(arr)
    b = np.nanmax(arr)
    notes_class = np.arange(a, b, (b - a) / len(scale))
    return notes_class


def note_number(arr, scale):
    x_notes = note_classes(arr, scale)
    mapping = []
    if len(arr.shape) >= 2:
        for idx, value in np.ndenumerate(arr):
            mapping.append(np.array(bisect(x_notes, value), dtype='f8') - 1)
    else:
        mapping = np.asarray([bisect(x_notes, a) for a in arr], dtype='f8') - 1
        mapping[np.isnan(arr)] = np.nan
    mapping = np.reshape(mapping, arr.shape)
    return mapping


def build_scale(base_note, mode='major', octaves=1):
    if mode == 'major':
        intervals = [0, 2, 4, 5, 7, 9, 11]
    elif mode == 'minor':
        intervals = [0, 2, 3, 5, 7, 8, 10]
    elif mode == 'pentatonic':
        intervals = [0, 2, 4, 7, 9]

    intervals = [n + (12 * octave)
                 for octave in range(octaves)
                 for n in intervals]

    notes = [n + ("'" * octave)
             for octave in range(octaves)
             for n in "c cis d dis e f fis g gis a ais b".split()]
    scale_names = np.roll(notes,
                          notes.index(base_note.lower().replace('#', 'is')))
    scale_notes = [scale_names[s] for s in intervals]
    return scale_notes


def note_name(number, scale):
    '''
    Transform a number to a note string, including np.nan as musical rests.
    '''
    if np.isnan(number):
        return "r"
    else:
        return scale[int(number)]


def chord_scaled(arr, scale, period=12):
    remainder = arr.size % period
    if remainder:
        fill = period - remainder
        arr = np.append(arr, np.zeros(fill) * np.nan)

    arr_scaled = np.int32([np.nansum(row) / len(row)
                           for row in arr.reshape((-1, period))])

    return None


def get_music(series, period=12, key='C', mode='major', octaves=2):
    midi_out = StringIO()

    if all(np.isnan(series)):
        s = SMF([])
        s.write(midi_out)
    else:
        scale = build_scale(key, mode, octaves)

        notes = note_number(series, scale)
        melody = parse(' '.join([note_name(x, scale) for x in notes]))

        chords = chord_scaled(series, scale, period)
        harmony = parse(chords)

        # Transform it to a MIDI file with chords.
#        s = SMF([melody // harmony])
        s = SMF([melody])
        s.write(midi_out)

    return midi_out
