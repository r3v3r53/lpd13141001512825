import psutil
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import IP, ConScanDB
from datetime import datetime

class ConScan:
    def __init__(self, db_name, base):
        self.db_name = db_name
        self.base = base
        engine = create_engine('sqlite:///%s' % self.db_name)
        self.base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def scan(self):
        print "Starting Scan for local Connections"
        AF_INET6 = getattr(socket, 'AF_INET6', object())
        proto_map = {(AF_INET, SOCK_STREAM)  : 'TCP',
                     (AF_INET6, SOCK_STREAM) : 'TCP6',
                     (AF_INET, SOCK_DGRAM)   : 'UDP',
                     (AF_INET6, SOCK_DGRAM)  : 'UDP6'}
        for p in psutil.process_iter():
            program = p.name
            con = p.get_connections(kind='inet')

            for c in con:

                if len(c.raddr) > 0:
                    new_ip = IP(ip=c.raddr[0])
                    #check if ip address is in database
                    ip = self.session.query(IP).filter_by(ip=c.raddr[0]).first()

                    if ip == None:
                        self.session.add(new_ip)
                        ip = new_ip

                    con = ConScanDB(local_port=c.laddr[1], remote_port=c.raddr[1],
                        time=datetime.now(), remote_ip=ip)
                    self.session.add(con)
                    print "Local Port: %s, Remote IP: %s, Remote Port: %s, Status: %s, Name: %s, Pid: %s" % (c.laddr[1], c.raddr[0], c.raddr[1], c.status, p.name(), p.pid)
        self.session.commit()
