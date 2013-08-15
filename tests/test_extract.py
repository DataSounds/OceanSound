#!/usr/bin/env python

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


from OceanSound.extract_pyhdf import extract_series as pyhdf_extract
from OceanSound.extract_gdal import extract_series as gdal_extract


CONTAINER = "http://41e7942089bad530cb53-26c284b979cc7ba85c89e77b5734ccd5.r9.cf2.rackcdn.com/"

TEST_FILES = (
  "A20021822002212.L3m_MO_CHL_chlor_a_9km",
  "A20022132002243.L3m_MO_CHL_chlor_a_9km"
)


def test_extract(tmpdir):
    lat, lon = 0, 0
    indir = str(tmpdir)
    for test_file in TEST_FILES:
        urlretrieve(CONTAINER + test_file, str(tmpdir.join(test_file)))
    assert pyhdf_extract(lat, lon, indir) == gdal_extract(lat, lon, indir)

def test_extracted(tmpdir):
    lat, lon = 0, 0
    indir = str(tmpdir)
    for test_file in TEST_FILES:
        urlretrieve(CONTAINER + test_file, str(tmpdir.join(test_file)))
    a_pyhdf = pyhdf_extract(lat, lon, indir)
    a_gdal = gdal_extract(lat, lon, indir)
    assert len(a_pyhdf['Series']) == len(TEST_FILES) == len(a_gdal['Series'])
