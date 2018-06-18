"""A hook for refreshing a component's metadata."""

from wmt.utils.ssh import get_host_info, open_connection_to_host
from wmt.utils.hook import yaml_dump


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
    yaml_dump('/tmp/files.yaml', pbs_files)

    # Extract model names from file list, removing duplicates.
    models = get_model_names(pbs_files)
    yaml_dump('/tmp/models.yaml', models)
