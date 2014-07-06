#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multi_user_server import MultiUserServer

class ChatServer(MultiUserServer):
    
    def __init__(self, port=4681):
        print 'Starting server...'
        MultiUserServer.__init__(self, port)

    def initialize_session(self, client):
        print 'New connection: %s' % client.userhost
        client.nick = None
        
        client.send('This is a primitive chat server designed by Felix Bade.')
        self.tellWhoArePresent(client)
        client.send('What nick would you like to use?')
    
    def handle_line(self, client, line):
        if client.nick is None:
            if self.tryToUseNick(client, line):
                print '%s uses nick %s' % (client.userhost, client.nick)
                self.greetOtherUsers(client)
        else:
            self.broadcastMessage('%s: %s' % (client.nick, line))

    def finish_session(self, client):
        if client.nick is not None:
            for other_client in self.getOtherClients(client):
                other_client.send('Quit: ' + client.userhost)
        print 'Lost connection: %s' % client.userhost

    def tellWhoArePresent(self, client):
        other_clients = self.getOtherClients(client)
        
        if other_clients:
            client.send('Currently online:\n')
            max_nick_length = max(len(x.nick) for x in other_clients)
            for other_client in other_clients:
                space = ' ' * (max_nick_length + 1 - len(other_client.nick))
                client.send('%s%s%s\n' % (other_client.nick, space, other_client.userhost))
        else:
            client.send('Nobody online.\n')

    def tryToUseNick(self, client, potential_nick):
        if potential_nick in [x.nick for x in self.getOtherClients(client)]:
            client.send('That nick is already in use.\n')
            return False
        
        if len(potential_nick) > 24:
            client.send('Your nick cannot be longer than 24 characters\n')
            return False

        client.nick = potential_nick
        return True

    def greetOtherUsers(self, client):
        self.broadcastMessage('New user: %s (%s)\n' % (client.nick, client.userhost))
    
    def broadcastMessage(self, message):
        # Also send message back to the sender
        for receiver in self.clients:
            receiver.send(message)

    def getOtherClients(self, client):
        return [x for x in self.clients if x is not client and x.nick is not None]

