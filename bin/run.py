#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser, join
import subprocess
import time

import numpy as np
#import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pygame.mixer
#pygame.init()
pygame.mixer.init()

from OceanSound.extract import extract_series
from OceanSound.sounds import get_music
from OceanSound.capture import find_corners, find_boat, get_image, boat_lat_lon, calibrate
from OceanSound.visuals import plot_series

def pos_dummy():
    ## setting limits to cut
    LATLIMS_AM = np.array([0]) #foz do rio amazonas
    LONLIMS_AM = np.array([-45])

    #LATLIMS_AT = np.array([-23]) #Oc. Atlantico
    #LONLIMS_AT = np.array([-30])

    return LATLIMS_AM, LONLIMS_AM

def pos_camera(color):
    b = get_image()
    corners = find_corners(b, color=color)
    boat = find_boat(b, color=color)
    lat, lon = boat_lat_lon(boat, corners)
    return np.array([lat]), np.array([lon])

def basemap_ui():

    fig = plt.figure(0, figsize=(20, 10))
    globe = Basemap()
    globe.bluemarble()
    parallels = np.arange(-81,81,10.)
    # labels = [left,right,top,bottom]
    globe.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,351.,20.)
    globe.drawmeridians(meridians,labels=[True,False,False,True])

    def on_pick(event):
        print event.xdata, event.ydata
        do_calc(np.array([event.xdata]), np.array([event.ydata]))

    fig.canvas.mpl_connect('button_release_event', on_pick)
    plt.show()

def pos_command_line():
    coords = raw_input('OceanSound> Entre com a latitude e a longitude: ')
    lat, lon = coords.strip('(').strip(')').split(',')
    LATLIMS = np.array([float(lat)])
    LONLIMS = np.array([float(lon)])
    return LATLIMS, LONLIMS

def set_indir_outdir():
    if os.path.exists((os.path.join(os.getcwd()) + '/data/')):
        indir = os.path.join(os.getcwd(), 'data/')
    else:
        EOFError
        indir = raw_input('digite aqui o diretorio do seus dados > ')
    outdir = os.getcwd()
    return indir, outdir

#color, bg_img, img = calibrate()
#import pdb; pdb.set_trace()
RUNNING = True
while RUNNING:
    #LATLIMS_AM, LONLIMS_AM = pos_dummy()
    #LATLIMS_AM, LONLIMS_AM = pos_camera(color=color)
    indir, outdir = set_indir_outdir()
    LATLIMS_AM, LONLIMS_AM = pos_command_line()
#    do_calc(LATLIMS_AM, LONLIMS_AM)

    land_checker = Basemap()
    if land_checker.is_land(LATLIMS_AM, LONLIMS_AM):
        print 'SOS! Array indefinido. Ponto em terra!'
        pygame.mixer.music.load('SOS.midi')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            #plot animado?
            time.sleep(1)
    else:
        dataAM = extract_series(LATLIMS_AM, LONLIMS_AM, indir, outdir)
        #np.savez(join(outdir, 'multiPixAM'), **dataAM)

        #a = np.load(join(outdir, 'multiPixAM.npz'))

        data_am = np.double(dataAM['Series'])
        if all(np.isnan(a) for a in data_am):
            print 'THE SOUND OF SILENCE. Also, BATMAN. Tudo é Rest e NaN'
            pygame.mixer.music.load('Batman_song.midi')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                #plot animado?
                time.sleep(1)
        else:
            am = get_music(data_am, name='am')

            pygame.mixer.music.load('am_cbo_select_music.mid')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if pygame.mixer.music.get_pos() % 1000 > 950:
                    plot_series(data_am,
                        (u'Música do ponto Lat = %.2f Lon = %.2f'
                            % (dataAM['Lat'], dataAM['Lon'])),
                        'serie.png',
                        tstep=pygame.mixer.music.get_pos())
                #time.sleep(.5)
    command = raw_input('OceanSound> ')
    if command == 'q':
        RUNNING = False
