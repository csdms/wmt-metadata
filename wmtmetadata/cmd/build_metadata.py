"""Command-line tool to build WMT component metadata."""

import argparse
from wmtmetadata.build import BuildMetadata


def main():
    parser = argparse.ArgumentParser(
        description='Build metadata for a WMT component')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config-file', type=str, default=None,
                        help='Execution server configuration file')
    group.add_argument('--hostname', type=str, default=None,
                        help='Hostname of execution server')
    parser.add_argument('--component', type=str, default=None,
                        help='Name of single component to build')
    args = parser.parse_args()

    if args.config_file is None and args.hostname is None:
        print 'Error: must supply config file or hostname'
        return

    # Args config_file and hostname are mutually exclusive.
    b = BuildMetadata(config_file=args.config_file, hostname=args.hostname)
    b.build()

if __name__ == '__main__':
    main()
