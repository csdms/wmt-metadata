"""Unit tests for the host module."""

import os
import pytest
from wmtmetadata.host import HostInfo


host = 'siwenna.colorado.edu'


def test_hostinfo_noargs():
    with pytest.raises(TypeError):
        h = HostInfo()


def test_hostinfo():
    h = HostInfo(host)
    assert isinstance(h, HostInfo)


def test_hostinfo_load():
    h = HostInfo(host)
    h.load()
    assert h.info['name'] == host
