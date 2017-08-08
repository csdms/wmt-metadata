"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump
from topoflow_utils.hook import assign_parameters


file_list = []


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    env['model_end_year'] = long(env['model_start_year']) \
                            + long(env['_run_duration'])

    assign_parameters(env, file_list)

    env['_file_list'] = file_list
    yaml_dump('_env.yaml', env)
