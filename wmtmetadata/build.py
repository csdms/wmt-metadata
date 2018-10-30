"""Build and install component metadata on a WMT server."""

import os
import shutil
from scripting.contexts import cd

from wmtmetadata.config import ConfigFromFile, ConfigFromHost
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
