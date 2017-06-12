#!/usr/bin/env python
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

import BaseHTTPServer
import threading
import time
import urllib

WEBSERVERPORT = 8080
TIMEFMT = "%Y-%m-%d %H:%M:%S"

def index(sock):
    """
    Return index page
    """

    sock.write("<html>")
    sock.write("<head>")
#    sock.write('<meta http-equiv="refresh" content="30">')
    sock.write("</head>")
    sock.write("<body>")
    sock.write("<title>Alexa to Naim bridge</title>")
    sock.write("<h1>Alexa to Naim bridge</h1>")
    sock.write("<h2>%s</h2>" % time.strftime(TIMEFMT))

    sock.write("</body>")
    sock.write("</html>")

def description(sock):
    """
    Generate a description page
    """

    sock.write("<html>")
    sock.write("<head>")
#    sock.write('<meta http-equiv="refresh" content="30">')
    sock.write("</head>")
    sock.write("<body>")
    sock.write("<title>Description</title>")
    sock.write('<h1>Description</h1>')
    sock.write("<h2>%s</h2>" % time.strftime(TIMEFMT))
    sock.write("<h2>TBD</h2>")

    sock.write("</body>")
    sock.write("</html>")

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Handle requests for URLs
    """

    paths = {"/" : index,
             "/description.xml" : description,
            }

    def do_HEAD(sock):  # pylint: disable=invalid-name,no-self-argument
        """
        Respond to head request
        """

        sock.send_response(200)
        sock.send_header("Content-type", "text/html")
        sock.end_headers()

    def do_GET(sock):  # pylint: disable=invalid-name,no-self-argument
        """
        Respond to GET request
        """

        print("Path", sock.path, urllib.unquote(sock.path))
        Handler.do_HEAD(sock)
        if sock.path in sock.paths:
            sock.paths[sock.path](sock.wfile)
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

        self.webserver(BaseHTTPServer.HTTPServer, Handler)


    def webserver(self, server_class, handler_class):
        """
        The web server
        """

        server_address = ('127.0.0.1', WEBSERVERPORT)
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
