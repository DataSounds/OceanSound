#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
subset_MODIS using gdal package.

Makes a subset of a pixel time series from MODIS
Chlorophyll images.

"""

import gdal


def open_file(filename):
    A = gdal.Open(filename, gdal.GA_ReadOnly)
    pin = A.GetMetadata()

    return A, pin


def extract_point(dataset, ilt, ilg):
    return dataset.ReadAsArray()[ilt, ilg]
