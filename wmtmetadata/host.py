"""Get information about the machine hosting a WMT executor."""

import os
import json
from wmtmetadata.server import hosts_dir


class HostInfo(object):

    host_info_file = 'info.json'

    def __init__(self, hostname):
        self.filename = os.path.join(hosts_dir, hostname, 'db',
                                     self.host_info_file)
        self.info = {}

    def load(self):
        with open(self.filename, 'r') as fp:
            self.info = json.load(fp)
