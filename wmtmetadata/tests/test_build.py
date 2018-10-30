"""Unit tests for the build module."""

import os
import pytest
from wmtmetadata.build import BuildMetadata
from . import data_dir


sample_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
host = 'siwenna.colorado.edu'
name = 'Hydrotrend'
tmp_dir = '/tmp'


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


def test_build_fromfile_hazexecutor():
    b = BuildMetadata(config_file=sample_config_file)
    assert hasattr(b.config, 'executor')


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_build_fromhost():
    b = BuildMetadata(hostname=host)
    components = b.config.components.keys()
    assert components.pop() == name


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_build_fromhost_hazexecutor():
    b = BuildMetadata(hostname=host)
    assert hasattr(b.config, 'executor')


def test_build_build():
    b = BuildMetadata(config_file=sample_config_file)
    b.build(target_dir=tmp_dir)
    assert os.path.isfile(os.path.join(tmp_dir, name, 'wmt.yaml'))
    assert os.path.isfile(os.path.join(tmp_dir, name, 'db', 'info.json'))
