#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

from chat_server import ChatServer

server = ChatServer()

try:
    server.set_port(int(argv[1]))
except ValueError:
    pass
except IndexError:
    pass

try:
    server.run()
except KeyboardInterrupt:
    server.stop()
