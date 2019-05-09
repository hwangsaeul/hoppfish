#!/bin/env python3
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


import pytest
import uuid

from hoppfish.worker import Worker
from hoppfish.pipeline import Pipeline, GstPipeline

# fmt: off
import gi
gi.require_version('Gst', '1.0')


from gi.repository import GObject, Gst
# fmt: on
import gi


def test_empty_worker():
    Gst.init()

    worker = Worker()

    p = GstPipeline(str(uuid.uuid4()))
    p.build_pipeline('videotestsrc ! fakesink')

    worker.add_pipeline(p)
    worker.start()
    worker.join()
