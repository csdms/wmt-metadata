import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import (assign_parameters, lowercase_choice,
                                 scalar_to_rtg_file)


file_list = [] # ['pixel_file']


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['n_steps'] = int(round(float(env['run_duration']) / float(env['dt'])))
    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])
    env['n_layers'] = 1  # my choice

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    assign_parameters(env, file_list)

    env['soil_type_0'] = lowercase_choice(env['soil_type_0'])

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    src = find_simulation_input_file(env['site_prefix'] + '.rti')
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    for var in ('Ks_0', 'Ki_0', 'qs_0', 'qi_0', 'G_0'):
        if env[var + '_ptype'] == 'Scalar':
            scalar_to_rtg_file(var, env)
