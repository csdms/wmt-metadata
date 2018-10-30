"""Unit tests for the build module."""

import os
import pytest
from wmtmetadata.build import BuildMetadata
from . import data_dir


sample_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
host = 'siwenna.colorado.edu'
name = 'Hydrotrend'


def test_build_noargs():
    with pytest.raises(ValueError):
        b = BuildMetadata()


def test_build_twoargs():
    with pytest.raises(ValueError):
        b = BuildMetadata(config_file=sample_config_file, hostname=host)


def test_build_fromfile():
    b = BuildMetadata(config_file=sample_config_file)
    components = b.config.components.keys()
    assert components.pop() == name


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_configfromhost_load():
    b = BuildMetadata(hostname=host)
    components = b.config.components.keys()
    assert components.pop() == name
