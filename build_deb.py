#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 ScyllaDB
#

#
# This file is part of Scylla.
#
# Scylla is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Scylla is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scylla.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import shutil
import tarfile
import subprocess
import pathlib

if __name__ == "__main__":
    shutil.rmtree('build', ignore_errors=True)
    os.makedirs('build/debian')
    subprocess.run('./SCYLLA-VERSION-GEN', shell=True, check=True)
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_deb.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/python3/build_reloc.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/python3/build_deb.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla-jmx')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_deb.sh', shell=True, check=True, cwd='scylla-jmx')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla-tools-java')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_deb.sh', shell=True, check=True, cwd='scylla-tools-java')
    for m in ['scylla', 'scylla-jmx', 'scylla-tools-java']:
        with open('{}/build/SCYLLA-VERSION-FILE'.format(m)) as f:
            version = f.read().strip()
        with open('{}/build/SCYLLA-RELEASE-FILE'.format(m)) as f:
            release = f.read().strip()
        d = pathlib.Path('{}/build/debian'.format(m))
        for f in d.glob('**/scylla*_{}-{}-*.deb'.format(version, release)):
            shutil.copy(f, 'build/debian/{}'.format(f.name))
