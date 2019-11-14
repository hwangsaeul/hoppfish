#
#  Copyright 2019 SK Telecom Co., Ltd.
#    Author: Walter Lozano <walter.lozano@collabora.com>
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

from flask import Flask
from flask_restful import request, abort, Api, Resource
import dbus
import json

app = Flask(__name__)
api = Api(app)

def get_json_value(obj, key, default):
    ret = default
    try:
       ret = obj[key]
    except:
        pass

    return ret

#########################################
# Live Streaming
# POST
#   srt/start/edgeId, srt/stop/edgeId
# GET
#   srt/url/edgeId
#########################################
class srt(Resource):
    def post(self, method, edge_id):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Hwangsae1',
                    '/org/hwangsaeul/Hwangsae1/EdgeInterface')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Hwangsae1.EdgeInterface')

            ret = ''
            if method == "start":
                if request.is_json:
                    body = request.get_json()
                    print("body:", str(body))
                    width = get_json_value(body, 'width', 0)
                    height = get_json_value(body, 'height', 0)
                    fps = get_json_value(body, 'fps', 0)
                    bitrate = get_json_value(body, 'bitrate', 0)
                    ret = dbus_interface.Start(edge_id, width, height, fps, bitrate)
                    print("ret:", ret)
                else:
                    return "body type is not json", 404
            elif method == "stop":
                ret = dbus_interface.Stop(edge_id)
                print("ret:", ret)

            response = json.loads('{"url": "' + ret + '"}')

        except Exception as e:
            print ('Exception:', e)
            response = "internal error"
            http_ret = 404
        return response, http_ret

api.add_resource(srt, '/api/v1.0/srt/<method>/<edge_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
