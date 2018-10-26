#! /usr/bin/env bash
# Install all components to the db/components directory of a WMT server.

source="${BASH_SOURCE[0]}"
source_dir="$(cd -P "$(dirname "$source")" && pwd)"
project_dir=$(dirname $source_dir)

if [ -z "$wmt_executor" ]; then
    wmt_executor="siwenna.colorado.edu"
fi

if [ -z "$wmt_executor_username" ]; then
    wmt_executor_username="wmtuser"
fi

if [ -z "$wmt_executor_path" ]; then
    wmt_executor_path="/home/csdms/wmt/_testing"
fi

if [ -z "$wmt_server_path" ]; then
    wmt_server_path="/data/web/htdocs/wmt/api/_testing"
fi

echo "WMT executor      = $wmt_executor"
echo "WMT executor user = $wmt_executor_username"
echo "WMT executor path = $wmt_executor_path"
echo "WMT server path   = $wmt_server_path"
echo "project path      = $project_dir"

if [ ! -f $project_dir/wmt-config-$wmt_executor.yaml ]; then
    ssh $wmt_executor_username@$wmt_executor \
	PATH=$wmt_executor_path/conda/bin:\$PATH \
	cmt-config > $project_dir/wmt-config-$wmt_executor.yaml
fi

components=$(python $project_dir/scripts/list-components.py)

rm -rf $wmt_server_path/db/components/*
for c in $components; do
    echo "- $c"
    cp -r $project_dir/metadata/$c $wmt_server_path/db/components
done

$project_dir/scripts/build-metadata \
    $project_dir/wmt-config-$wmt_executor.yaml
