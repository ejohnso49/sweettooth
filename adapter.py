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


from gi.repository import GLib
import pydbus

BLUEZ_NAME = 'org.bluez'
SYSTEM_BUS = pydbus.SystemBus()


class Adapter (object):
    __bluez_root = SYSTEM_BUS.get(BLUEZ_NAME, '/')

    def __init__(self, hci_address):
        self._adapter_obj = self._find_adapter(hci_address)
        self.powered = True

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

        obj_dict = cls.__bluez_root.GetManagedObjects()
        # Filter only object paths with 'hci'
        hci_dict = {key: val for (key, val) in obj_dict.items() if 'hci' in key}
        for path, hci in hci_dict.items():
            if hci['org.bluez.Adapter1']['Address'] == hci_address:
                result = SYSTEM_BUS.get(BLUEZ_NAME, path)

        if result is None:
            raise Exception('No HCI found with address {}'.format(hci_address))
        return result


if __name__ == '__main__':
    hci0 = Adapter('5C:F3:70:81:D3:6C')
    print(hci0.powered)
