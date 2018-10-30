# wmt-metadata

Build the metadata for CSDMS components used in the
Web Modeling Tool (WMT).

Install this package into the Python distribution used by a WMT server.
Then,
build and install component metdata with the hostname of an executor

    build-metadata --hostname='siwenna.colorado.edu'

or with an existing WMT config file from an executor

    build-metadata --config-file='wmt-config-siwenna.colorado.edu.yaml'

Note that  `--config-file` and `--hostname` are mutually exclusive.

By default,
metadata for all components is built.
Setting the `--components` keyword to the name of a single component
will built only that component.
This keyword works with either `--config-file` or `--hostname`.
