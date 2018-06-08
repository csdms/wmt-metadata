#! /usr/bin/env bash
# Install all components to the db/components directory of a WMT server.

if [ -z "$wmt_executor" ]; then
    wmt_executor="siwenna.colorado.edu"
fi

if [ -z "$wmt_executor_username" ]; then
    wmt_executor=$USER
fi

if [ -z "$wmt_executor_path" ]; then
    wmt_executor_path="/home/csdms/wmt/_testing"
fi

if [ -z "$wmt_server_path" ]; then
    wmt_server_path="/data/web/htdocs/wmt/api/_testing"
fi

project_dir=$(pwd)

echo "WMT executor      = $wmt_executor"
echo "WMT executor user = $wmt_executor_username"
echo "WMT executor path = $wmt_executor_path"
echo "WMT server path   = $wmt_server_path"

ssh $wmt_executor_username@$wmt_executor \
    PATH=$wmt_executor_path/conda/bin:\$PATH \
    cmt-config > $project_dir/wmt-config-$wmt_executor.yaml

sudo rm -rf $wmt_server_path/db/components
sudo cp -r $project_dir/metadata/ $wmt_server_path/db/components
sudo chown -R $USER $wmt_server_path/db/components

$project_dir/scripts/build-metadata \
    $project_dir/wmt-config-$wmt_executor.yaml \
    --prefix=$wmt_server_path/db/components
