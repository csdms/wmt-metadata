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
    env['model_end_date'] = long(env['model_start_date']) \
                            + long(env['_run_duration'])

    env['input_var_source'] = 'WMT'
    env['output_filename'] = 'FrostNumberGeo_output.nc'

    # Todo: Remove these hooks when methods are implemented.
    env['degree_days_method'] = 'MinJanMaxJul'  # will become a choice
    env['n_precipitation_grid_fields'] = 0
    env['n_soilproperties_grid_fields'] = 0
    env['calc_surface_frostnumber'] = False
    env['calc_stefan_frostnumber'] = False

    # XXX: This is my choice for implementing in WMT.
    env['n_temperature_grid_fields'] = 1

    assign_parameters(env, file_list)

    env['_file_list'] = file_list
    yaml_dump('_env.yaml', env)
