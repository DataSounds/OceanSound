#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
subset_MODIS using gdal package.

Makes a subset of a pixel time series from MODIS
Chlorophyll images.
'''


import gdal
import numpy as np
import glob
import os


def extract_series(LATLIMS, LONLIMS, indir):
    LATLIMS = np.asarray(LATLIMS)
    LONLIMS = np.asarray(LONLIMS)

    multi_pix = []
    Lat = None
    Lon = None
    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        A = gdal.Open(filename, gdal.GA_ReadOnly)
        a = A.GetMetadata()
        lon = np.arange(np.float(a['Westernmost Longitude']),
                        np.float(a['Easternmost Longitude']),
                        np.float(a['Longitude Step']))
        lat = np.arange(np.float(a['Northernmost Latitude']),
                        np.float(a['Southernmost Latitude']),
                        -np.float(a['Latitude Step']))
        # Get the indices needed for the area of interest
        # argmin catch the indices of minor element
        ilt = np.argmin(np.abs(lat - np.max(LATLIMS)))
        ilg = np.argmin(np.abs(lon - np.min(LONLIMS)))
        ## load the subset of data needed for the map limits given
        P = np.double(A.ReadAsArray()[ilt, ilg])
        if P < np.float(a['Data Minimum']):
            P = np.nan
        P = np.float(a['Slope']) * P + np.float(a['Intercept'])
        Lat = lat[ilt]  # lat[ilt+np.arange(0,ltlm-1)]
        Lon = lon[ilg]  # lon[ilg+np.arange(0,lglm-1)]
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": Lat, "Lon": Lon}
