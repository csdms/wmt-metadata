import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import assign_parameters, scalar_to_rtg_file


# file_list = ['flow_grid_file', 'pixel_file']
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
    env['n_layers'] = 3  # my choice

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    assign_parameters(env, file_list)

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    # src = find_simulation_input_file(env['site_prefix'] + '.rti')
    # shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))
    src = find_simulation_input_file(env['flow_grid_file'])
    env['flow_grid_file'] = env['site_prefix'] + '_flow.rtg'
    shutil.copy(src, os.path.join(os.curdir, env['flow_grid_file']))

    src = find_simulation_input_file(env['rti_file'])
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    for var in ('elev', 'h0_table', 'd_freeze', 'd_thaw', 'Ks_0', 'qs_0',
                'th_0', 'Ks_1', 'qs_1', 'th_1', 'Ks_2', 'qs_2', 'th_2'):
        if env[var + '_ptype'] == 'Scalar':
            scalar_to_rtg_file(var, env)

