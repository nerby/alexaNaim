#!/usr/bin/env python
"""
alex_naim.py

Control Naim mu-so volume using Amazon's Alexa

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-11
"""
from __future__ import print_function

import socket
import uuid
from upnp import mlisten, verify_msearch, MULTICAST_GRP, MULTICAST_PORT
from web import WebServer

RUNNING = True

def listen_msearch():
    """
    1.2.2 Discovery: Search: Request with M-SEARCH

    Listen for a M-SEARCH (ssdp.discovery)

    """

    while True:
        data, addr = mlisten(MULTICAST_GRP, MULTICAST_PORT)
        try:
            hostname = socket.gethostbyaddr(addr[0])
        except socket.herror:
            hostname = "UNKNOWN"
        print(addr, hostname)
        print(data)
        found, search_target, maximum_time = verify_msearch(data)
        if found:
            return hostname, search_target, maximum_time

def test_msearch():
    """
    Stub to test listen_msearch
    """

    while RUNNING:
        hostname, search_target, maximum_time = listen_msearch()
        print(hostname[0], hostname[2], search_target, maximum_time)

def get_uuid():
    """
    Get a uuid for this instance, the first time create a unique uuid and place
    it in a file. On subsequent requests just return the value from the file.
    """

    uuid_file = "uuid.txt"

    try:
        fobject = open(uuid_file, 'r')

    except IOError:
        device_uuid = str(uuid.uuid1())
        fobject = open(uuid_file, "w")
        fobject.write(device_uuid)
        fobject.close()
    else:
        device_uuid = fobject.readline()
        fobject.close()

    return device_uuid


def main():
    """
    Main program
    """

    global RUNNING # pylint: disable=global-statement

    web = WebServer()
    try:
        web.daemon = True
        web.start()
        test_msearch()
    except KeyboardInterrupt:
        print("Interrupted")
        RUNNING = False
        web.stop()

if __name__ == '__main__':
    main()
