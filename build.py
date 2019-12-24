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

if __name__ == "__main__":
    shutil.rmtree('build', ignore_errors=True)
    os.makedirs('build')
    subprocess.run('./SCYLLA-VERSION-GEN', shell=True, check=True)
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/python3/build_reloc.sh', shell=True, check=True, cwd='scylla')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla-jmx')
    subprocess.run('../tools/toolchain/dbuild ./reloc/build_reloc.sh', shell=True, check=True, cwd='scylla-tools-java')
    ar = tarfile.open('scylla/build/release/scylla-package.tar.gz')
    ar.extractall('build/scylla')
    ar.close()
    ar = tarfile.open('scylla/build/release/scylla-python3-package.tar.gz')
    ar.extractall('build/scylla-python3')
    ar.close()
    ar = tarfile.open('scylla-jmx/build/scylla-jmx-package.tar.gz')
    ar.extractall('build/scylla-jmx')
    ar.close()
    ar = tarfile.open('scylla-tools-java/build/scylla-tools-package.tar.gz')
    ar.extractall('build/scylla-tools')
    ar.close()
    gzip_process = subprocess.Popen("pigz > build/scylla-all-package.tar.gz", shell=True, stdin=subprocess.PIPE)
    ar = tarfile.open(fileobj=gzip_process.stdin, mode='w|')
    ar.add('build/scylla', arcname='scylla')
    ar.add('build/scylla-python3', arcname='scylla-python3')
    ar.add('build/scylla-jmx', arcname='scylla-jmx')
    ar.add('build/scylla-tools', arcname='scylla-tools')
    ar.add('build/SCYLLA-VERSION-FILE', arcname='SCYLLA-VERSION-FILE')
    ar.add('build/SCYLLA-RELEASE-FILE', arcname='SCYLLA-RELEASE-FILE')
    ar.add('build/SCYLLA-PRODUCT-FILE', arcname='SCYLLA-PRODUCT-FILE')
    ar.add('install.sh')
    ar.close()
    gzip_process.communicate()
