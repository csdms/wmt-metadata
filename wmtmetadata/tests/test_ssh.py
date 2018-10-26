"""Unit tests for the ssh module."""

import paramiko
import pytest
from wmtmetadata.ssh import open_connection


host = 'localhost'
user = 'foo'
passwd = 'bar'


def test_open_connection():
    with pytest.raises(paramiko.SSHException):
        ssh = open_connection(host, user, passwd)
