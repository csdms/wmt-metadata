import os
import shutil

from wmt.config import site
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import assign_parameters, scalar_to_rtg_file


file_list = []


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

    assign_parameters(env, file_list)

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    src = find_simulation_input_file(env['site_prefix'] + '.rti')
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    for var in ('rho_snow', 'c0', 'T0', 'h0_snow', 'h0_swe'):
        if env[var + '_ptype'] == 'Scalar':
            scalar_to_rtg_file(var, env)
