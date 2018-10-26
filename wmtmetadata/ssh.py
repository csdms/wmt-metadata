"""Routines that use SSH."""

import paramiko


def open_connection(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password)
    except paramiko.SSHException:
        raise

    return ssh
