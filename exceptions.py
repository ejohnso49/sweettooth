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
