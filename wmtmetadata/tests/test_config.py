"""Unit tests for the config module."""

import os
import pytest
from wmtmetadata.config import Config, ConfigFromFile, ConfigFromHost
from wmtmetadata.host import HostInfo
from . import data_dir


tmp_dir = '/tmp'
sample_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
host = 'siwenna.colorado.edu'
name = 'Hydrotrend'
fetched_config_file = 'wmt-config-{}.yaml'.format(host)


def test_config():
    config = Config()
    assert isinstance(config, Config)


def test_configfromfile():
    config = ConfigFromFile(sample_config_file)
    assert config.filename == sample_config_file


def test_configfromfile_load():
    config = ConfigFromFile(sample_config_file)
    config.load()
    components = config.components.keys()
    assert components.pop() == name


def test_configfromhost():
    config = ConfigFromHost(host)
    assert config.host.info['name'] == host


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_configfromhost_build():
    config = ConfigFromHost(host)
    config.build()


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_configfromhost_fetch():
    config = ConfigFromHost(host)
    config.fetch(local_dir=tmp_dir)
    assert os.path.isfile(os.path.join(tmp_dir, fetched_config_file))


@pytest.mark.skip(reason="Don't abuse remote test machine")
def test_configfromhost_load():
    config = ConfigFromHost(host)
    config.build()
    config.fetch(local_dir=tmp_dir)
    config.load()
    components = config.components.keys()
    assert components.pop() == name
