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

from .extract import find_point_index, extract_grid


def extract_series(LATLIMS, LONLIMS, indir):
    multi_pix = []
    lat = None
    lon = None

    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        A = gdal.Open(filename, gdal.GA_ReadOnly)
        pin = A.GetMetadata()

        if lat is None or lon is None:
            lat, lon = extract_grid(pin)
            ilt, ilg = find_point_index(LATLIMS, LONLIMS, lat, lon)

        ## load the subset of data needed for the map limits given
        P = np.double(A.ReadAsArray()[ilt, ilg])
        if P < np.float(pin['Data Minimum']):
            P = np.nan
        P = np.float(pin['Slope']) * P + np.float(pin['Intercept'])
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": lat[ilt], "Lon": lon[ilg]}
