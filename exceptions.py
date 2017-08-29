class SweettoothException(Exception):
    """There was an ambiguous exception in Sweettooth"""
    pass


class NoAdaptersFoundException(SweettoothException):
    """Could not find any HCI adapters on DBus"""
    pass


class AdapterNotFoundException(SweettoothException):
    """Could not find the specified HCI adapter on DBus"""

    def __init__(self, address):
        message = 'HCI Adapter with address: {} not found'.format(address)
        super().__init__(message)
