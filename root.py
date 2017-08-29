# Sweettooth, a simple Bluez and DBus library
# Copyright (C) 2017  Eric Johnson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pydbus
import re
from exceptions import NoAdaptersFoundException
from gi.repository import GLib, GObject
from time import sleep


class RootObj(object):
    __system_bus = pydbus.SystemBus()
    __bluez_bus_name = 'org.bluez'
    __adapter_regex_str = r"^/org/bluez/hci\d+$"

    def __init__(self):
        self.__dbus_obj = __class__.__system_bus.get(__class__.__bluez_bus_name, '/')
        self.adapter_path_list = self.__find_hci_adapter_paths()    # This seems hacky, but I'm not sure why

    def update_hci_adapter_path_list(self):
        self.adapter_path_list = self.__find_hci_adapter_paths()

    def __find_hci_adapter_paths(self):
        result = []
        obj_dict = self.managed_objects
        for object_path in obj_dict.keys():
            if re.search(__class__.__adapter_regex_str, object_path) is not None:
                result.append(object_path)
        if not result:
            raise NoAdaptersFoundException()
        return result

    @property
    def managed_objects(self):
        return self.__dbus_obj.GetManagedObjects()

