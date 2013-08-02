#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Chooses package between pyhdf and gdal to deal with HDF4 files.

This function will import extract_series to construct your Chlorophyll-a
time series.
'''

try:
    from extract_pyhdf import extract_series
except ImportError:
    try:
        from extract_gdal import extract_series
    except ImportError:
        print("You must have installed pyhdf or gdal package")
