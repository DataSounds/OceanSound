#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
subset_MODIS using pyhdf package.

Makes a subset of a pixel time series from MODIS
Chlorophyll images.
'''


from pyhdf.SD import SD
import numpy as np
import glob
import os

from .extract import find_point_index


def extract_grid(filename):
    A = SD(filename)
    pin = A.attributes()
    lon = np.arange(pin['Westernmost Longitude'],
                    pin['Easternmost Longitude'],
                    pin['Longitude Step'])
    lat = np.arange(pin['Northernmost Latitude'],
                    pin['Southernmost Latitude'],
                    -pin['Latitude Step'])
    return lat, lon


def extract_series(LATLIMS, LONLIMS, indir):
    multi_pix = []
    Lat = None
    Lon = None

    files = sorted(glob.glob(os.path.join(indir, 'A*')))
    lat, lon = extract_grid(files[0])
    ilt, ilg = find_point_index(LATLIMS, LONLIMS, lat, lon)

    for filename in files:
        A = SD(filename)

        # retrieve data SDS
        d = A.datasets()
        sds_name = d.keys()[0]  # name of sds. Dictionary method.
        sds = A.select(sds_name)
        pin = A.attributes()

        ## load the subset of data needed for the map limits given
        P = np.double(sds[ilt, ilg])
        if P < pin['Data Minimum']:
            P = np.nan
        P = pin['Slope'] * P + pin['Intercept']
        Lat = lat[ilt]
        Lon = lon[ilg]
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": Lat, "Lon": Lon}
