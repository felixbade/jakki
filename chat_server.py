#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multi_user_server import MultiUserServer

class ChatServer(MultiUserServer):
    
    def __init__(self, port=4681):
        print 'Starting server...'
        MultiUserServer.__init__(self, port)

    def initialize_session(self, client):
        print 'New connection: %s' % client.userhost
        client.send('Hello!')
        client.send('Online: ')
        for other_client in self.getOtherClients(client):
            client.send(other_client.userhost)
            other_client.send('Join: ' + client.userhost)
    
    def handle_line(self, client, line):
        print client, line
        for receiver in self.clients:
            receiver.send('<%s> %s' % (client.userhost, line))

    def finish_session(self, client):
        for other_client in self.getOtherClients(client):
            other_client.send('Quit: ' + client.userhost)
        print 'Lost connection: %s' % client.userhost

    def getOtherClients(self, client):
        return [x for x in self.clients if x is not client]
