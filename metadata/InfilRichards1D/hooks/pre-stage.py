import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import (assign_parameters, lowercase_choice,
                                 scalar_to_rtg_file)


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
    env['save_profile_dt'] = float(env['dt'])
    env['save_cube_dt'] = float(env['dt'])
    env['n_layers'] = 1  # my choice

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    assign_parameters(env, file_list)

    env['soil_0_type'] = lowercase_choice(env['soil_0_type'])
    env['soil_1_type'] = lowercase_choice(env['soil_1_type'])
    env['soil_2_type'] = lowercase_choice(env['soil_2_type'])

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    src = find_simulation_input_file(env['site_prefix'] + '.rti')
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    for var in ('Ks_val_0', 'Ki_val_0', 'qs_val_0', 'qi_val_0', 'qr_val_0', 
                'pB_val_0', 'pA_val_0', 'lam_val_0', 'c_val_0', 'Ks_val_1',
                'Ki_val_1', 'qs_val_1', 'qi_val_1', 'qr_val_1', 'pB_val_1',
                'pA_val_1', 'lam_val_1', 'c_val_1', 'Ks_val_2', 'Ki_val_2',
                'qs_val_2', 'qi_val_2', 'qr_val_2', 'pB_val_2', 'pA_val_2',
                'lam_val_2', 'c_val_2'):
        if env[var + '_ptype'] == 'Scalar':
            scalar_to_rtg_file(var, env)
