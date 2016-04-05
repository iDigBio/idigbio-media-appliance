#!/bin/bash

rm -r ~/conda-builds
mkdir ~/conda-builds
mkdir ~/conda-builds/platform-pack/

cd ~/conda-builds

packages='pytest-cov python-editor aniso8601 blinker flask-restful flask-sqlalchemy appdirs alembic easygui'

for p in $packages; do
    rm ~/miniconda3/conda-bld/linux-64/$p*
    conda skeleton pypi $p;
    if [ "$p" = "flask-restful" ]; then
        sed -i 's/\[paging\]//' flask-restful/meta.yaml;
    fi
    conda build --no-test $p;
    conda convert --platform all `ls ~/miniconda3/conda-bld/linux-64/$p*` -o ~/conda-builds/platform-pack/;
done

for p in `ls ~/conda-builds/platform-pack/*/*`; do
    anaconda upload --user idigbio $p;
done
