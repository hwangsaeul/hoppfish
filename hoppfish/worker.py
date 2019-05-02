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
