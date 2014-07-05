#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread

class ClientHandler(Thread):

    def __init__(self, server, connection, address):
        Thread.__init__(self)
        self.server = server
        self.connection = connection
        self.address = address
        self.nick = None
        self.daemon = True
        self.start()

    def run(self):
        # Tell the new client who are present
        self.connection.send('Currently online:\n')
        other_clients = [x for x in self.server.clients if x is not self]
        if other_clients:
            longest_nick_length = max(len(client.nick) for client in other_clients)
            for client in other_clients:
                nick = client.nick
                host = client.address[0]
                port = client.address[1]
                space = ' ' * (longest_nick_length + 1 - len(nick))
                self.connection.send('%s%s%s:%d\n' % (nick, space, host, port))
       
        # Ask for a nick
        self.connection.send('What nick would you like to use?\n')
        self.nick = self.connection.makefile().readline().strip('\n')
        
        if self.nick in [client.nick for client in other_clients]:
            self.connection.send('That nick is already in use.\n')
            self.close()
            return
        
        if len(self.nick) > 24:
            self.connection.send('Your nick cannot be longer than 24 characters\n')
            self.close()
            return
        
        # Greet other clients
        host = self.address[0]
        port = self.address[1]
        self.broadcast('New user: %s (%s:%d)\n' % (self.nick, host, port))
        
        # Broadcast every message forever
        while True:
            line = self.connection.makefile().readline()
            if line == '':
                self.broadcast('Quit: %s\n' % self.nick)
                self.close()
                break
            host = self.address[0]
            port = self.address[1]
            self.broadcast('%s: %s' % (self.nick, line))
    
    def close(self):
        self.connection.close()
        self.server.clients.remove(self)

    def broadcast(self, message):
        for client in self.server.clients:
            # Also send message back to the sender
            client.connection.send(message)
