import os
import glob
from wmt.utils.hook import yaml_dump


def execute(env):
    hyps_files = glob.glob('*.hyps')
    for f in hyps_files:
        os.remove(f)

    # For debugging
    yaml_dump('_env_post.yaml', env)
