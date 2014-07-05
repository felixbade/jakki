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
        # Greet other clients
        self.broadcast('New user: %s:%d\n' % self.address)
        
        # Tell the new client who are present
        self.connection.send('Currently online:\n')
        for client in self.server.clients:
            self.connection.send('%s:%d\n' % client.address)
        
        # Broadcast every message forever
        while True:
            line = self.connection.makefile().readline()
            if line == '':
                self.broadcast('Quit: %s:%d\n' % self.address)
                self.server.clients.remove(self)
                break
            host = self.address[0]
            port = self.address[1]
            self.broadcast('%s:%d\t%s' % (host, port, line))
    
    def broadcast(self, message):
        for client in self.server.clients:
            if client is not self:
                client.connection.send(message)
