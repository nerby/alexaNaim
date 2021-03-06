#!/usr/bin/env python3
"""
web.py

Provide a web server to return description and possibly respond to REST

FILE: $HeadURL$
REVISION: $Revision$
DATE LAST CHANGED: $Date$

Atanu Ghosh
<atanu@acm.org>
2017-06-12
"""
from __future__ import print_function

import sys
import threading
import time
import utils

# Shutdown the errors due to supporting python2 and python3
# pylint: disable=no-name-in-module,import-error

if sys.version_info[0] > 2:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import unquote
else:
    from urllib import unquote
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

WEBSERVERPORT = 8080
TIMEFMT = "%Y-%m-%d %H:%M:%S"

def index(sock):
    """
    Return index page
    """

    sock.write(b"<html>")
    sock.write(b"<head>")
#    sock.write('<meta http-equiv="refresh" content="30">')
    sock.write(b"</head>")
    sock.write(b"<body>")
    sock.write(b"<title>Alexa to Naim bridge</title>")
    sock.write(b"<h1>Alexa to Naim bridge</h1>")
    sock.write(("<h2>%s</h2>" % time.strftime(TIMEFMT)).encode("utf-8"))

    sock.write(b"</body>")
    sock.write(b"</html>")

def description(sock):
    """
    Generate a description page
    """

    sock.write(b"<html>")
    sock.write(b"<head>")
#    sock.write('<meta http-equiv="refresh" content="30">')
    sock.write(b"</head>")
    sock.write(b"<body>")
    sock.write(b"<title>Description</title>")
    sock.write(b'<h1>Description</h1>')
    sock.write(("<h2>%s</h2>" % time.strftime(TIMEFMT)).encode("utf-8"))
    sock.write(b"<h2>TBD</h2>")

    sock.write(b"</body>")
    sock.write(b"</html>")

class Handler(BaseHTTPRequestHandler):
    """
    Handle requests for URLs
    """

    FUNCTION = 0
    CONTENT_TYPE = 1

    paths = {"/" : [index],
             "/description.xml" : [description, "text/xml"],
            }

    def do_HEAD(sock):  # pylint: disable=invalid-name,no-self-argument
        """
        Respond to head request
        """

        content_type = "text/html"

        sock.send_response(200)
        if sock.path in sock.paths:
            entry = sock.paths[sock.path]
            if len(entry) > 1:
                content_type = entry[Handler.CONTENT_TYPE]
            sock.send_header("Content-type", content_type)
        else:
            sock.send_header("Content-type", content_type)
        sock.end_headers()

    def do_GET(sock):  # pylint: disable=invalid-name,no-self-argument
        """
        Respond to GET request
        """

        print("Path", sock.path, unquote(sock.path))
        Handler.do_HEAD(sock)
        if sock.path in sock.paths:
            sock.paths[sock.path[Handler.FUNCTION]](sock.wfile)
        else:
            index(sock.wfile)

class WebServer(threading.Thread):
    """
    Web server in a thread
    """

    keep_running = True

    def run(self):
        """
        Get the remote into from the main thread
        """

        self.webserver(HTTPServer, Handler)


    def webserver(self, server_class, handler_class):
        """
        The web server
        """

        server_address = (utils.get_interface_ip_address(), WEBSERVERPORT)
        httpd = server_class(server_address, handler_class)

        print("Webserver running on ", server_address)
#        browser = "xm http://127.0.0.1:" + str(WEBSERVERPORT)
#        print(browser)
#        os.system(browser)

        while self.keep_running:
            httpd.handle_request()

    def stop(self):
        """
        Get this thread to die
        """

        print("Shutting down web server on next request")
        self.keep_running = False

def main():
    """
    Main program to just run the web server
    """

    web = WebServer()
    try:
        web.daemon = True
        web.start()
        web.join()
    except KeyboardInterrupt:
        print("Interrupted")
        web.stop()

if __name__ == '__main__':
    main()
