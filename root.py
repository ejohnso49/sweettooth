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

