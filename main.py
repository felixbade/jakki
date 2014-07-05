#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

from client_handler import ClientHandler

class MultiUserServer:

    def __init__(self, port=4681):
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', port))
        print 'Starting server... (listening on port %d)' % port
        self.socket.listen(10)

        while True:
            connection, address = self.socket.accept()
            new_client = ClientHandler(self, connection, address)
            self.clients.append(new_client)
    
MultiUserServer()
