"""A hook for modifying parameter values read from the WMT client."""

import os
from wmt.controllers.models import copy_uploaded_files
from wmt.utils.hook import yaml_dump
from permafrost_benchmark_system.file import (IlambConfigFile,
                                              get_region_labels_txt,
                                              get_region_labels_ncdf)


gfed_region_names = ['global', 'bona', 'tena', 'ceam', 'nhsa', 'shsa',
                     'euro', 'mide', 'nhaf', 'shaf', 'boas', 'ceas',
                     'seas', 'eqas', 'aust']


def load_custom_regions(regions_file):
    """Get a list of custom region labels from a file.

    Parameters
    ----------
    regions_file : str
        The path to an ILAMB custom regions file.

    Returns
    -------
    list
        A list of custom region names.

    """
    try:
        return get_region_labels_ncdf(regions_file)
    except:
        return get_region_labels_txt(regions_file)
    else:
        return []


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

    f = IlambConfigFile(var_list,
                        relationships=has_relationships,
                        title=env['simulation_name'])
    f.setup()
    f.write()

    model_list = []
    for k, v in env.items():
        if k.startswith('_model_') and v == 'On':
            model_list.append(k.lstrip('_model_').encode('utf-8'))
    env['models'] = model_list

    regions = []
    for r in gfed_region_names:
        if env['_region_' + r] == 'On':
            regions.append(r)
    env['regions'] = regions

    if env['_define_regions_file'] != 'Off':
        env['define_regions'] = str(env['_define_regions_file'])
        copy_uploaded_files(env['_model_id'], os.getcwd())
        custom_regions = load_custom_regions(env['define_regions'])
        env['regions'].extend(custom_regions)

    # For debugging.
    env['_sources_file'] = f.sources_file
    env['_var_list'] = var_list
    env['_has_relationships'] = has_relationships
    yaml_dump('_env.yaml', env)
