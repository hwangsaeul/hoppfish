#
#  Copyright 2019 SK Telecom Co., Ltd.
#    Author: Heekyoung Seo <hkseo@sk.com>
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

#########################################
# Live Streaming
# POST
#   srt/start/edgeId, srt/stop/edgeId
# GET
#   srt/url/edgeId
#########################################
class srt(Resource):
    def get(self, method, edge_id):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Chamge1',
                    '/org/hwangsaeul/Chamge1/Arbiter/Manager')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Chamge1.Arbiter.Manager')

            if method == "url":
                method = "getUrl"
                print "method is updated to " + method

            command = '{\"method\":\"' + method + '\",\"to\":\"' + edge_id + '\"}'
            print (command)
            ret = dbus_interface.UserCommand(command)
            result = ret[0]
            response = ret[1]
        except Exception as e:
            response = str(e);
            http_ret = 404
        return response, http_ret
    def post(self, method, edge_id):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Chamge1',
                    '/org/hwangsaeul/Chamge1/Arbiter/Manager')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Chamge1.Arbiter.Manager')

            if method == "start":
                if request.is_json:
                    method = "streamingStart"
                    print "method is updated to " + method
                    params = json.dumps(request.get_json())
                    command = '\",\"params\":' + params + '}'
                else:
                    return "body type is not json", 404
            elif method == "stop":
                method = "streamingStop"
                print "method is updated to " + method
            elif method == "url":
                method = "getUrl"
                print "method is updated to " + method

            command = '{\"method\":\"' + method + '\",\"to\":\"' + edge_id + '\"}'
            print (command)
            ret = dbus_interface.UserCommand(command)
            result = ret[0]
            response = ret[1]
        except Exception as e:
            response = str(e);
            http_ret = 404
        return response, http_ret

#########################################
# Record Start/Stop
# POST
#   record/start/edgeId, record/stop/edgeId
#########################################
class record(Resource):
    def post(self, method, edge_id):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Chamge1',
                    '/org/hwangsaeul/Chamge1/Arbiter/Manager')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Chamge1.Arbiter.Manager')

            if method == "start":
                method = "recordStart"
            elif method == "stop":
                method = "recordStop"

            # TODO
            # replace edge_id to hub_id here or agent'r roll?
            command = '{\"method\":\"' + method + '\",\"to\":\"' + edge_id + '\"}'
            print (command)
            ret = dbus_interface.UserCommand(command)
            result = ret[0]
            response = ret[1]
        except Exception as e:
            response = str(e);
            http_ret = 404
        return response, http_ret

#########################################
# VOD Service 
# GET
#  lookup by edge/record, get url
#  delete request
#########################################
class vod(Resource):
    def get(self, method, uid):
        http_ret = 201
        try:
            obj = dbus.SessionBus().get_object('org.hwangsaeul.Chamge1',
                    '/org/hwangsaeul/Chamge1/Arbiter/Manager')
            dbus_interface = dbus.Interface(obj,
                    dbus_interface='org.hwangsaeul.Chamge1.Arbiter.Manager')
            id_type = "edge_id"

            if method == "lookup-by-record":
                method = "lookupByRecord"
                id_type = "record_id"
                from_str = request.args.get('start', type = str)
                to_str = request.args.get('end', type = str)
                print (from_str)
                print (to_str)
            elif method == "lookup-by-edge":
                method = "lookupByEdge"
                from_str = request.args.get('start', type = str)
                to_str = request.args.get('end', type = str)
                print (from_str)
                print (to_str)
            elif method =="url":
                method = "getUrl"

            # TODO
            # replace edge_id to hub_id here or agent'r roll?
            command = '{\"method\":\"' + method + '\",\"to\":\"' + uid + '\"}'
            print (command)
            ret = dbus_interface.UserCommand(command)
            result = ret[0]
            response = ret[1]
        except Exception as e:
            response = str(e);
            http_ret = 404
        return response, http_ret
    def delete(self, method, uid):
        # TODO
        # implement to create command and invoke UserCommand
        print "[delete] edge id: " + method + ", file id : " + uid
        response = "not impemented, yet"
        return response, 201

api.add_resource(srt, '/api/v1.0/srt/<method>/<edge_id>')
api.add_resource(record, '/api/v1.0/record/<method>/<edge_id>')
api.add_resource(vod, '/api/v1.0/vod/<method>/<uid>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
