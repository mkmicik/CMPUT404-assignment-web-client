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

REQUEST_GET = "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n"
REQUEST_POST = "POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\nConnection: close\r\n\r\n"
DEFAULT_PORT = 80

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    # return a connection to the host on the specified port
    def connect(self, host, port):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    # return the status code from the response
    def get_code(self, data):
        parsed_response = data.split()
        return parsed_response[1]

    # return the body from the response
    def get_body(self, data):
        #return data
        if data != None:
            return data.split('\r\n\r\n',2)[1]
        else:
            return None

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

    # could not figure out how to use urllib to parse the url so I'm gonna
    # do it manually. Might be more error prone but f*** it
    def splitURL(self, url):
        host = ''
        port = DEFAULT_PORT
        path = ''

        split_url = url.split(':')

        # url_split[0] will always be 'https', always ignored
        if len(split_url) == 2:
            # port is not specified
            # only one colin in the path, no port specified
            paths = split_url[1]
            paths = paths.strip('/')        # remove trailing and leading slashes
            path_list = paths.split('/')    # list in format host, path_dir, path_dir ... path_dir

            host = path_list.pop(0)         # host is the first in the list
            # rebuild the path structure
            for dir in path_list:
                path += '/'
                path += dir
        else:
            # port is specified
            # 2 colins in the path, port must be specified
            host = split_url[1]
            host = host.strip('/')          # remove trailing and leading slashes
            paths = split_url[2]            # list in format port_num, path_dir, path_dir ... path_dir
            path_list = paths.split('/')
            port = path_list[0]             
            path_list.pop(0)                # get the port
            # rebuild the path structure
            for dir in path_list:       
                path += '/'
                path += dir

        # cannot give it nothing, / is the path if no path specified
        if (path == ''): 
            path += '/'

        return host, port, path


    def GET(self, url, args=None):
        # from the url, we need to parse out the host, path, and port to use
        host, port, path = self.splitURL(url)

        request = REQUEST_GET % (path, host)

        #print request

        client_connection = self.connect(host, int(port))
        client_connection.sendall(request)

        response = self.recvall(client_connection)
        client_connection.close()

        code = self.get_code(response)
        body = self.get_body(response)

        #print code
        #print body
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        # from the url, we need to parse out the host, path, and port to use
        host, port, path = self.splitURL(url)
        
        post_body = ""
        arg_len = 0

        # handle args
        if (args != None):
            post_body = urllib.urlencode(args)
            arg_len = len(post_body)
        else:
            post_body = ''
        
        request = REQUEST_POST % (path, host, arg_len)
        request += post_body

        #print request

        client_connection = self.connect(host, int(port))
        client_connection.sendall(request)

        response = self.recvall(client_connection)
        client_connection.close()

        code = self.get_code(response)
        body = self.get_body(response)

        #print code
        #print body

        return HTTPResponse(int(code), body)

    def command(self, url, command="GET", args=None):
        print "URL: ", url
        print "COMMAND: ", command
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
# Entry point supplied by Dr. Hindle
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

