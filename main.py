#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

from multi_user_server import MultiUserServer

try:
    port = int(argv[1])
    server = MultiUserServer(port)
except:
    server = MultiUserServer()

server.serve_forever()
