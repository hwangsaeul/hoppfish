# -*- coding: utf-8 -*-
#
# Copyright 2019 SK Telecom Co., Ltd.
#   Author: Jeongseok Kim <jeongseok.kim@sk.com>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
Setup file for hoppfish
"""

from setuptools.dist import Distribution
from setuptools import setup, Extension
import os
import re
import subprocess
from subprocess import CalledProcessError

try:
    git_full_version = subprocess.check_output(
        'git describe --long --tags', shell=True, encoding='utf-8')
except CalledProcessError:
    rev_cnt = subprocess.check_output(
        'git rev-list --count --all', shell=True, encoding='utf-8').strip()
    last_hash = subprocess.check_output(
        'git rev-parse --short HEAD', shell=True, encoding='utf-8').strip()
    git_full_version = '0.0.0-%s-g%s' % (rev_cnt, last_hash)

full_version = git_full_version.split('-')

if full_version[1] == '0':
    version = full_version[0]
else:
    version = full_version[0] + '+git' + full_version[1]

setup(name='hoppfish',
      version=version,
      description='Hwangsaeul validation tool',
      url='https://github.com/hwangsaeul/hoppfish',
      packages=['hoppfish'],
      )
