"""
Easy HTTP Handler
"""

import os
import cgi
import sys,threading,datetime,http.server,socketserver
import traceback

import cgi
try:
    from http import HTTPStatus
except:
    class HTTPStatus:
        def __new__(cls, value, phrase, desc=''):
            obj = int.__new__(cls, value)
            obj._value_ = value
            obj.phrase = phrase
            obj.description = desc

        NOT_FOUND = (404, "Not found")
        INTERNAL_SERVER_ERROR = (500, "Internal error")

from urllib.parse import urlparse, parse_qs

class ThreadedTCPServer (socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class EasyHTTPHandler (http.server.SimpleHTTPRequestHandler):
    """
    This class handles the HTTP request from clients.
    Only GET request is implemented.
    This class should be subclassed to extend the functionality.
    """
    PlainTextType = "text/plain; charset=utf-8"
    HTMLType = "text/html; charset=utf-8"
    DocRoot = "."
    logEnabled = False
    defaultFile = "index.html"
    oop = None

    def handleRequest (self, req, qs):
        try:
            res = self.callMethod (req, qs)
            if res:
                out, contype = res
                if not out:
                    return
                if isinstance(out, type('')):
                    out = bytes(out, "UTF-8")
                self.send_response (200, "OK")
                self.send_header ("Expires", "Feb  1 17:17:37 HST 2016")
                self.send_header ("Cache-Control", "no-cache, must-revalidate")
                self.send_header ("Cache-Control", "no-store")
                self.send_header ("Content-Type", contype)
                self.end_headers ()
                self.wfile.write (out)
            else:
                self.serveFile (req, qs)
                return
        except FileNotFoundError:
            self.send_error (HTTPStatus.NOT_FOUND)
        except BrokenPipeError:
            return
        except Exception as e:
            traceback.print_exc()   
            self.send_error (HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_GET(self):
        parts = urlparse (self.path)
        qs = parse_qs (parts.query)
        req = parts.path[1:]
        self.handleRequest (req, qs)

    def do_POST(self):
        parts = urlparse (self.path)
        length = int(self.headers['content-length'])
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        boundary = pdict.get('boundary')

        if boundary:
            pdict['boundary'] = bytes(boundary, 'UTF-8')
            qs = cgi.parse_multipart(fp=self.rfile, pdict=pdict)
        else:
            qs = parse_qs(bytes.decode(self.rfile.read(length), 'UTF-8'))
        req = parts.path[1:]
        self.handleRequest (req, qs)

    def serveFile (self, req, qs):
        self.path = self.DocRoot + "/" + req
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        return None, ""

    def log_message (self, format, *args):
        if self.logEnabled:
            super().log_message(format, *args)
        return 

    def getDefValue (self, qstr, name, defValue):
        try:
            return qstr[name][0]
        except:
            return defValue

    def intVal (self, qstr, name, defValue=0):
        return int(self.getDefValue(qstr, name, str(defValue)))

    def boolVal (self, qstr, name):
        return 1 if qstr[name][0] == 'true' else 0

    def floatVal (self, qstr, name, defValue=0):
        return float(self.getDefValue(qstr, name, str(defValue)))

    def response (self, resp, contType):
        if isinstance(resp, type('')):
            resp = bytes(resp, "UTF-8")
        return resp, contType

    def callMethod (self, req, qstr):
        try:
            if req == "" :
                return False
            req = req.split('/')[-1]
            #print (req, qstr)
            fn = getattr(self, req)
            if fn:
                return fn (req, qstr)
        except Exception as e:
            return False
        return False

class EasyHTTPServerThreaded (ThreadedTCPServer):
    def __init__(self, ipnp, hdl):
        super(EasyHTTPServerThreaded, self).__init__(ipnp, hdl)

    def run4ever (self):
        try:
            self.serve_forever()
            self.shutdown()
        except Exception as e:
            traceback.print_exc()
            print ("HTTPD terminated")

class EasyHTTPServer (socketserver.ForkingTCPServer):
    def __init__(self, ipnp, hdl):
        super(EasyHTTPServer, self).__init__(ipnp, hdl)

    def run4ever (self):
        try:
            self.serve_forever()
            self.shutdown()
        except Exception as e:
            traceback.print_exc()
            print ("HTTPD terminated")

ThreadedTCPServer.allow_reuse_address = True
socketserver.TCPServer.allow_reuse_address = True
