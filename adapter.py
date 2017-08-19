import dbus
from sys import exit
from abc import ABC

BLUEZ_NAME = "org.bluez"
bus = dbus.SystemBus()

bluez_root_object = bus.get_object("org.bluez", "/")  # Possible global var
bluez_obj_manager = dbus.Interface(bluez_root_object, "org.freedesktop.DBus.ObjectManager")  # Possible global var
object_dict = bluez_obj_manager.GetManagedObjects()  # Possible global var
hci_dict = {key: val for (key, val) in object_dict.items() if "hci" in key}  # Possible global var


def generic_get_property(prop_ifc, ifc_name, prop_name):
    return prop_ifc.Get(ifc_name, prop_name)


def generic_set_property(prop_ifc, ifc_name, prop_name, prop_val):
    prop_ifc.Set(ifc_name, prop_name, prop_val)
    return


class Adapter1DBus(ABC):

    def __init__(self, hci_name):
        print(bluez_root_object)
        if hci_name is None or hci_name is "":
            hci_name = "hci0"
        try:
            self._hci_dbus_obj = hci_dict['/'.join(["/org", "bluez", hci_name])]
            self._prop_ifc = dbus.Interface(self._hci_dbus_obj, "org.freedesktop.DBus.Properties")
            self._adapter_ifc = dbus.Interface(self._hci_dbus_obj, "org.bluez.Adapter1")


        except KeyError as err:
            print("Error: hci_name not found {}".format(str(err)))
            exit(1)

    @property
    def discovering(self):
        return generic_get_property(self._prop_ifc, "org.bluez.Adapter1", "discovering")

    @property
    def powered(self):
        return self._hci_dbus_obj["org.bluez.Adapter1"]["Powered"]

    @property
    def pairable(self):
        return generic_get_property(self._prop_ifc, "org.bluez.Adapter1", "pairable")
