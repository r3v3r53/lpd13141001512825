import psutil
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

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
                print c
                continue
                print c.local_address
                remoteaddr = ""
                if c.remote_address:
                    raddr = "%s:%s" % (c.remote_address)
                    print("%-8s %-22s %-22s %-13s %-6s %s"% (proto_map[(c.family, c.type)],localaddr,remoteaddr,str(c.status),p.pid,program[:15]))
                                                                                                    
