import os
import shutil

from wmt.utils.hook import find_simulation_input_file


def execute(env):
    """Perform post-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    src = find_simulation_input_file(env['rti_file'])
    shutil.copy(src, os.path.join(os.curdir, env['site_prefix'] + '.rti'))
