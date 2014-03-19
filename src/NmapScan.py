#!/usr/bin/python
import nmap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import IP, NmapScanDB
from datetime import datetime


class NmapScan:
    def __init__(self, db_name, base, ip, port):
        self.db_name = db_name
        self.base = base
        self.ip = ip
        self.port = port
        engine = create_engine('sqlite:///%s' % self.db_name)
        self.base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def scan(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip, self.port)
        for host in nm.all_hosts():
            new_ip = IP(ip=host)
            #check if ip address is in database
            ip_address = self.session.query(IP).filter_by(ip=host).first()

            if ip_address == None:
                self.session.add(new_ip)
                ip_address = new_ip


		print('----------------------------------------------------')
		print('Host : %s (%s)' % (host, nm[host].hostname()))
		print('State : %s' % nm[host].state())

		for proto in nm[host].all_protocols():
                    if proto in ['tcp', 'udp']:
			print('----------')
			print('Protocol : %s' % proto)

			lport = nm[host][proto].keys()
			lport.sort()
			print "Ports:"
			for p in lport:
                            print port
                            nmap = NmapScanDBDB(port=p,
                                                time=now,
                                                protocol=proto,
                                                ip=ip_address)
                            self.session.add(nmap)
