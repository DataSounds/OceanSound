#/usr/bin/env python
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


def extract_series(LATLIMS, LONLIMS, indir):
    LATLIMS = np.asarray(LATLIMS)
    LONLIMS = np.asarray(LONLIMS)

    multi_pix = []
    Lat = None
    Lon = None
    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        A = SD(filename)
        pin = A.attributes()
        lon = np.arange(pin['Westernmost Longitude'],
                        pin['Easternmost Longitude'],
                        pin['Longitude Step'])
        lat = np.arange(pin['Northernmost Latitude'],
                        pin['Southernmost Latitude'],
                        -pin['Latitude Step'])
        # Get the indices needed for the area of interest
        # argmin catch the indices of minor element
        ilt = np.int(np.argmin(np.abs(lat - np.max(LATLIMS))))
        ilg = np.int(np.argmin(np.abs(lon - np.min(LONLIMS))))
        # retrieve data SDS
        d = A.datasets()
        sds_name = d.keys()[0]  # name of sds. Dictionary method.
        sds = A.select(sds_name)
        ## load the subset of data needed for the map limits given
        P = np.double(sds[ilt, ilg])
        if P < pin['Data Minimum']:
            P = np.nan
        P = pin['Slope'] * P + pin['Intercept']
        Lat = lat[ilt]
        Lon = lon[ilg]
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": Lat, "Lon": Lon}
