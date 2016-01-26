#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

REQUEST_GET = "GET / HTTP/1.0\n\n"
REQUEST_PUT = "PUT / HTTP/1.0\n\n"
DEFAULT_PORT = 80

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        return data

    def get_headers(self,data):
        return data

    def get_body(self, data):
        return data

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):

        request = "GET / HTTP/1.0\n\n"
        socket = self.connect(url, DEFAULT_PORT)
        socket.sendall(REQUEST_GET)

        response = self.recvall(socket)

        code = 200
        body = self.get_body(response)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        print "URL: ", url
        print "COMMAND: ", command
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
# fuck this bullshit hipster loosely typed sad excuse for a language
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):

        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   

