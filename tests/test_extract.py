#!/usr/bin/env python

import tempfile
import os
import glob
import shutil
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import numpy as np
import pytest

try:
    from OceanSound.extract_pyhdf import extract_series as pyhdf_extract
    HAS_PYHDF = True
except ImportError:
    HAS_PYHDF = False

try:
    from OceanSound.extract_gdal import extract_series as gdal_extract
    HAS_GDAL = True
except ImportError:
    HAS_GDAL = False


CONTAINER = "http://41e7942089bad530cb53-26c284b979cc7ba85c89e77b5734ccd5.r9.cf2.rackcdn.com/"

TEST_FILES = (
    "A20021822002212.L3m_MO_CHL_chlor_a_9km",
    "A20022132002243.L3m_MO_CHL_chlor_a_9km"
)


def nan_equal(a, b):
    ''' http://stackoverflow.com/questions/10710328/ '''
    return ((a == b) | (np.isnan(a) & np.isnan(b))).all()


def setup_module(module):
    module.lat, module.lon = 0, 0
    module.indir = tempfile.mkdtemp()

    if not HAS_GDAL and not HAS_PYHDF:
        pytest.skip('You must have PyHDF or GDAL installed!')

    for test_file in TEST_FILES:
        urlretrieve(CONTAINER + test_file, os.path.join(indir, test_file))
    module.pyhdf = pyhdf_extract(lat, lon, indir)
    module.gdal = gdal_extract(lat, lon, indir)


def test_extract(tmpdir):
    assert nan_equal(pyhdf['Series'], gdal['Series'])


def test_len(tmpdir):
    assert len(pyhdf['Series']) == len(gdal['Series'])
    assert len(pyhdf['Series']) == len(glob.glob(os.path.join(indir, 'A*')))


def test_lon(tmpdir):
    assert round(pyhdf['Lon'], 3) == round(gdal['Lon'], 3)


def test_lat(tmpdir):
    assert round(pyhdf['Lat'], 3) == round(gdal['Lat'], 3)


def teardown_module(module):
    shutil.rmtree(module.indir)
