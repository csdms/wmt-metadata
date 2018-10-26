"""Configuration information for a remote WMT executor."""

import os
import yaml
from wmtmetadata.ssh import open_connection
from wmtmetadata.host import HostInfo
from wmtmetadata import top_dir


class Config(object):

    def __init__(self):
        self.filename = None
        self.components = {}

    def load(self):
        with open(self.filename, 'r') as fp:
            _cfg = yaml.load(fp)
        self.components = _cfg['components']


class ConfigFromFile(Config):
    
    def __init__(self, filename='wmt-config-siwenna.yaml'):
        super(ConfigFromFile, self).__init__()
        self.filename = filename


class ConfigFromHost(Config):

    cmd = 'PATH={}:$PATH;cmt-config > {}'

    def __init__(self, hostname='siwenna.colorado.edu'):
        super(ConfigFromHost, self).__init__()
        self.filename = 'wmt-config-{}.yaml'.format(hostname)
        self.host = HostInfo(hostname)
        self.host.load()
        self.hostpath = os.path.join(self.host.info['wmt_prefix'], 'bin')
        self.hostfile = '/tmp/{}'.format(self.filename)

    def build_on_host(self, username=None, password=None):
        if username is None:
            username = self.host.info['username']
        if password is None:
            password = self.host.info['password']
        cmd = self.cmd.format(self.hostpath, self.hostfile)
        ssh = open_connection(self.host.info['name'], username, password)
        _, stdout, stderr = ssh.exec_command(cmd)  # All
        cfg = stdout.readlines()                   # three lines
        err = stderr.readlines()                   # needed. Why?
        ssh.close()

    def fetch_from_host(self, local_dir=None, username=None, password=None):
        if local_dir is None:
            local_dir = top_dir
        if username is None:
            username = self.host.info['username']
        if password is None:
            password = self.host.info['password']
        ssh = open_connection(self.host.info['name'], username, password)
        sftp = ssh.open_sftp()
        self.filename = os.path.join(local_dir, self.filename)
        sftp.get(self.hostfile, self.filename)
        ssh.close()
