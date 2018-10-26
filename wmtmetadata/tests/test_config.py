"""Unit tests for the config module."""

import os
from wmtmetadata.config import Config, ConfigFromFile, ConfigFromHost
from wmtmetadata.host import HostInfo
from . import data_dir


config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
host = 'siwenna.colorado.edu'
name = 'Hydrotrend'


def test_config():
    config = Config()
    assert isinstance(config, Config)


def test_configfromfile():
    config = ConfigFromFile(config_file)
    assert config.filename == config_file


def test_configfromfile_load():
    config = ConfigFromFile(config_file)
    config.load()
    components = config.components.keys()
    assert components.pop() == name


def test_configfromhost():
    config = ConfigFromHost(host)
    assert config.host.info['name'] == host


def test_configfromhost_build():
    config = ConfigFromHost(host)
    config.build_on_host()
