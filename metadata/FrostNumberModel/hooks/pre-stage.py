"""A hook for modifying parameter values read from the WMT client."""

import os
import shutil

from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import assign_parameters


file_list = []


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    assign_parameters(env, file_list)
    env['fn_out_filename'] = 'frostnumber_output.dat'

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
