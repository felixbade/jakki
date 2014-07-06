#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server_listener import ServerListener

class MultiUserServer:

    def __init__(self, port=0):
        self.running = False
        self.port = port
        self.clients = []
        self.listener = ServerListener(self)

    def set_port(self, port):
        if not self.running:
            self.port = port

    def run(self):
        self.running = True
        self.listener.serve_forever()

    def new_connection(self, client):
        self.clients.append(client)
        self.initialize_session(client)

    def initialize_session(self, client):
        pass

    def handle_line(self, client, line):
        pass
    
    def close_connection(self, client):
        self.finish_session(client)
        client.close_connection()
        self.clients.remove(client)

    def finish_session(self, client):
        pass
    
    def stop(self):
        print '\nStopping server...'
        for client in self.clients:
            client.close_connection()
        self.running = False
