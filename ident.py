#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

def getIdent(remote_ip, remote_port, local_port, timeout=30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((remote_ip, 113)) # identd default port
        s.send('%d, %d\n' % (remote_port, local_port))
        response = s.makefile().readline()
        s.close()

        if response.split(':')[1] == 'USERID':
            user = ':'.join(response.split(':')[3:]).replace('\n', '')
            user = user.replace('\0', '')
            user = user.replace('\n', '')
            user = user.replace('\r', '')
            user = user.replace(' ', '')
            return user
    except:
        return None