"""Build and install component metadata on a WMT server."""

import os
import shutil
from scripting.contexts import cd

from wmtmetadata.config import ConfigFromFile, ConfigFromHost
from wmtmetadata.metadata import (Files, Info, Uses, Provides,
                                  Parameters)
from wmtmetadata.server import components_dir, tmp_dir
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

    def copy_metadata_files(self, component_name):
        if os.path.exists(component_name):
            shutil.rmtree(component_name)
        src = os.path.join(metadata_dir, component_name)
        dst = os.path.join(os.getcwd(), component_name)
        shutil.copytree(src, dst)

    def build(self, target_dir=components_dir):
        for name, component in self.config.components.items():
            with cd(target_dir):
                self.copy_metadata_files(name)

            for cls in [Files, Info, Uses, Provides, Parameters]:
                c = cls(component)
                with cd(os.path.join(target_dir, name, 'db')):
                    c.write()
