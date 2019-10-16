# -*- coding: utf-8 -*-
#
#  Copyright 2019 SK Telecom Co., Ltd.
#    Author: Jeongseok Kim <jeongseok.kim@sk.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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
