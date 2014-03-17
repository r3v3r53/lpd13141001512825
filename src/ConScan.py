import psutil
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from classes import IP, ConScanDB

class ConScan:
    def scan(self):
        AF_INET6 = getattr(socket, 'AF_INET6', object())
        proto_map = {(AF_INET, SOCK_STREAM)  : 'TCP',
                                  (AF_INET6, SOCK_STREAM) : 'TCP6',
                                  (AF_INET, SOCK_DGRAM)   : 'UDP',
                                  (AF_INET6, SOCK_DGRAM)  : 'UDP6'}
        for p in psutil.process_iter():
            program = p.name
            con = p.get_connections(kind='inet') #or all
            for c in con:
                if len(c.raddr) > 0:
                    print "Local Port: %s, Remote IP: %s, Remote Port: %s, Status: %s, Name: %s, Pid: %s" % (c.laddr[1], c.raddr[0], c.raddr[1], c.status, p.name(), p.pid)
