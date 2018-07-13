"""A hook for refreshing a component's metadata."""

import os
import subprocess
import json
from wmt.utils.ssh import get_host_info, open_connection_to_host
from wmt.config import site
from pbs_server.models import get_model_name, update_parameters
from pbs_server.variables import get_variable_name


hostname = 'siwenna.colorado.edu'
models_dir = '/home/csdms/ilamb/MODELS-by-project/PBS'
data_dir = '/home/csdms/ilamb/DATA-by-project/PBS'


# Note that I modified info.json to add login credentials.
def get_pbs_listing(pbs_dir):
    """
    Get a listing of model outputs or benchmark data uploaded through the PBS.

    Parameters
    ----------
    pbs_dir : str
      The path to the directory of uploaded PBS files.

    Returns
    -------
    list
      A list of uploaded model output files.

    """
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


def execute(name):
    """Hook called by components/refresh API.

    Parameters
    ----------
    name : str
      The name of the component.

    """

    # Get names of files uploaded through the PBS.
    models_files = get_pbs_listing(models_dir)
    data_files = get_pbs_listing(data_dir)

    # Extract model names from file list, removing duplicates.
    models = []
    for pbs_file in models_files:
        model_name = get_model_name(pbs_file)
        if model_name not in models:
            models.append(model_name)
    models.sort()

    # Extract variable names from file list, removing duplicates.
    variables = []
    for pbs_file in data_files:
        variable_name = get_variable_name(pbs_file)
        if variable_name not in variables:
            variables.append(variable_name)
    variables.sort()

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
