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
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Hwangsae1.RecorderAgent',
                    '/org/hwangsaeul/Hwangsae1/RecorderInterface')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Hwangsae1.RecorderInterface')

            ret = ''
            response = json.loads('{}')
            if method == "start":
                ret = dbus_interface.Start(edge_id)
                print("ret:", ret)
                response = json.loads('{"recordId": "' + ret + '"}')
            elif method == "stop":
                ret = dbus_interface.Stop(edge_id)
                print("ret:", ret)

        except Exception as e:
            print ('Exception:', e)
            response = "internal error"
            http_ret = 404
        return response, http_ret

api.add_resource(srt, '/api/v1.0/record/<method>/<edge_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9090', debug=True)
