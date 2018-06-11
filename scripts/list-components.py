"""Prints the names of components installed on a WMT executor."""
import os
import yaml

project_dir=os.path.dirname(os.path.dirname(__file__))
wmt_executor = os.environ['wmt_executor']
cfg_file = os.path.join(project_dir,
                        'wmt-config-{}.yaml'.format(wmt_executor))

try:
    with open(cfg_file, 'r') as fp:
        cfg = yaml.safe_load(fp)
except IOError:
    raise

components = cfg['components'].keys()
for item in components:
    print item
