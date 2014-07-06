#!/usr/bin/env python
# -*- coding: utf-8 -*-

from traceback import print_exc
from threading import Thread
from socket import gethostbyaddr, herror

from ident import getIdent

def tryToGetHostnameFromIp(ip):
    try:
        return gethostbyaddr(ip)[0]
    except herror:
        return ip

class ClientConnection(Thread):

    def __init__(self, server, connection, address):
        Thread.__init__(self)
        
        self.server = server
        self.connection = connection
        self.address = address
        self.userident = getIdent(address, server.port, 3) # 3 sec timeout
        self.hostname = tryToGetHostnameFromIp(address[0])
        if self.userident is not None:
            self.userhost = self.userident + '@' + self.hostname
        else:
            self.userhost = self.hostname
        
        self.daemon = True
        self.start()

    def run(self):
        socketfile = self.connection.makefile()
        try:
            while True:
                line = socketfile.readline()
                if line == '':
                    self.server.close_connection(self)
                    break
                self.server.handle_line(self, line)
        except:
            print_exc()
            self.server.close_connection()
    
    def send(self, data):
        for line in data.split('\n'):
            line = line.replace('\r', '').replace('\0', '')
            if line:
                self.connection.send(line + '\n')
    
    def close_connection(self):
        self.connection.close()
