"""A hook for refreshing a component's metadata."""

import os
import subprocess
import json
from wmt.utils.ssh import get_host_info, open_connection_to_host
from wmt.config import site
import pbs_server.models as models
import pbs_server.variables as variables


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


def update_models(params):
    """Updates ILAMB metadata for model outputs uploaded through the PBS.

    Parameters
    ----------
    params : list
      The WMT parameters for the ILAMB component.

    """
    models_files = get_pbs_listing(models_dir)

    # Extract model names from file list and sort, removing duplicates.
    model_list = []
    for pbs_file in models_files:
        model_name = models.get_name(pbs_file)
        if model_name not in model_list:
            model_list.append(model_name)
    model_list.sort()

    models.update_parameters(params, model_list)


def update_variables(params):
    """Updates ILAMB metadata for benchmark data uploaded through the PBS.

    Parameters
    ----------
    params : list
      The WMT parameters for the ILAMB component.

    """
    data_files = get_pbs_listing(data_dir)

    # Extract variable names from file list, removing duplicates.
    variable_dict = {}
    for pbs_file in data_files:
        variable_name = variables.get_name(pbs_file)
        if variable_name not in variable_dict.keys():
            variable_dict[variable_name] = pbs_file

    variables.update_parameters(params, variable_dict.keys())

    # Create or update the .cfg.tmpl file for each variable.
    for var_name, file_name in variable_dict.items():
        variables.update_template(var_name, file_name)


def execute(name):
    """Hook called by components/refresh API.

    Parameters
    ----------
    name : str
      The name of the component (here, 'ILAMB').

    """
    parameters_file = os.path.join(site['db'], 'components', name,
                                   'db', 'parameters.json')
    with open(parameters_file, 'r') as fp:
        params = json.load(fp)

    update_models(params)
    update_variables(params)

    # Note that I had to give `a+w` permissions to the parameters file.
    with open(parameters_file, 'w') as fp:
        json.dump(params, fp, indent=4)

    # Touch the wsgi script so the WMT client reads the changes.
    # I had to change the permissions to `a+w` on the wsgi script.
    # And also add site['bin'].
    script_path = os.path.join(site['bin'], 'wmt_wsgi_main.py')
    r = subprocess.call(['touch', script_path])
