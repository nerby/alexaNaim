#!/usr/bin/env python
"""
upnp.py

Listen for UPnP alive messages

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-11
"""
from __future__ import print_function

import logging
import socket
import sys

# http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf

MULTICAST_GRP = "239.255.255.250"
MULTICAST_PORT = 1900

def mlisten(grp, port):
    """
    Listen for a multicast packet and return it
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass

    sock.bind((grp, port))
    host = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
                    socket.inet_aton(host))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(grp) + socket.inet_aton(host))

    data = None
    addr = None

    try:
        data, addr = sock.recvfrom(9000)
        logging.debug(addr)
        logging.debug(data)
    except socket.error as err:
        print("socket.error".format(err))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    sock.close()

    return data, addr

def parse_upnp(data):
    """
    Parse packet the first line will be of the form
    M-SEARCH * HTTP/1.1
    The rest of the lines will be colon separated field names and values

    return the first line as three fields and the other values as a dictionary
    """

    values = {}

    lines = data.splitlines()
    first_line = lines[0].split()
    for i in lines[1:]:
        pos = i.find(":")
        if pos != -1:
            values[i[0:pos]] = i[pos+1:].strip()

    return first_line[0], first_line[1], first_line[2], values

def verify_msearch(data):   # pylint: disable=too-many-return-statements
    """
    Verify this is a M-SEARCH packet
    return the ST (Search target) and MX (Maximum wait time)
    """

    false_tuple = (False, None, None)

    command, spec, version, values = parse_upnp(data)
    if command != "M-SEARCH":
        return false_tuple
    if spec != "*":
        return false_tuple
    if version != "HTTP/1.1":
        return false_tuple

    mandatory_fields = ["HOST", "MAN", "MX", "ST"]
    for i in mandatory_fields:
        if not values.get(i):
            return false_tuple

    if values["HOST"] != "239.255.255.250:1900" and \
        values["HOST"] != "239.255.255.250":
        print("Unexpected value for HOST %s" % values["HOST"], file=sys.stderr)

    if values["MAN"] != '"ssdp:discover"':
        return false_tuple

    try:
        maximum_time = int(values["MX"])
    except ValueError:
        return false_tuple

    # Spec says value cannot be greater than 120
    if maximum_time > 120:
        maximum_time = 120

    return True, values["ST"], maximum_time

def send_unicast_response(addr, port, payload):
    """
    Send a unicast response to a M-SEARCH (ssdp.discovery)

    HTTP/1.1 200 OK
    HOST: 239.255.255.250:1900
    EXT:
    CACHE-CONTROL: max-age=100
    LOCATION: http://172.16.1.153:80/description.xml
    SERVER: Linux/3.14.0 UPnP/1.0 IpBridge/1.18.0
    hue-bridgeid: 001788FFFE283D27
    ST: upnp:rootdevice
    USN: uuid:2f402f80-da50-11e1-9b23-001788283d27::upnp:rootdevice
    """

    # TODO

def multicast_response(payload):
    """
    Used to send periodic multicast NOTIFY (ssdp.alive)

    NOTIFY * HTTP/1.1
    Host: 239.255.255.250:1900
    Location: http://172.16.1.160:3500/
    NTS: ssdp:alive
    Cache-Control: max-age=1800
    Server: UPnP/1.0 DLNADOC/1.50 AirReceiver/1.0.3.0
    USN: uuid:8698b57c-42b5-44d0-93dc-295178cca460::upnp:rootdevice
    NT: upnp:rootdevice

    """

    # TODO
    # Remember ttl must be set to 4
    # ttl = struct.pack('b', 4)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

def main():
    """
    Main program sit in a loop printing packets
    """

    logging.basicConfig(level=logging.DEBUG)

    while True:
        data, addr = mlisten(MULTICAST_GRP, MULTICAST_PORT)
        try:
            hostname = socket.gethostbyaddr(addr[0])
        except socket.herror:
            hostname = "UNKNOWN"
        print(addr, hostname)
        print(data)
        command, spec, version, values = parse_upnp(data)
        print("Command", command)
        print("Spec", spec)
        print("Version", version)
        print("Values", values)
        for key, value in values.iteritems():
            print(key, value)

        is_msearch, search_target, maximum_wait_time = verify_msearch(data)
        if is_msearch:
            print("M-SEARCH", search_target, maximum_wait_time)

        print('---')

if __name__ == '__main__':
    main()
