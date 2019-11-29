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

class vod(Resource):
    def get(self, method):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Hwangsae1.RecorderAgent',
                    '/org/hwangsaeul/Hwangsae1/RecorderInterface')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Hwangsae1.RecorderInterface')

            ret = ''
            if method == 'lookup-by-record':
                record_id = request.args.get('recordId')
                try:
                    range_from = int(request.args.get('from'))
                except:
                    range_from = 0
                try:
                    range_to = int(request.args.get('to'))
                except:
                    range_to = 0
                ret = dbus_interface.LookupByRecord(record_id, range_from, range_to)
                edge_id = ret[0]
                file_list = ret[1]
                ret = {}
                ret['edgeId'] = edge_id
                file_list_ret = []
                for f in file_list:
                    file_data = {
                      'fileId': f[0],
                      'start': f[1],
                      'end': f[2],
                      'size': f[3]
                    }
                ret['fileList'] = file_list_ret
                ret = json.dumps(ret)

            elif method == 'lookup-by-edge':
                edge_id = request.args.get('edgeId')
                try:
                    range_from = int(request.args.get('from'))
                except:
                    range_from = 0
                try:
                    range_to = int(request.args.get('to'))
                except:
                    range_to = 0
                ret = dbus_interface.LookupByEdge(edge_id, range_from, range_to)
                file_list = ret
                ret = {}
                file_list_ret = []
                for f in file_list:
                    file_data = {
                      'recordId': f[0],
                      'fileId': f[1],
                      'start': f[2],
                      'end': f[3],
                      'size': f[4]
                    }
                    file_list_ret.append(file_data)
                ret['fileList'] = file_list_ret
                ret = json.dumps(ret)

            response = ret

        except Exception as e:
            print ('Exception:', e)
            response = "internal error"
            http_ret = 404
        return response, http_ret

        return response, http_ret

api.add_resource(srt, '/api/v1.0/record/<method>/<edge_id>')
api.add_resource(vod, '/api/v1.0/vod/<method>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9090', debug=True)
