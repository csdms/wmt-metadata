"""Create the metadata files describing a WMT component."""

import os
import json
from wmtmetadata.utils import commonpath


indent = 2


class MetadataBase(object):

    def __init__(self, component):
        self.filename = None
        self.data = None
        self.api = component['api']
        self.files = component['files']
        self.info = component['info']
        self.parameters = component['parameters']
        self.provides = component['provides']
        self.uses = component['uses']

    def write(self):
        with open(self.filename, 'w') as fp:
            json.dump(self.data, fp, indent=indent)


class Files(MetadataBase):
    
    def __init__(self, component):
        super(Files, self).__init__(component)
        self.filename = 'files.json'
        self._prefix = self._get_prefix()
        self.data = []
        for name in self.files:
            self.data.append(name[len(self._prefix):])

    def _get_prefix(self):
        if len(self.files) == 1:
            prefix = os.path.dirname(prefix)
        else:
            prefix = commonpath(self.files)
        prefix += os.path.sep
        return prefix
