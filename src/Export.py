from shutil import copyfile
from classes import Con
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import NmapScanDB, ConScanDB, LogScanDB
from datetime import datetime

class Export:
    def __init__(self, db_name, base, filename, filetype):
        self.filetype = filetype
        self.filename = filename
        self.db_name = db_name
        self.base = base
        engine = create_engine('sqlite:///%s' % self.db_name)
        self.base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def scan(self):
        if self.filetype == "db":
            try:
                copyfile(self.db_name, "%s.%s" % (self.filename, self.filetype))
                print "File saved to %s.%s" % (self.filename, self.filetype)
            except Exception as e:
                print "ERROR: %s" % e
        elif self.filetype == "csv":
            self.csv()
        elif self.filetype == "pdf":
            self.pdf()
        pass

    def csv(self):
        try:
            conscans = self.session.query(ConScanDB).all()
            portscans = self.session.query(NmapScanDB).all()
            logscans = self.session.query(LogScanDB).all()
            print "File saved to %s.csv" % self.filename
        except Exception as e:
            print "Erro: %s" % e

    def pdf(self):
        try:
            print "File saved to %s.pdf" % self.filename
        except Exception as e:
            print "Erro: %s" % e
