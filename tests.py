#!/usr/bin/env python3
"""
tests.py

Place for unit tests

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-12
"""
from __future__ import print_function

import unittest
import upnp

class TestUPnPMethods(unittest.TestCase):
    """
    Test UPnP methods
    """

    EOL = "\r\n"

    NOTIFY1 = ["NOTIFY", "*", "HTTP/1.1",
               {"Host" : "239.255.255.250:1900",
                "Location" : "http://172.16.1.160:3500",
                "NTS" :  "ssdp:alive",
                "Cache-Control" : "max-age=1800",
                "Server" : "UPnP/1.0 DLNADOC/1.50 AirReceiver/1.0.3.0",
                "USN" : "uuid:8698b57c-42b5-44d0-93dc-295178cca460::urn:schemas-upnp-org:service:ConnectionManager:1", # pylint: disable=line-too-long

                "NT" : "urn:schemas-upnp-org:service:ConnectionManager:1"
               }]

    BAD1 = ["", "", "", {}]

    BAD2 = ["NOTIFY", "*", "HTTP/1.1", {}]

    def build_packet(self, comp):
        """
        Build a packet from components
        """

        packet = ""
        for i in comp[0:3]:
            packet += i + " "

        packet += self.EOL

        values = comp[3]

        for i in values:
            packet += i + ": " + values[i] + self.EOL

        return packet

    def test_parse(self):
        """
        Test the parser
        """

        for notify in [self.NOTIFY1, self.BAD1, self.BAD2]:
            packet = self.build_packet(notify)
            command, spec, version, values = upnp.parse_upnp(packet)
            self.assertEqual(command, notify[0])
            self.assertEqual(spec, notify[1])
            self.assertEqual(version, notify[2])

            actual_values = notify[3]
            for i in actual_values:
                self.assertEqual(values[i], actual_values[i])

if __name__ == '__main__':
    unittest.main()
