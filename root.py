import pydbus
from gi.repository import GLib, GObject

class RootObj(object):
    __system_bus = pydbus.SystemBus()
    __bluez_bus_name = 'org.bluez'
    def __init__(self):
        self.__dbus_obj = __class__.__system_bus.get(__class__.__bluez_bus_name, '/')
        self.device_path_list = []
        self.__initialize_glib_loop()

    def __initialize_glib_loop(self):
        self.__dbus_obj.InterfacesAdded.connect(self.__add_device_to_list)
        self.__dbus_obj.InterfacesRemoved.connect(self.__remove_device_from_list)

    def __add_device_to_list(self, path, interfaces):
        if 'org.bluez.Device1' in interfaces.keys():
                self.device_path_list.append(path)
            return

    def __remove_device_from_list(self, path, interfaces):
        if 'org.bluez.Device1' in interfaces.keys():
            try:
                self.device_path_list.remove(path)
            except ValueError:
                pass
        return

    @property
    def managed_objects(self):
        return self.__dbus_obj.GetManagedObjects()