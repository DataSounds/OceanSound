#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Chooses package between pyhdf and gdal to deal with HDF4 files.

This function will import extract_series to construct your Chlorophyll-a
time series.
'''

import numpy as np


try:
    from extract_pyhdf import extract_series
except ImportError:
    try:
        from extract_gdal import extract_series
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
