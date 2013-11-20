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

from .extract import find_point_index, extract_grid


def extract_series(LATLIMS, LONLIMS, indir):
    multi_pix = []
    lat = None
    lon = None

    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        A = SD(filename)

        # retrieve data SDS
        d = A.datasets()
        sds_name = d.keys()[0]  # name of sds. Dictionary method.
        sds = A.select(sds_name)
        pin = A.attributes()

        if lat is None or lon is None:
            lat, lon = extract_grid(pin)
            ilt, ilg = find_point_index(LATLIMS, LONLIMS, lat, lon)

        ## load the subset of data needed for the map limits given
        P = np.double(sds[ilt, ilg])
        if P < pin['Data Minimum']:
            P = np.nan
        P = pin['Slope'] * P + pin['Intercept']
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": lat[ilt], "Lon": lon[ilg]}
