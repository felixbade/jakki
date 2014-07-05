#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread

class ClientHandler(Thread):

    def __init__(self, server, connection, address):
        Thread.__init__(self)
        self.server = server
        self.connection = connection
        self.address = address
        self.daemon = True
        self.start()

    def run(self):
        # Broadcast everything forever
        while True:
            line = self.connection.makefile().readline()
            for client in self.server.clients:
                if client is not self:
                    host = self.address[0]
                    port = self.address[1]
                    client.connection.send('%s:%d\t%s' % (host, port, line))
