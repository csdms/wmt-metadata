"""A hook for refreshing a component's metadata."""

import os
import json
from wmt.utils.ssh import get_host_info, open_connection_to_host
from wmt.config import site


hostname = 'siwenna.colorado.edu'
pbs_dir = '/home/csdms/ilamb/MODELS-by-project/PBS'


# Note that I modified info.json to add login credentials.
def get_pbs_listing():
    info = get_host_info(hostname)
    cmd = 'ls {}'.format(pbs_dir)
    ssh = open_connection_to_host(info['name'],
                                  info['username'],
                                  password=info['password'])
    _, stdout, _ = ssh.exec_command(cmd)
    file_list = stdout.readlines()
    ssh.close()
    for i, item in enumerate(file_list):
        file_list[i] = item.rstrip()
    return file_list


def get_model_names(pbs_files):
    names = []
    for pbs_file in pbs_files:
        parts = pbs_file.split('_')
        name = parts[2]
        if name not in names:
            names.append(name)
    return names


def execute(name):
    """Hook called by components/refresh API.

    Parameters
    ----------
    name : str
      The name of the component.

    """

    # Get files listed in MODELS-by-project/PBS directory.
    pbs_files = get_pbs_listing()

    # Extract model names from file list, removing duplicates.
    models = get_model_names(pbs_files)

    # Read the ILAMB parameters.json file.
    parameters_file = os.path.join(site['db'], 'components', name,
                                   'db', 'parameters.json')
    with open(parameters_file, 'r') as fp:
        params = json.load(fp)

    # TODO Add new models to the ILAMB metadata.

    # Write the updated ILAMB parameters.json file.
    # Note that I had to give `a+w` permissions to the file.
    with open(parameters_file, 'w') as fp:
        json.dump(params, fp, indent=4)
