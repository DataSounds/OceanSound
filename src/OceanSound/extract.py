#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chooses package between pyhdf and gdal to deal with HDF4 files.

This function will import extract_series to construct your Chlorophyll-a
time series.

"""

import glob
import os

import numpy as np

try:
    import extract_pyhdf as extractor
except ImportError:
    try:
        import extract_gdal as extractor
    except ImportError:
        print("You must have installed pyhdf or gdal package")


def find_point_index(LATLIMS, LONLIMS, lats, lons):
    LATLIMS = np.asarray(LATLIMS)
    LONLIMS = np.asarray(LONLIMS)

    # Get the indices needed for the area of interest
    # argmin catch the indices of minor element
    ilt = np.int(np.argmin(np.abs(lats - np.max(LATLIMS))))
    ilg = np.int(np.argmin(np.abs(lons - np.min(LONLIMS))))

    return ilt, ilg


def extract_grid(pin):
    lon = np.arange(np.float(pin['Westernmost Longitude']),
                    np.float(pin['Easternmost Longitude']),
                    np.float(pin['Longitude Step']))
    lat = np.arange(np.float(pin['Northernmost Latitude']),
                    np.float(pin['Southernmost Latitude']),
                    -np.float(pin['Latitude Step']))

    return lat, lon


def extract_series(LATLIMS, LONLIMS, indir, extractor=extractor):
    multi_pix = []
    lat = None
    lon = None

    for filename in sorted(glob.glob(os.path.join(indir, 'A*'))):
        dataset, pin = extractor.open_file(filename)

        if lat is None or lon is None:
            lat, lon = extract_grid(pin)
            ilt, ilg = find_point_index(LATLIMS, LONLIMS, lat, lon)

        ## load the subset of data needed for the map limits given
        P = np.double(extractor.extract_point(dataset, ilt, ilg))
        if P < np.float(pin['Data Minimum']):
            P = np.nan
        P = np.float(pin['Slope']) * P + np.float(pin['Intercept'])
        multi_pix.append(P)

    return {"Series": np.asarray(multi_pix), "Lat": lat[ilt], "Lon": lon[ilg]}
