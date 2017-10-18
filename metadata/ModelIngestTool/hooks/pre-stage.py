"""A hook for modifying parameter values read from the WMT client."""

from wmt.utils.hook import yaml_dump


def execute(env):
    """Perform pre-stage tasks for running a component.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.

    """
    file_list = []
    for k, v in env.items():
        if k.startswith('_ingest_') and v != 'Off':
            file_list.append(v.encode('utf-8'))
    env['ingest_files'] = file_list

    yaml_dump('_env.yaml', env)
