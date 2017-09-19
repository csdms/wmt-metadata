"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    yaml_dump('_env.yaml', env)
