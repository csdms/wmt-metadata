"""A hook for modifying parameter values read from the WMT client."""

import os
from wmt.models.models import get_model_upload_dir
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

    f = IlambConfigFile(var_list, relationships=has_relationships)
    f.setup()
    f.write()

    regions = []
    for r in gfed_region_names:
        if env['_region_' + r] == 'On':
            regions.append(r)
    env['regions'] = regions

    if env['_define_regions_file'] != 'Off':
        env['define_regions'] = str(env['_define_regions_file'])
        upload_dir = get_model_upload_dir(env['_model_id'])
        regions_file = os.path.join(upload_dir, env['define_regions'])
        custom_regions = load_custom_regions(regions_file)
        env['regions'].extend(custom_regions)

    # For debugging.
    env['_sources_file'] = f.sources_file
    env['_var_list'] = var_list
    env['_has_relationships'] = has_relationships
    yaml_dump('_env.yaml', env)
