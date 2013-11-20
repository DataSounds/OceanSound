#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
subset_MODIS using pyhdf package.

Makes a subset of a pixel time series from MODIS
Chlorophyll images.

"""

from pyhdf.SD import SD


def open_file(filename):
    A = SD(filename)

    # retrieve data SDS
    d = A.datasets()
    sds_name = d.keys()[0]  # name of sds. Dictionary method.
    sds = A.select(sds_name)
    pin = A.attributes()

    return sds, pin


def extract_point(sds, ilt, ilg):
    return sds[ilt, ilg]
