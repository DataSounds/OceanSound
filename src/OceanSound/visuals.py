#/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def plot_series(series, title, output):
    # line Series
    fig = plt.figure(0)#figsize=(12,5), dpi=300)
    fig.clf()
    fig.suptitle(title)
    fig.add_subplot(211)
    plt.plot(series, 'o-', linewidth=3)
    x = np.arange(2002,2013,1)
    plt.xticks(np.arange(0,121,12),x)

    fig.add_subplot(212)
    series_stacked = np.tile(series, (20,1))
    plt.imshow(series_stacked)
    plt.gca().yaxis.set_visible(False)
    plt.xticks(np.arange(0,121,12),x)
    #plt.xlabel('Ano')
    #plt.ylabel(u'Concentração de Clorofila-a')
    #fig.savefig(output)

    plt.show()
    fig.canvas.draw()

    # Colors
    #plt.savefig('cor_pixeis_%s' % output)


def plot_animation(series, title, output, t_max):
    INTERVAL = 300
    frames = int(t_max / float(INTERVAL))

    fig = plt.figure(1)#figsize=(12,5), dpi=300)
    fig.clf()

    fig.suptitle(title)

    # line Series
    fig.add_subplot(211)
    plt.plot(series, 'o-', linewidth=3)

    bar = np.arange(0, np.nanmax(series), .1)
    marker = plt.axvline(0, linestyle='--')

    x = np.arange(2002,2013,1)
    plt.xticks(np.arange(0,121,12),x)

    # Colors
    fig.add_subplot(212)
    series_stacked = np.tile(series, (20,1))
    plt.imshow(series_stacked)
    plt.gca().yaxis.set_visible(False)
    plt.xticks(np.arange(0,121,12),x)
    #plt.xlabel('Ano')
    #plt.ylabel(u'Concentração de Clorofila-a')
    #fig.savefig(output)

    #plt.savefig('cor_pixeis_%s' % output)

    def init():
        marker.set_data([0], marker.get_ydata())
        return marker,

    def animate(i):
        print i
        marker.set_data([i], marker.get_ydata())
        return marker,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frames, interval=INTERVAL, blit=False)
    plt.show()
