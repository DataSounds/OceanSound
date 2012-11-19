#/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def plot_series(series, title, output, tstep=None):
    # line Series
    fig = plt.figure(0)#figsize=(12,5), dpi=300)
    fig.clf()
    fig.suptitle(title)
    fig.add_subplot(211)
    plt.plot(series, 'o-', linewidth=3)
    if tstep:
        bar = np.arange(0, np.nanmax(series), .1)
        plt.plot([tstep/300.] * len(bar), bar, '--')
    x = np.arange(2002,2013,1)
    plt.xticks(np.arange(0,121,12),x)

    fig.add_subplot(212)
    series_stacked = np.tile(series, (20,1))
    plt.imshow(series_stacked)
    plt.gca().yaxis.set_visible(False)
    plt.xticks(np.arange(0,121,12),x)
    if tstep:
        pass #plt.plot()
    #plt.xlabel('Ano')
    #plt.ylabel(u'Concentração de Clorofila-a')
    #fig.savefig(output)

    plt.show()
    fig.canvas.draw()

    # Colors
    #plt.savefig('cor_pixeis_%s' % output)



