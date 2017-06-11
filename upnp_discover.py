#!/usr/bin/env python
"""
upnp_discover.py

Listen for uPnp alive messages

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-11
"""
from __future__ import print_function

import socket

MULTICAST_GRP = "239.255.255.250"
MULTICAST_PORT = 1900

def mlisten(grp, port):
    """
    Listen for multicast packets and print them
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

    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error, exception:
            print('Exception', exception)
        print(addr)
        print(data)
        print('---')

mlisten(MULTICAST_GRP, MULTICAST_PORT)
