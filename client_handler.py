#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from threading import Thread

class ClientHandler(Thread):

    def __init__(self, server, connection, address):
        Thread.__init__(self)
        self.server = server
        self.connection = connection
        self.host = address[0]
        self.port = address[1]
        self.nick = None
        self.other_clients = [x for x in self.server.clients if x is not self]
        self.daemon = True
        self.start()
        print 'New client from %s:%d' % address

    def run(self):
        try:
            self.tellWhoArePresent()
           
            self.askForANick()
            if self.nick is None:
                return
            
            self.greetOtherUsers()
            
            # Broadcast every message
            while True:
                line = self.connection.makefile().readline()
                if line == '':
                    self.broadcast('Quit: %s\n' % self.nick)
                    break
                self.broadcast('%s: %s' % (self.nick, line))
        except Exception as e:
            if repr(e) == "error(54, 'Connection reset by peer')":
                pass
            else: 
                traceback.print_exc()
        self.close()
  
    def tellWhoArePresent(self):
        if self.other_clients:
            self.connection.send('Currently online:\n')
            max_nick_length = max(len(client.nick) for client in self.other_clients)
            for client in self.other_clients:
                space = ' ' * (max_nick_length + 1 - len(client.nick))
                self.connection.send('%s%s%s:%d\n' % (client.nick, space, client.host, client.port))
        else:
            self.connection.send('Nobody online.\n')

    def askForANick(self):
        self.connection.send('What nick would you like to use?\n')
        potential_nick = self.connection.makefile().readline().strip('\n')
        
        if potential_nick in [client.nick for client in self.other_clients]:
            self.connection.send('That nick is already in use.\n')
            self.close()
            return
        
        if len(potential_nick) > 24:
            self.connection.send('Your nick cannot be longer than 24 characters\n')
            self.close()
            return

        self.nick = potential_nick
        print '(%s:%d) uses nick %s' % (self.host, self.port, self.nick)

    def greetOtherUsers(self):
        self.broadcast('New user: %s (%s:%d)\n' % (self.nick, self.host, self.port))

    def close(self):
        self.server.clients.remove(self)
        self.connection.close()
        if self.nick is not None:
            print 'Client exited from %s:%d (%s)' % (self.host, self.port, self.nick)
        else:
            print 'Client exited from %s:%d' % (self.host, self.port)

    def broadcast(self, message):
        for client in self.server.clients:
            # Also send message back to the sender
            client.connection.send(message)
