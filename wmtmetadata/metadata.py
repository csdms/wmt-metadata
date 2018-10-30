"""Create the metadata files describing a WMT component."""

import os
import re
import fnmatch
import warnings
import collections
import json
import yaml
from wmtmetadata.utils import commonpath
from wmtmetadata import metadata_dir


class MetadataBase(object):

    indent = 2

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
            json.dump(self.data, fp, indent=self.indent)
        if self.filename == 'parameters.json':
            os.chmod(self.filename, 0666)


class Files(MetadataBase):
    
    def __init__(self, component):
        super(Files, self).__init__(component)
        self.filename = 'files.json'
        self.prefix = self._get_prefix()
        self.data = []
        for name in self.files:
            self.data.append(name[len(self.prefix):])

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


def section_break(title):
    return {
        'key': 'separator',
        'name': title,
        'description': title,
        'value': {
            'type': 'string',
            'default': '',
        }
    }


def old_style_parameter(name, param):
    return {
        'key': name,
        'name': param['description'],
        'description': param['description'],
        'value': param['value'],
        'visible': param.get('visible', True),
        'global': param.get('global', False)
    }


class Parameters(MetadataBase):

    def __init__(self, component):
        super(Parameters, self).__init__(component)
        self.filename = 'parameters.json'
        self.data = []
        self.load_component_config()

        if len(self.provides) > 0:
            self.add_outputs()

        if self.component_config.has_key('extras'):
            self.parameters.update(self.component_config['extras'])

        if self.component_config.has_key('ignore'):
            self._hide_ignored()

        if self.component_config.has_key('globals'):
            driver = section_break('Globals')
            driver['global'] = True
            self.data.append(driver)
            for name in self.component_config.get('globals', []):
                if name in self.parameters.keys():
                    self.parameters[name]['global'] = True

        self.make_sections()
        self.make_groups()
        self.make_mappers()

    def _hide_ignored(self):
        ignored = []
        for pattern in self.component_config['ignore']:
            p = re.compile(fnmatch.translate(pattern))
            ignored.extend(filter(p.match, params))

        for name in ignored:
            if name in self.parameters:
                self.parameters[name]['visible'] = False
            else:
                if name not in self.parameters.keys():
                    msg = '{name}: pattern not in params'.format(name)
                    warnings.warn(msg)

    def make_sections(self):
        added = set()

        for name in self.parameters.keys():
            if self.parameters[name].has_key('global') and \
               self.parameters[name]['global'] is True:
                try:
                    self.data.append(
                        old_style_parameter(name, self.parameters[name]))
                except KeyError:
                    warnings.warn('{}: missing parameter'.format(name))
                else:
                    added.add(name)

        for section in self.component_config.get('sections', []):
            self.data.append(section_break(section['title']))
            for member in section['members']:
                try:
                    self.data.append(
                        old_style_parameter(member, self.parameters[member]))
                except KeyError:
                    warnings.warn('{}: missing parameter'.format(name))
                else:
                    added.add(member)

        missing = set(self.parameters.keys()) - added
        if len(missing) > 0:
            for name in missing:
                self.parameters[name]['visible'] = False
                self.data.append(
                    old_style_parameter(name, self.parameters[name]))

    def make_groups(self):
        groups = self.component_config.get('groups', {})
        for name, members in groups.items():
            for item in self.data:
                if item['key'] in members:
                    item['group'] = {
                        "name": name,
                        "leader": item['key'] == members[0],
                        "members": len(members),
                    }

    def _get_mapped_parameters(self, roles):
        mapped_params = [roles['selector']]
        for mapping in roles['selections']:
            param = mapping.values()[0]
            try:
                mapped_params.index(param)
            except ValueError:
                mapped_params.append(param)
        return mapped_params

    def _get_mappings(self, selections):
        mappings = collections.OrderedDict()
        for mapping in selections:
            for ptype, param in mapping.items():
                mappings[ptype] = param
        return mappings

    def make_mappers(self):
        mappers = self.component_config.get('parameter_mappers', {})
        for mapper, roles in mappers.items():
            mapped_params = self._get_mapped_parameters(roles)
            for item in self.data:
                if item['key'] in mapped_params:
                    item['selection'] = {
                        'name': mapper,
                        'selector': roles['selector'] == item['key'],
                        'members': len(mapped_params),
                        }
                    if item['selection']['selector'] is True:
                        item['selection']['mapping'] = \
                            self._get_mappings(roles['selections'])

    def add_outputs(self):
        print_section = {
            'title': 'Output files',
            'members': [],
        }

        for name in self.provides:
            self.parameters[name] = {
                'description': name,
                'value': {
                    'type': 'choice',
                    'default': 'off',
                    'choices': [
                        'off',
                        name
                    ]
                }
            }
            print_section['members'].append(name)

        self.component_config['sections'].append(print_section)
