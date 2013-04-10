#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
from sebastian.lilypond.interp import parse
import fluidsynth

from OceanSound.sounds import build_scale, note_number, note_name

SF2 = os.environ.get('SOUNDFONT', "/usr/share/sounds/sf2/FluidR3_GS.sf2")


def main():
    fs = fluidsynth.Synth()
    fs.start()

    sfid = fs.sfload(SF2)
    fs.program_select(0, sfid, 0, 0)

    #matriz = np.array([[15,14,13,12],[14,12,10,8],[13,10,7,4],[12,8,4,0]],
    #                  dtype=np.float64)
    matriz = np.array([[15, 14, 13, 12, 11, 7, 9, 5, 13, 11, 12, 18],
                       [14, 12, 10, 8, 11, 13, 15, 5, 11, 17, 18, 9],
                       [13, 10, 7, 4, 11, 17, 8, 9, 18, 11, 14, 11],
                       [12, 8, 4, 0, 11, 16, 7, 13, 9, 10, 12, 15]],
                      dtype=np.float64)

    scale = build_scale('C', mode='major', octaves=1)
    notes = note_number(matriz, scale)

    def play_music(x, y):
        if matriz.shape[1] > matriz.shape[0]:
            note = notes[y, x]
        else:
            note = notes[x, y]

        melody = parse(note_name(note, scale))

        for s in melody:
            if 'midi_pitch' in s:
                fs.noteon(0, s['midi_pitch'], 100)
                #fs.noteoff(0, s['midi_pitch'])

    def on_move(event):
        x, y = event.xdata, event.ydata
        print('x = %s & y = %s' % (x, y))
        play_music(x, y)

    fig = plt.figure()
    fig.canvas.mpl_connect('motion_notify_event', on_move)
    ax = fig.add_subplot(111)
    ax.contourf(matriz)
    plt.show()

main()
