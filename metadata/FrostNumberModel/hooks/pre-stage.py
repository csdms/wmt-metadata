"""A hook for modifying parameter values read from the WMT client."""

import os
import shutil

from wmt.utils.hook import find_simulation_input_file, yaml_dump
from topoflow_utils.hook import assign_parameters


file_list = []


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['end_year'] = long(env['start_year']) + long(env['_run_duration']) - 1
    env['fn_out_filename'] = 'frostnumber_output.dat'

    assign_parameters(env, file_list)

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)

    env['_file_list'] = file_list
    yaml_dump('_env.yaml', env)
