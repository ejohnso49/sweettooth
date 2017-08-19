import dbus
from adapter import Adapter1DBus


bus = dbus.SystemBus()


if __name__ == "__main__":
    hci = Adapter1DBus("hci0")

    print(hci.discovering)
    print(hci.powered)
    print(hci.pairable)
