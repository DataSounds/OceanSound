#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
subset_MODIS

Programa para Fazer um subset teemporal de um pixel de imagens MODIS
Dentro dos limites Lat e Long determinados.

Baseado em subset_MODIS.py

Author =  Arnaldo Russo
e-mail =  arnaldorusso@gmail.com
'''
from pyhdf.SD import *
import numpy as np
import glob
import os
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#import scipy.io


def extract_series(LATLIMS, LONLIMS, indir):
    LATLIMS = np.asarray(LATLIMS)
    LONLIMS = np.asarray(LONLIMS)

    filelist = glob.glob(os.path.join(indir, 'A*'))
    filelist.sort()
    nfiles = len(filelist)
    files = []
    for path in filelist:
      files.append(path[len(indir):]) # remove path name

    names = []
    multi_pix = []
    for i in range(len(filelist)):
        A = SD(filelist[i])
        a = A.attributes()
        for k in xrange(0,len(a.keys())):
            nm = a.keys()[k]
            names.append(nm.replace(" ","_"))
        pin = dict(zip(names,a.values()[:]))
        lon = np.arange(pin['Westernmost_Longitude'],pin['Easternmost_Longitude'],pin['Longitude_Step'])
        lat = np.arange(pin['Northernmost_Latitude'],pin['Southernmost_Latitude'],-pin['Latitude_Step'])
        # Get the indices needed for the area of interest
        # argmin catch the indices of minor element
        ilt = np.int(np.argmin(np.abs(lat-np.max(LATLIMS))))
        ilg = np.int(np.argmin(np.abs(lon-np.min(LONLIMS))))
        # retrieve data SDS
        d = A.datasets()
        sds_name = d.keys()[0] # name of sds. Dictionary method.
        sds = A.select(sds_name)
        ## load the subset of data needed for the map limits given
        P = sds[ilt,ilg]
        P = np.double(P)
        if P < pin['Data_Minimum']:
            P = np.nan
        #P[P<pin['Data_Minimum']] = np.nan
        P = (pin['Slope']*P+pin['Intercept'])
        Lat = lat[ilt] # lat[ilt+np.arange(0,ltlm-1)]
        Lon = lon[ilg] # lon[ilg+np.arange(0,lglm-1)]
        multi_pix.append(P)


    #multi_pix[multi_pix < pin['Data_Minimum']] = np.nan
    PAM = np.asarray(multi_pix)
    return {"Series":PAM, "Lat":Lat, "Lon":Lon}
