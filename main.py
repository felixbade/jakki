#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import atexit

from client_handler import ClientHandler

class ChatServer:

    def __init__(self):
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 4681))
        self.socket.listen(10)

        while True:
            connection, address = self.socket.accept()
            print 'Connection from %s:%d' % address
            new_client = ClientHandler(self, connection, address)
            self.clients.append(new_client)
    
print 'Starting server... (listening on port 4681)'
server = ChatServer()
