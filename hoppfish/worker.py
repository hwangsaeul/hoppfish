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

from hoppfish.pipeline import Pipeline
import threading

# fmt: off
import gi
gi.require_version('GLib', '2.0')


from gi.repository import GLib  # noqa: E402
# fmt: on


class Worker(threading.Thread):

    def __init__(self, name=None):

        threading.Thread.__init__(self)

        self.name = name
        self.pipelines = {}
        self.loop = GLib.MainLoop()

    def _timeout(self):

        for uuid, pipeline in self.pipelines.items():
            if not pipeline.aborted():
                return True

        self.abort()
        self.loop.quit()
        return False

    def run(self):
        GLib.timeout_add(1000, self._timeout)

        try:
            self.loop.run()
        except GLib.Error:
            pass

    def add_pipeline(self, pipeline: Pipeline, start=True):
        self.pipelines[pipeline.uuid] = pipeline
        if start:
            pipeline.play()

    def abort(self):
        for uuid, pipeline in self.pipelines.items():
            pipeline.stop(True)

        self.loop.quit()
