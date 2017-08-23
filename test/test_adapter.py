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

import unittest
import adapter


class AdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.address = '5C:F3:70:81:D3:6C'
        self.adapter = adapter.Adapter(self.address)
        return

    def test_powered(self):
        self.adapter.powered = False
        self.assertFalse(self.adapter.powered)
        self.adapter.powered = True
        self.assertTrue(self.adapter.powered)
        return

    def test_address(self):
        self.assertEqual(self.adapter.address, self.address)
        return

    def tearDown(self):
        self.adapter.powered = False
        return


# This class is used to test discovery functions of the adapter
class AdapterDiscoveryTestCase(unittest.TestCase):
    def setUp(self):
        self.address = '5C:F3:70:81:D3:6C'
        self.adapter = adapter.Adapter(self.address)
        return


if __name__ == '__main__':
    unittest.main()
