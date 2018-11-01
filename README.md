# wmt-metadata

This repo stores server-side metadata
for a CSDMS Web Modeling Tool (WMT) component,
consisting of

* a description file, **wmt.yaml**, and
* pre- and post-stage hooks.

It also includes a Python package with a tool
for building and installing these metadata into a WMT server.
Install this package into the Python distribution used by a WMT server.
Then,
build and install component metdata
either with the hostname of an executor

    build-metadata --hostname='siwenna.colorado.edu'

or with an existing WMT config file obtained from an executor

    build-metadata --config-file='wmt-config-siwenna.colorado.edu.yaml'

Note that the `--config-file` and `--hostname` keywords
are mutually exclusive.

By default,
metadata for all components is built.
Setting the `--components` keyword to the name of a single component
will build only that component.
This keyword works with either `--config-file` or `--hostname`.
