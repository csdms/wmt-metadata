"""Prints the names of components installed on a WMT executor."""
import os
import yaml

wmt_executor = os.environ['wmt_executor']
cfg_file = 'wmt-config-' + wmt_executor + '.yaml' 

try:
    with open(cfg_file, 'r') as fp:
        cfg = yaml.safe_load(fp)
except IOError:
    raise

components = cfg['components'].keys()
for item in components:
    print item
