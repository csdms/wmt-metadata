"""Configuration information for a remote WMT executor."""

import yaml


class Config(object):

    def __init__(self):
        self.filename = None
        self.components = {}

    def load(self):
        with open(self.filename, 'r') as fp:
            _cfg = yaml.load(fp)
        self.components = _cfg['components']


class ConfigFromFile(Config):
    
    def __init__(self, filename='wmt-config-siwenna.yaml'):
        super(ConfigFromFile, self).__init__()
        self.filename = filename
