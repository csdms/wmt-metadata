"""Tests for classes in the metadata module."""

import os
from wmtmetadata.config import ConfigFromFile
from wmtmetadata.metadata import Files, Info, Uses, Provides
from . import data_dir


host = 'siwenna.colorado.edu'
test_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
name = 'Hydrotrend'
files = {
    'files_file': 'files.json',
    'info_file': 'info.json',
    'uses_file': 'uses.json',
    'provides_file': 'provides.json',
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


def test_uses():
    config = ConfigFromFile(test_config_file)
    config.load()
    u = Uses(config.components[name])
    assert u.data == []


def test_uses_write():
    config = ConfigFromFile(test_config_file)
    config.load()
    u = Uses(config.components[name])
    u.write()
    assert os.path.isfile(files['uses_file'])


def test_provides():
    config = ConfigFromFile(test_config_file)
    config.load()
    u = Provides(config.components[name])
    assert u.data[0]['id'] == 'discharge'


def test_provides_write():
    config = ConfigFromFile(test_config_file)
    config.load()
    u = Provides(config.components[name])
    u.write()
    assert os.path.isfile(files['provides_file'])
