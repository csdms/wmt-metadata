# wmt-metadata
Metadata for components used by the WMT.

    ssh beach.colorado.edu PATH=/home/csdms/wmt/topoflow.1/conda/bin:\$PATH cmt-config > wmt-config-beach.yaml
    sudo rm -rf ../../db/components
    sudo cp -r metadata/ ../../db/components
    sudo chown -R huttone ../../db/components
    ./build-metadata ./wmt-config-beach.yaml --prefix=../../db/components
