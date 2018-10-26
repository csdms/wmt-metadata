"""Tests for classes in the metadata module."""

import os
from wmtmetadata.config import ConfigFromFile
from wmtmetadata.metadata import Files, Info
from . import data_dir


host = 'siwenna.colorado.edu'
test_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
name = 'Hydrotrend'
files = {
    'files_file': 'files.json',
    'info_file': 'info.json'
    }


def teardown_module():
    for k, v in files.items():
        if os.path.exists(v):
            os.remove(v)


def test_files():
    config = ConfigFromFile(test_config_file)
    config.load()
    f = Files(config.components[name])
    assert f.data[0] == 'HYDRO.IN'


def test_files_write():
    config = ConfigFromFile(test_config_file)
    config.load()
    f = Files(config.components[name])
    f.write()
    assert os.path.isfile(files['files_file'])


def test_info():
    config = ConfigFromFile(test_config_file)
    config.load()
    n = Info(config.components[name])
    assert n.data['id'] == name


def test_info_write():
    config = ConfigFromFile(test_config_file)
    config.load()
    n = Info(config.components[name])
    n.write()
    assert os.path.isfile(files['info_file'])
