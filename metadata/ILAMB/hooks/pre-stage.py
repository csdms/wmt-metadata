"""A hook for modifying parameter values read from the WMT client."""
from wmt.utils.hook import yaml_dump
from permafrost_benchmark_system.file import IlambConfigFile


region_names = ['global', 'bona', 'tena', 'ceam', 'nhsa', 'shsa',
                'euro', 'mide', 'nhaf', 'shaf', 'boas', 'ceas',
                'seas', 'eqas', 'aust']


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    var_list = []
    for k, v in env.items():
        if k.startswith('_variable') and v != '':
            var_list.append(str(v))

    has_relationships = (env['_relationships'] == 'Yes') and \
                        (len(var_list) > 1)

    f = IlambConfigFile(var_list, relationships=has_relationships)
    f.setup()
    f.write()

    regions = []
    for r in region_names:
        if env['_region_' + r] == 'On':
            regions.append(r)
    env['regions'] = regions

    # For debugging.
    env['_sources_file'] = f.sources_file
    env['_var_list'] = var_list
    env['_has_relationships'] = has_relationships
    yaml_dump('_env.yaml', env)
