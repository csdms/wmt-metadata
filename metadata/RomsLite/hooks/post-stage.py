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
    for name in ('river_forcing_file', 'ocean_forcing_file'):
        src = find_simulation_input_file(env[name])
        shutil.copy(src, os.path.join(os.curdir, 'Forcing'))
