"""Tests for classes in the metadata module."""

import os
from wmtmetadata.config import ConfigFromFile
from wmtmetadata.metadata import Files
from . import data_dir


host = 'siwenna.colorado.edu'
test_config_file = os.path.join(data_dir, 'wmt-config-siwenna.yaml')
name = 'Hydrotrend'
files_file = 'files.json'


def teardown_module():
    if os.path.exists(files_file):
        os.remove(files_file)


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
    assert os.path.isfile(files_file)
