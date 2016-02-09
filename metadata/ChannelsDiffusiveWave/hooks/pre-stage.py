import os
import shutil

from wmt.config import site
from wmt.models.submissions import prepend_to_path
from wmt.utils.hook import find_simulation_input_file
from topoflow_utils.hook import assign_parameters


# file_list = ['rti_file',
#              'code_file',
#              'slope_file',
#              'pixel_file']
file_list = []


def load_rti(name):
    lines = []
    with open(name, 'r') as fp:
        for line in fp:
            if ';' in line:
                line = line[:line.find(';')]
            if ':' in line:
                lines.append(line)

    return yaml.load(os.linesep.join(lines))


def scalar_to_rtg_file(name, env):
    env[name + '_ptype'] = 'Grid'
    env[name + '_dtype'] = 'string'
    file_name = env['case_prefix'] + '_{name}.rtg'.format(name=name)

    rti = load_rti(env['site_prefix'] + '.rti')
    shape = (rti['Number of rows'], rti['Number of columns'])
    byte_order = rti['Byte order']
    if byte_order == 'MSB':
        dtype = '>f4'
    else:
        dtype = '<f4'
    grid = np.full(shape, env[name], dtype=dtype)
    grid.tofile(file_name)

    env[name] = env[name + '_file'] = file_name


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

    # TopoFlow needs site_prefix and case_prefix.
    # env['site_prefix'] = os.path.splitext(env['rti_file'])[0]
    # env['case_prefix'] = 'WMT'

    # If no pixel_file is given, let TopoFlow make one.
    if env['pixel_file'] == 'off':
        # file_list.remove('pixel_file')
        env['pixel_file'] = env['case_prefix'] + '_outlets.txt'

    # Translate the roughness choice to TopoFlow flags.
    env['MANNING'] = env['roughness_option'].startswith('Manning') * 1
    env['LAW_OF_WALL'] = 1 - env['MANNING']

    env['nval_ptype'] = env['z0val_ptype'] = env['roughness_ptype']
    # env['nval_scalar'] = env['z0val_scalar'] = env['roughness_scalar']
    env['nval'] = env['z0val'] = env['roughness']
    env['nval_file'] = env['z0val_file'] = env['roughness_file']    

    assign_parameters(env, file_list)

    # Default files common to all TopoFlow components are stored with the
    # topoflow component metadata.
    # prepend_to_path('WMT_INPUT_FILE_PATH',
    #                 os.path.join(site['db'], 'components', 'topoflow', 'files'))
    for fname in ('code_file', 'slope_file'):
        src = find_simulation_input_file(env[fname])
        shutil.copy(src, os.curdir)
    src = find_simulation_input_file(env[fname])
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))

    if env['width_ptype'] == 'Scalar':
        scalar_to_rtg_file('width', env)
    if env['angle_ptype'] == 'Scalar':
        scalar_to_rtg_file('angle', env)
