#!/usr/bin/python
import re
from pygeoip import GeoIP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import IP, LogScanDB
from datetime import datetime


class LogScan:
    def __init__(self, db_name, base, logfile):
        self.db_name = db_name
        self.base = base
        self.logfile = logfile
        engine = create_engine('sqlite:///%s' % self.db_name)
        self.base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.logfile = logfile
        self.gic = GeoIP('GeoIP.dat')
        self.giv6 = GeoIP('GeoIP.dat')


    def scan(self):
        try:
            logfile = open(self.logfile, 'r')
            self.parse(logfile)
            self.session.commit()
        except Exception, e:
            print "[-] " + str(e)
            

    def parse(self, logfile):
        for line in logfile.readlines():
            debug = 0
            if not re.search("SRC=192", line) and not re.search("SRC=0", line) and not re.search("SRC=172", line):
            #IP SRC
                lista = line.split("SRC=")
                ip_src = lista[1].split(' ')[0]
            #DATA
                lineMonth = str(line)
                dataT = lineMonth[:15]
            #INTERFACE
                device = line.split("IN=")
                dInterface = device[1].split(' ')[0]
                if (str(dInterface) ==""):
                    device = line.split("OUT=")
                    dInterface = device[1].split(' ')[0]
                #EVENT SOURCE
                    event = line.split("IN= ")
                    eventSrc = event[1].split('=')[0]
                else:
                    eventSrc = "IN"

            #PROTO
                proto=line.split("PROTO=")
                protoInf=proto[1].split(' ')[0]

                try:
                    
                    if len(ip_src)<=15:
                    #SOURCE PORT
                        spt=line.split("SPT=")
                        sptPort=spt[1].split(' ')[0]
                    #DESTINATION PORT
                        dpt=line.split("DPT=")
                        dptPort=dpt[1].split(' ')[0]
                        #data=self.gic.record_by_addr(IP)
                        #cty = data['country_code']
                        #ctyName =data['country_name']
                        #longitude = data['longitude']
                        #latitude = data['latitude']
                        ttlinf=line.split("TTL=")
                        ttlData=str(ttlinf[1].split(' ')[0])
                    else:
                        #cty=self.giv6.country_code_by_addr_v6(IP)
                        pass
                    
                    new_ip = IP(ip=ip_src)
            #check if ip address is in database
                    ip_address = self.session.query(IP).filter_by(ip=ip_src).first()

                    if ip_address == None:
                        self.session.add(new_ip)
                        ip_address = new_ip

                    log = LogScanDB(
                        time = datetime.strptime(dataT, "%b %d %H:%M:%S"),
                        ipsrc = ip_address,
                        event_src = eventSrc,
                        device = dInterface,
                        protocol = protoInf,
                        ttl = ttlData,
                        src_port = sptPort,
                        dst_port = dptPort,
                        country = '',#cty,
                        country_name = '',#ctyName,
                        lon = '',#longitude,
                        lat = ''#latitude
                        )
                    self.session.add(log)
                except Exception as e:
                    print e
