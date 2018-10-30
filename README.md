# wmt-metadata

Build the metadata for CSDMS components used in the
Web Modeling Tool (WMT).

Install this package into the Python distribution used by a WMT server.
Then,
build and install component metdata with the hostname of an executor

    build-metadata --hostname='siwenna.colorado.edu'

or with an existing WMT config file from an executor

    build-metadata --config-file='wmt-config-siwenna.colorado.edu.yaml'
