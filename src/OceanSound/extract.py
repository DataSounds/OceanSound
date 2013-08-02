#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
subset_MODIS

Makes a subset of a pixel time series from MODIS 
Chlorophyll images.

'''

try:
    from extract_pyhdf import extract_serie
except ImportError:
    try:
        from extract_gdal import extract_series
    except ImportError:
        print("You must have installed pyhdf or gdal package")
