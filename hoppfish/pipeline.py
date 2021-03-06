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

# fmt: off
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')


from gi.repository import GLib, Gst  # noqa: E402
# fmt: on


class Pipeline:

    def __init__(self, uuid=None):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        if self._uuid is not None:
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
        if self._pipeline is not None:
            self._pipeline.set_state(Gst.State.NULL)

    def aborted(self):
        return self._aborted

    def _timeout(self):
        self.stop(True)
        return False

    def _bus_call(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS or t == Gst.MessageType.ERROR:
            GLib.source_remove(self._timeout_id)
            # TODO: error handling
            self.stop(True)

    def build_pipeline(self, pipeline_description, timeout_ms=5000):
        try:
            self._pipeline = Gst.parse_launch(pipeline_description)
            self._bus = self._pipeline.get_bus()
            self._bus.add_signal_watch()
            self._bus.connect('message', self._bus_call)
            self._timeout_ms = timeout_ms
            if self._timeout_ms > 0:
                self._timeout_id = GLib.timeout_add(
                    self._timeout_ms, self._timeout)

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
