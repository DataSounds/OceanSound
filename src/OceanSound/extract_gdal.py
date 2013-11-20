#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
subset_MODIS using gdal package.

Makes a subset of a pixel time series from MODIS
Chlorophyll images.

"""


import gdal
import numpy as np
import glob
import os

from .extract import find_point_index


def extract_grid(filename):
    A = gdal.Open(filename, gdal.GA_ReadOnly)
    pin = A.GetMetadata()
    lon = np.arange(np.float(pin['Westernmost Longitude']),
                    np.float(pin['Easternmost Longitude']),
                    np.float(pin['Longitude Step']))
    lat = np.arange(np.float(pin['Northernmost Latitude']),
                    np.float(pin['Southernmost Latitude']),
                    -np.float(pin['Latitude Step']))

    return lat, lon


def extract_series(LATLIMS, LONLIMS, indir):
    multi_pix = []
    Lat = None
    Lon = None

    files = sorted(glob.glob(os.path.join(indir, 'A*')))
    lat, lon = extract_grid(files[0])
    ilt, ilg = find_point_index(LATLIMS, LONLIMS, lat, lon)

    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        A = gdal.Open(filename, gdal.GA_ReadOnly)
        pin = A.GetMetadata()

        ## load the subset of data needed for the map limits given
        P = np.double(A.ReadAsArray()[ilt, ilg])
        if P < np.float(pin['Data Minimum']):
            P = np.nan
        P = np.float(pin['Slope']) * P + np.float(pin['Intercept'])
        Lat = lat[ilt]  # lat[ilt+np.arange(0,ltlm-1)]
        Lon = lon[ilg]  # lon[ilg+np.arange(0,lglm-1)]
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": Lat, "Lon": Lon}
