#!/usr/bin/env python

import pytest

pytest.main("--cov src/OceanSound --cov-report xml --cov-report term-missing --junitxml=tests.xml")
