#!/bin/env python3
##
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
