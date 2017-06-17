#!/usr/bin/env python3
"""
utils.py

Common utility functions

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-17
"""
from __future__ import print_function

import socket

def get_interface_ip_address(peer="8.8.8.8"):
    """
    Get the IP address of the interface on which I will transmit packets
    This will discover one of the interfaces on the host.
    No traffic is sent as this a UDP connect.
    There might be issues if the host has multiple interfaces, in which case
    pass in the IP address of the peer host that we wish to communicate with.

    What used to work really nicely:
    print(socket.gethostbyname(socket.gethostname()))
    There was a dependency on the local name lookup machinery but it
    didn't really matter because of the infrastructure is down this program
    wpuld fail anyway. Unfortunately the Linux guys started adding an entry of
    the form:
    127.0.0.1 hostname
    Therefore this trick returns 127.0.0.1.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((peer, 1))
    interface_ip_address = sock.getsockname()[0]
    sock.close()

    return interface_ip_address

if __name__ == '__main__':
    print(get_interface_ip_address())
    print(get_interface_ip_address("8.8.8.8"))
