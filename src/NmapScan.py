#-*-coding: utf-8-*-

import nmap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import IP, NmapScanDB
from datetime import datetime
import GeoIP

class NmapScan:
    '''
    Classe para o sportscans
    '''
    def __init__(self, db_name, base, ip, port):
        '''
        Constructor
        Efectua a ligacao a base de dados fornecida
        e inicia o portscan

        @arg db_name: nome do ficheiro com a base de dados
        @arg base: alchemy declarative_base()
        @arg ip: endereco ou range de ips
        @arg port ou range de ports
        '''
        self.db_name = db_name
        self.base = base
        self.ip = ip
        self.port = port
        engine = create_engine('sqlite:///%s' % self.db_name)
        self.base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.scan()


    def scan(self):
        '''
        Função para efectuar o portscan
        Grava na base de dados o IP 
        com a respectiva georeferencia
        e os resultados obtidos.
        Simultâneamente os mesmos são impressos na consola
        '''
        nm = nmap.PortScanner()
        nm.scan(self.ip, self.port)
        now = datetime.now()
        for host in nm.all_hosts():
            try:
                gi = GeoIP.open('GeoLiteCity.dat', GeoIP.GEOIP_STANDARD)
                geo = gi.record_by_addr(host)
                country_=geo['country_code']
                country_name_=geo['country_name']
                lon_=geo['longitude']
                lat_=geo['latitude']
            except:
                country_ = None
                country_name_ = None
                lon_ = None
                lat_ = None
            finally:
                new_ip = IP(ip=host, 
                        country=country_, 
                        country_name=country_name_,
                        lon=lon_, 
                        lat=lat_)
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
                        print p
                        nmp = NmapScanDB(port=p,
                                         time=now,
                                         protocol=proto,
                                         ip=ip_address)
                        self.session.add(nmp)
        self.session.commit()
