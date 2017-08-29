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


from gi.repository import GLib, GObject
from exceptions import AdapterNotFoundException
from time import sleep
from root import RootObj
import pydbus
import re


class Adapter (object):
    __bluez_bus_name = 'org.bluez'
    __system_bus = pydbus.SystemBus()
    __bluez_root = RootObj()
    __discovery_timeout = 1500  # This time out is in ms

    def __init__(self, hci_address=None):
        self._adapter_obj = self._find_adapter(hci_address)
        self.powered = True
        self.device_path_list = []
        self._setup_glib_loop()
        return

    def _setup_glib_loop(self):
        GObject.timeout_add(__class__.__discovery_timeout, self.__timeout_handler)
        self._loop = GLib.MainLoop()

    def start_discovery(self):
        print('setting discovery on')
        self._adapter_obj.StartDiscovery()
        self._loop.run()
        return

    def stop_discovery(self):
        self._adapter_obj.StopDiscovery()
        return

    @property
    def uuids(self):
        return self._adapter_obj.UUIDs

    @property
    def discoverable(self):
        return self._adapter_obj.Discoverable

    @discoverable.setter
    def discoverable(self, value):
        self._adapter_obj.Discoverable = value
        return

    @property
    def discovering(self):
        return self._adapter_obj.Discovering

    @property
    def pairable(self):
        return self._adapter_obj.Pairable

    @pairable.setter
    def pairable(self, value):
        self._adapter_obj.Pairable = value
        return

    @property
    def powered(self):
        return self._adapter_obj.Powered

    @powered.setter
    def powered(self, value):
        self._adapter_obj.Powered = value
        return

    @property
    def address(self):
        return self._adapter_obj.Address

    @property
    def alias(self):
        return self._adapter_obj.Alias

    @alias.setter
    def alias(self, value):
        self._adapter_obj.Alias = value
        return

    @property
    def modalias(self):
        return self._adapter_obj.Modalias

    @property
    def dbus_name(self):
        return self._adapter_obj.Name

    @property
    def dbus_class(self):
        return self._adapter_obj.Class

    @property
    def discoverable_timeout(self):
        return self._adapter_obj.DiscoverableTimeout

    @discoverable_timeout.setter
    def discoverable_timeout(self, value):
        self._adapter_obj.DiscoverableTimeout = value
        return

    @property
    def pairable_timeout(self):
        return self._adapter_obj.PairableTimeout

    @pairable_timeout.setter
    def pairable_timeout(self, value):
        self._adapter_obj.PairableTimeout = value
        return

    @classmethod
    def _find_adapter(cls, hci_address):
        result = None
        if hci_address is None:     # User didn't specify an address for HCI
            if not cls.__bluez_root.adapter_path_list:
                raise AdapterNotFoundException(hci_address)
            else:   # Default to using the first entry in the adapter path list
                result = cls.__system_bus.get(cls.__bluez_bus_name, cls.__bluez_root.adapter_path_list[0])
        elif hci_address:
            obj_dict = cls.__bluez_root.managed_objects
            for path in cls.__bluez_root.adapter_path_list:
                if obj_dict[path]['org.bluez.Adapter1']['Address'] == hci_address:
                    result = cls.__system_bus.get(cls.__bluez_bus_name, path)
            if result is None:
                raise AdapterNotFoundException

        return result

    def __timeout_handler(self):
        print('entering timeout handler')
        self._loop.quit()


if __name__ == '__main__':
    hci0 = Adapter('5C:F3:70:81:D3:6C', '00:06:66:D8:19:81', True)
    hci0.start_discovery()
    hci0.stop_discovery()
    print(hci0._device_path)
