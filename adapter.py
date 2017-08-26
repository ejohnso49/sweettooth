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
import pydbus
import re

BLUEZ_NAME = 'org.bluez'
SYSTEM_BUS = pydbus.SystemBus()
loop = GLib.MainLoop()


class Adapter (object):
    __bluez_root = SYSTEM_BUS.get(BLUEZ_NAME, '/')

    def __init__(self, hci_address, search_key, search_address=False):
        self._adapter_obj = self._find_adapter(hci_address)
        self.powered = True
        self._search_key = search_key
        self._device_path = ''
        if search_address is True:
            self.__bluez_root.InterfacesAdded.connect(self._search_for_device_address)
            # self.__bluez_root.OnPropertiesChanged = self._search_for_device_address
        else:
            self.__bluez_root.InterfacesAdded.connect(self._search_for_device_name)
            # self.__bluez_root.OnPropertiesChanged = self._search_for_device_name
        return

    def start_discovery(self):
        self._adapter_obj.StartDiscovery()
        return

    def stop_discovery(self):
        self._adapter_obj.StopDiscovery()
        return

    def _search_for_device_address(self, path, interfaces):
        print('Search for device address')
        print(path)
        print(interfaces)
        if 'org.bluez.Device1' in interfaces.keys():
            print(interfaces['org.bluez.Device1']['Address'])
            if interfaces['org.bluez.Device1']['Address'] == self._search_key:
                self._device_path = path
                loop.quit()
        return

    def _search_for_device_name(self, path, interfaces):
        print('Search for device name')
        if 'org.bluez.Device1' in interfaces.keys():
            print(interfaces['org.bluez.Device1']['Alias'])
            if interfaces['org.bluez.Device1']['Alias'] == self._search_key:
                self._device_path = path
                loop.quit()
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
        hci_regex = re.compile(r'.*(hci)\d$')

        obj_dict = cls.__bluez_root.GetManagedObjects()
        # Filter only object paths with 'hci'
        hci_dict = {key: val for (key, val) in obj_dict.items() if hci_regex.match(key)}
        for path, hci in hci_dict.items():
            if hci['org.bluez.Adapter1']['Address'] == hci_address:
                result = SYSTEM_BUS.get(BLUEZ_NAME, path)

        if result is None:
            raise Exception('No HCI found with address {}'.format(hci_address))
        return result


def force_timeout():
    print('timeout hit')
    loop.quit()

if __name__ == '__main__':
    GObject.timeout_add(50000, force_timeout)
    hci0 = Adapter('5C:F3:70:81:D3:6C', '00:06:66:D8:19:81', False)
    hci0.start_discovery()
    loop.run()
    hci0.stop_discovery()
    print(hci0._device_path)
