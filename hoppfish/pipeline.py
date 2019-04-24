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

from gi.repository import GLib, GObject, Gst
import uuid

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')


class Pipeline:

    def __init__(self, uuid=None):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if self._uuid != None:
            raise ValueError('Can\'t overwrite existing uuid value')
        self._uuid = uuid

    def play(self):
        pass

    def stop(self):
        pass

    def aborted(self):
        return False


class GstPipeline(Pipeline):

    def __init__(self, uuid=None):
        self._pipeline = None
        self._bus = None
        self._timeout_ms = -1
        self._aborted = False
        Pipeline.__init__(self, uuid)

    def __del__(self):
        if self._pipeline != None:
            self._pipeline.set_state(Gst.State.NULL)

    def aborted(self):
        return self._aborted

    def _timeout(self):
        self.stop(True)
        return False

    def build_pipeline(self, pipeline_description, timeout_ms=5000):
        try:
            self._pipeline = Gst.parse_launch(pipeline_description)
            self._bus = self._pipeline.get_bus()
            self._bus.add_signal_watch()
            self._timeout_ms = timeout_ms
        except GLib.Error as e:
            raise Exception('gst-exception', e.message)

        return self._pipeline

    def play(self):
        self._pipeline.set_state(Gst.State.PLAYING)
        GLib.timeout_add(self._timeout_ms, self._timeout)

    def stop(self, terminate=False):
        if terminate:
            self._pipeline.set_state(Gst.State.NULL)
            self._aborted = terminate
        else:
            self._pipeline.set_state(Gst.State.PAUSED)
