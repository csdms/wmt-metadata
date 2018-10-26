"""Get information about the machine hosting a WMT executor."""

import os
import sys
import json


class HostInfo(object):

    prefix = os.path.dirname(sys.prefix)

    def __init__(self, hostname):
        self.filename = os.path.join(self.prefix, 'db', 'hosts',
                                     hostname, 'db', 'info.json')
        self.info = {}

    def load(self):
        with open(self.filename, 'r') as fp:
            self.info = json.load(fp)
