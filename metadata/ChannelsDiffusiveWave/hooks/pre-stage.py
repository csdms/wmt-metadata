import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
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
    env['n_steps'] = int(round(float(env['_run_duration']) / float(env['dt'])))
    env['save_grid_dt'] = float(env['dt'])
    env['save_pixels_dt'] = float(env['dt'])

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    # Translate the roughness choice to TopoFlow flags.
    env['MANNING'] = env['roughness_option'].startswith('Manning') * 1
    env['LAW_OF_WALL'] = 1 - env['MANNING']

    assign_parameters(env, file_list)

    # for fname in ['code_file', 'slope_file'] + file_list:
    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    # src = find_simulation_input_file(env['site_prefix'] + '.rti')
    # shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    src = find_simulation_input_file(env['code_file'])
    env['code_file'] = env['site_prefix'] + '_flow.rtg'
    shutil.copy(src, os.path.join(os.curdir, env['code_file']))

    src = find_simulation_input_file(env['slope_file'])
    env['slope_file'] = env['site_prefix'] + '_slope.rtg'
    shutil.copy(src, os.path.join(os.curdir, env['slope_file']))

    src = find_simulation_input_file(env['rti_file'])
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    for var in ('width', 'angle', 'roughness', 'd0', 'sinu'):
        if env[var + '_ptype'] == 'Scalar':
            scalar_to_rtg_file(var, env)

    for var in ('nval', 'z0val'):
        env[var + '_ptype'] = env['roughness_ptype']
        env[var + '_dtype'] = env['roughness_dtype']
        env[var] = env['roughness']
        env[var + '_file'] = env['roughness_file']

    # env['update_time_step'] = float(env['dt']) * float(env['update_time_step'])
    # env['output_interval'] = float(env['dt']) * float(env['output_interval'])
