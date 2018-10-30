"""Build and install component metadata on a WMT server."""

import os
import shutil
from scripting.contexts import cd

from wmtmetadata.config import ConfigFromFile, ConfigFromHost
from wmtmetadata.metadata import (Files, Info, Uses, Provides,
                                  Parameters)
from wmtmetadata.host import HostInfo
from wmtmetadata.server import components_dir, tmp_dir
from wmtmetadata.ssh import open_connection
from wmtmetadata import metadata_dir


class BuildMetadata(object):

    def __init__(self, hostname=None, config_file=None):
        if hostname is not None and config_file is not None:
            raise ValueError('Only one of hostname or config_file is allowed')

        if config_file is not None:
            self.config = ConfigFromFile(config_file)
        elif hostname is not None:
            self.config = ConfigFromHost(hostname)
            self.config.build()
            self.config.fetch(local_dir=tmp_dir)
        else:
            raise ValueError('Must supply config file or hostname')

        self.config.load()
        self.get_executor_info()

    def get_executor_info(self):
        try:
            self.config.executor
        except AttributeError:
            self.config.executor = HostInfo(self.config.host['hostname'])
            self.config.executor.load()

    def copy_metadata_files(self, component_name):
        if os.path.exists(component_name):
            shutil.rmtree(component_name)
        src = os.path.join(metadata_dir, component_name)
        dst = os.path.join(os.getcwd(), component_name)
        shutil.copytree(src, dst)

    def build(self, target_dir=components_dir, username=None,
              password=None, single_component=None):
        if username is None:
            username = self.config.executor.info['username']
        if password is None:
            password = self.config.executor.info['password']

        for name, component in self.config.components.items():
            if single_component is not None:
                if single_component != name:
                    continue
            with cd(target_dir):
                self.copy_metadata_files(name)

            for cls in [Files, Info, Uses, Provides, Parameters]:
                c = cls(component)
                with cd(os.path.join(target_dir, name, 'db')):
                    c.write()

            datadir = Files(component).prefix
            ssh = open_connection(self.config.executor.info['name'],
                                  username, password)
            sftp = ssh.open_sftp()
            remote_files = sftp.listdir(path=datadir)

            with cd(os.path.join(target_dir, name, 'files')):
                for f in remote_files:
                    sftp.get(os.path.join(datadir, f), f)

            ssh.close()
