import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import choices_map, units_map


file_list = ['DEM_file']


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

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    env['A_units'] = units_map[env['A_units']]
    env['LINK_FLATS'] = choices_map[env['LINK_FLATS']]
    env['FILL_PITS_IN_Z0'] = choices_map[env['FILL_PITS_IN_Z0']]
    env['LR_PERIODIC'] = choices_map[env['LR_PERIODIC']]
    env['TB_PERIODIC'] = choices_map[env['TB_PERIODIC']]

    for fname in file_list:
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    # src = find_simulation_input_file(env['site_prefix'] + '.rti')
    # shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))
