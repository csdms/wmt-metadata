"""A hook for refreshing a component's metadata."""

import os
import subprocess
import json
from wmt.utils.ssh import get_host_info, open_connection_to_host
from wmt.config import site


hostname = 'siwenna.colorado.edu'
pbs_dir = '/home/csdms/ilamb/MODELS-by-project/PBS'
model_template = { "group": { "name": "pbs_models_group", "members":
    1, "leader": False }, "name": "{model_name}", "global": False,
    "value": { "default": "Off", "type": "choice", "choices": [ "On",
    "Off" ] }, "visible": True, "key": "_model_{model_name}",
    "description": "{model_name}" }


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


def key_in_pbs_group(key, parameters):
    for param in parameters:
        if 'group' in param.keys():
            if param['group']['name'] == 'pbs_models_group':
                if param['key'] == key:
                    return True
    return False


def update_parameters(parameters, models):
    for index, param in enumerate(parameters):
        if param['key'] == '_pbs_models':
            pbs_group_header = param
            pbs_group_index = index

    for model in models:
        key = '_model_{}'.format(model)
        if not key_in_pbs_group(key, parameters):
            entry = model_template.copy()
            entry['key'] = key
            entry['name'] = model
            entry['description'] = model
            pbs_group_header['group']['members'] += 1
            pbs_group_index += 1
            parameters.insert(pbs_group_index, entry)


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
    models.sort()

    # Read the ILAMB parameters.json file.
    parameters_file = os.path.join(site['db'], 'components', name,
                                   'db', 'parameters.json')
    with open(parameters_file, 'r') as fp:
        params = json.load(fp)

    # Add new models to the ILAMB metadata.
    update_parameters(params, models)

    # Write the updated ILAMB parameters.json file.
    # Note that I had to give `a+w` permissions to the file.
    with open(parameters_file, 'w') as fp:
        json.dump(params, fp, indent=4)

    # Touch the wsgi script so the client reads the changes.
    # I had to change the permissions to `a+w` on the wsgi script.
    # And also add site['bin'].
    script_path = os.path.join(site['bin'], 'wmt_wsgi_main.py')
    r = subprocess.call(['touch', script_path])
