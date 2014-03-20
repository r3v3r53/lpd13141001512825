#!/usr/bin/python
import nmap
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


    def scan(self):
        pass
