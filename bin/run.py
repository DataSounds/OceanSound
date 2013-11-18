#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join, exists
from os import getcwd
from sys import argv
import subprocess
import time
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pygame.mixer
pygame.mixer.init()

from DataSounds.sounds import get_music

from OceanSound.extract import extract_series
from OceanSound.visuals import plot_series, plot_animation

def pos_camera(color):
    b = get_image()
    corners = find_corners(b, color=color)
    boat = find_boat(b, color=color)
    lat, lon = boat_lat_lon(boat, corners)
    return np.array([lat]), np.array([lon])

def basemap_ui():

    def tellme(s):
        plt.title(s,fontsize=16)
        plt.draw()

    fig = plt.figure(0, figsize=(10, 5))
    globe = Basemap()
    globe.bluemarble()
    parallels = np.arange(-80,80,10.)
    # labels = [left,right,top,bottom]
    globe.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,351.,20.)
    globe.drawmeridians(meridians,labels=[True,False,False,True])

    points = []
    while len(points) == 0:
        tellme('Select one point with mouse click')
        points = plt.ginput(1, timeout=-1)
        if len(points) != 1:
            time.sleep(1)

    point = points[0]
    plt.close('all')
    return np.array((point[0],)), np.array((point[1],))

def pos_command_line():
    coords = raw_input('OceanSound> Input latitude and longitude: ')
    lat, lon = coords.strip('(').strip(')').split(',')
    LATLIMS = np.array([float(lat)])
    LONLIMS = np.array([float(lon)])
    return LATLIMS, LONLIMS

def do_calc(LATLIMS_AM, LONLIMS_AM, indir, outdir):
    land_checker = Basemap()
    if land_checker.is_land(LATLIMS_AM, LONLIMS_AM):
        print 'SOS! Sorry you have selected a land pixel!'
        pygame.mixer.music.load('SOS.midi')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            #plot animado?
            time.sleep(1)
    else:
        dataAM = extract_series(LATLIMS_AM, LONLIMS_AM, indir)
        data_am = np.double(dataAM['Series'])
        if all(np.isnan(a) for a in data_am):
            print 'THE SOUND OF SILENCE. Also, BATMAN. Everything is Rest and NaN'
            pygame.mixer.music.load('Batman_song.midi')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # Anim plot? See Matplotlib.Animation
                time.sleep(1)
        else:
            am = get_music(data_am)

            music = pygame.mixer.Sound('Oc.midi')
            pygame.mixer.music.load('Oc.midi')
            pygame.mixer.music.play()
            anim = plot_animation(data_am,
                        (u'Music from Lat = %.2f Lon = %.2f'
                            % (dataAM['Lat'], dataAM['Lon'])),
                        'serie.png',
                        t_max=36000)#music.get_length())

#            while pygame.mixer.music.get_busy():
#                pass


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('--mode', choices=('basemap', 'cmd', 'cv'),
                        default='cmd', help='Point selection mode')
    parser.add_argument('--indir', default=join(getcwd(), 'data'),
                        help='input dir with MODIS data')
    parser.add_argument('--outdir', default=getcwd(),
                        help='output dir for MIDI and plots')
    args = parser.parse_args()

    indir, outdir = args.indir, args.outdir

    if args.mode == 'cmd':
        get_pos = pos_command_line
    elif args.mode == 'cv':
        from OceanSound.capture import find_corners, find_boat, get_image
        from OceanSound.capture import calibrate, boat_lat_lon
        color, bg_img, img = calibrate()
        get_pos = partial(pos_camera, color=color)
    elif args.mode == 'basemap':
        get_pos = basemap_ui

    RUNNING = True
    while RUNNING:
        LATLIMS_AM, LONLIMS_AM = get_pos()

        do_calc(LATLIMS_AM, LONLIMS_AM, indir, outdir)

        if args.mode in ('cmd', 'cv'):
            command = raw_input('OceanSound> ')
            if command == 'q':
                RUNNING = False
