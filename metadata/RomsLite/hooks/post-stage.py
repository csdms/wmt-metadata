import os
import shutil

from wmt.utils.hook import find_simulation_input_file


_DEFAULT_FILES = {
    'river_forcing_file': 'river.nc',
    'waves_forcing_file': 'waves.nc',
}

def execute(env):
    """Perform post-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    for name in _DEFAULT_FILES:
        if env[name] != _DEFAULT_FILES[name]:
            try:
                os.remove(os.path.join(os.curdir, 'Forcing', env[name]))
            except OSError:
                pass

        src = find_simulation_input_file(env[name])
        shutil.copy(src, os.path.join(os.curdir, 'Forcing'))
