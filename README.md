# wmt-metadata
Metadata for components used by the WMT.

Prepare to install components into a WMT server
by setting
the name of the WMT executor and
the paths to where WMT is installed on the server and the executor.

    wmt_executor="beach.colorado.edu"
    wmt_executor_path=/home/csdms/wmt/_testing
    wmt_server_path=/data/web/htdocs/wmt/api/_testing

Install the components with

    bash ./scripts/install-components.sh

This pulls component information from the executor into the server.

The ownership of all WMT server files is by the group `nobody`,
so `sudo` privileges on the server machine
are needed to install the components.

To instead install components manually, use

```
ssh beach.colorado.edu PATH=/home/csdms/wmt/topoflow.1/conda/bin:\$PATH cmt-config > wmt-config-beach.yaml
sudo rm -rf ../../db/components
sudo cp -r metadata/ ../../db/components
sudo chown -R huttone ../../db/components
./scripts/build-metadata ./wmt-config-beach.yaml --prefix=../../db/components
```
