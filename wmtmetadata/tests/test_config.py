"""Unit tests for config module."""

import os
from wmtmetadata.config import Config, ConfigFromFile
from . import data_dir


config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
name = 'Hydrotrend'


def test_config():
    config = Config()
    assert isinstance(config, Config)


def test_configfromfile_hasfile():
    config = ConfigFromFile(config_file)
    assert config.filename == config_file


def test_configfromfile_load():
    config = ConfigFromFile(config_file)
    config.load()
    components = config.components.keys()
    assert components.pop() == name
