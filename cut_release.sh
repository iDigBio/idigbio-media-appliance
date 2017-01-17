#!/bin/bash

require_clean_work_tree () {
    # Update the index
    git update-index -q --ignore-submodules --refresh
    err=0

    # Disallow unstaged changes in the working tree
    if ! git diff-files --quiet --ignore-submodules --
    then
        echo >&2 "cannot $1: you have unstaged changes."
        git diff-files --name-status -r --ignore-submodules -- >&2
        err=1
    fi

    # Disallow uncommitted changes in the index
    if ! git diff-index --cached --quiet HEAD --ignore-submodules --
    then
        echo >&2 "cannot $1: your index contains uncommitted changes."
        git diff-index --cached --name-status -r --ignore-submodules HEAD -- >&2
        err=1
    fi

    if [ $err = 1 ]
    then
        echo >&2 "Please commit or stash them."
        exit 1
    fi
}

require_clean_work_tree

nv=$(./versioning.py --no-human bump $1)

echo "Creating new $1 release at version $nv"

python setup.py sdist bdist_wheel upload &&
./versioning.py --no-human pypi &&
git commit -am "Creating new $1 release at version $nv." &&
git push &&
git tag $nv &&
git push --tags &&
conda build . --no-test &&
conda convert --platform all ~/anaconda3/conda-bld/linux-64/idigbio-media-appliance-$nv-py35_0.tar.bz2 -o ~/conda-builds/platform-pack/ &&

for p in `ls ~/conda-builds/platform-pack/*/idigbio-media-appliance-$nv*`; do
    anaconda upload --user idigbio $p;
done