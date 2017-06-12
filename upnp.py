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

import socket

#  http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf

MULTICAST_GRP = "239.255.255.250"
MULTICAST_PORT = 1900

def mlisten(grp, port):
    """
    Listen for multicast packets and return them
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass

    sock.bind((grp, port))
    host = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(grp) + socket.inet_aton(host))

    data = None
    addr = None

    try:
        data, addr = sock.recvfrom(9000)
    except socket.error, exception:
        print('Exception', exception)

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

def main():
    """
    Main program sit in a loop printing packets
    """

    while True:
        data, addr = mlisten(MULTICAST_GRP, MULTICAST_PORT)
        print(addr)
        print(data)
        command, spec, version, values = parse_upnp(data)
        print("Command", command)
        print("Spec", spec)
        print("Version", version)
        print("Values", values)
        for i in values:
            print(i, values[i])
        
        print('---')

if __name__ == '__main__':
    main()
