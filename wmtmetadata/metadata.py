"""Create the metadata files describing a WMT component."""

import os
import re
import fnmatch
import warnings
import json
import yaml
from wmtmetadata.utils import commonpath
from wmtmetadata import metadata_dir


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
        self.component_config_file = os.path.join(metadata_dir,
                                                  self.api['class'],
                                                  'wmt.yaml')
        self.component_config = None

    def load_component_config(self):
        with open(self.component_config_file, 'r') as fp:
            self.component_config = yaml.load(fp)

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


class Info(MetadataBase):
    
    def __init__(self, component):
        super(Info, self).__init__(component)
        self.filename = 'info.json'
        self.data = self.info.copy()
        for key in ['id', 'name', 'class']:
            self.data[key] = self.api['class']
        try:
            self.data['initialize_args'] = self.api['initialize_args']
        except KeyError:
            warnings.warn('missing initialize_args')
            self.data['initialize_args'] = ''


class Ports(MetadataBase):

    def __init__(self, component):
        super(Ports, self).__init__(component)
        self.data = []
        self.load_component_config()

    def load(self):
        port_type = type(self).__name__.lower()
        port = self.component_config.get(port_type, [])
        for name in port:
            names = []
            for pattern in port[name]['exchange_items']:
                p = re.compile(fnmatch.translate(pattern))
                names.extend(filter(p.match, getattr(self, port_type)))

            self.data.append({
                'id': name,
                'required': port[name]['required'],
                'exchange_items': names,
            })


class Uses(Ports):

    def __init__(self, component):
        super(Uses, self).__init__(component)
        self.filename = 'uses.json'
        self.load()


class Provides(Ports):

    def __init__(self, component):
        super(Provides, self).__init__(component)
        self.filename = 'provides.json'
        self.load()
