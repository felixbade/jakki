#!/usr/bin/env python
# -*- coding: utf-8 -*-

from traceback import print_exc
from threading import Thread
from socket import gethostbyaddr
from ident import getIdent

def tryToGetHostnameFromIp(ip):
    try:
        return gethostbyaddr(ip)[0]
    except socket.herror:
        return ip

class ClientConnection(Thread):

    def __init__(self, server, connection, address):
        Thread.__init__(self)
        
        self.server = server
        self.connection = connection
        self.address = address
        self.ident = getIdent(address, server.port, timeout=3)
        self.hostname = tryToGetHostnameFromIp(address[0])
        
        self.daemon = True
        self.start()

    def run(self):
        socketfile = self.connection.makefile()
        try:
            while True:
                line = socketfile.readline()
                if line == '':
                    self.close()
                    break
                self.handle(line)
        except:
            print_exc()
            self.close()

    def handle(self, line):
        pass

    def close(self):
        pass
