#!/bin/bash -e

PACKAGES="scylla-package.tar.gz scylla-python3-package.tar.gz scylla-jmx-package.tar.gz scylla-tools-package.tar.gz"
if [ ! -e reloc/build_reloc.sh ]; then
    echo "run build_reloc.sh in top of scylla-unified-pkg dir"
    exit 1
fi

for p in $PACKAGES; do
    if [ ! -f $p ]; then
        echo "copy $p to $(pwd) before running build_reloc.sh"
        exit 1
    fi
done

for p in $PACKAGES; do
    t=build/${p%-package.tar.gz}
    mkdir -p $t
    tar -C $t -xpf $p
done
cp install.sh build

tar -C build -czpf build/scylla-unified-package.tar.gz ${PACKAGES//-package.tar.gz} install.sh
