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

import dbus

def enroll():
    try:
        print ("Get Arbiter Agent Bus Interface");
        obj = dbus.SessionBus().get_object('org.hwangsaeul.Chamge1',
                '/org/hwangsaeul/Chamge1/Arbiter/Manager')
        dbus_interface = dbus.Interface(obj,
                dbus_interface='org.hwangsaeul.Chamge1.Arbiter.Manager')

        """Call a method that make arbiter manager to enroll"""
        dbus_interface.Enroll()

        """Call a method that make arbiter manager to activate"""
        dbus_interface.Activate()
    except dbus.exceptions.DBusException as error:
        print(str(error) + "\n")
        return False

    return True

if __name__ == '__main__':
    if enroll() == True:
        print ("Arbiter Agent is Enrolled...");
    else:
        print ("Arbiter Agent is not working...");

