"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump
from permafrost_benchmark_system.file import IlambConfigFile


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    cmip5_vars = []
    for k, v in env.items():
        if k.startswith('_variable') and v != '':
            cmip5_vars.append(str(v))
    f = IlambConfigFile(cmip5_vars)
    f.setup()
    f.write()

    # For debugging.
    env['_sources_file'] = f.sources_file
    env['_cmip5_vars'] = cmip5_vars
    yaml_dump('_env.yaml', env)
