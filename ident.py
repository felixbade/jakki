#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For IDENT protocol documentation, see
# https://www.ietf.org/rfc/rfc1413.txt

import socket

def getIdent(remote_address, local_port, timeout=30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((remote_address[0], 113)) # identd default port
        s.send('%d, %d\n' % (remote_address[1], local_port))
        response = s.makefile().readline()
        s.close()

        response = response.split(':')
        if response[1] == 'USERID':
            user = ':'.join(response[3:])
            user = user.replace('\0', '')
            user = user.replace('\n', '')
            user = user.replace('\r', '')
            user = user.replace(' ', '')
            return user
    except:
        return None
