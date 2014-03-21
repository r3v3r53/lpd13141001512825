from shutil import copyfile
from classes import Con
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import NmapScanDB, ConScanDB, LogScanDB
from datetime import datetime
import csv

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
        filename = "%s.csv" %self.filename
        try:
            spamWriter = csv.writer(open(filename, 'wb'), delimiter=',',
                                    quotechar='\x22', quoting=csv.QUOTE_MINIMAL)

            conscans = self.session.query(ConScanDB).all()
            spamWriter.writerow(["LOCAL CONNECTIONS"])
            spamWriter.writerow(["[Time]"]
                                + ["[Local Port]"]
                                + ["[Remote IP]"]
                                + ["[Remote Port]"])
            for line in conscans:
                spamWriter.writerow([line.time]
                                    + [line.local_port]
                                    + [line.remote_ip.ip]
                                    + [line.remote_port])

            portscans = self.session.query(NmapScanDB).all()
            spamWriter.writerow(["PORT SCANS"])
            spamWriter.writerow(["[Time]"]
                                + ["[IP]"]
                                + ["[Protocol]"]
                                + ["[Port]"])
            for line in portscans:
                spamWriter.writerow([line.time]
                                    + [line.ip.ip]
                                    + [line.protocol]
                                    + [line.port])

            logscans = self.session.query(LogScanDB).all()
            spamWriter.writerow(["LOG SCANS"])
            spamWriter.writerow(["[Time]"]
                                + ["IP"]
                                + ["[Event]"]
                                + ["[Device]"]
                                + ["[Protocol]"]
                                + ["TTL"]
                                + ["Src Port"]
                                + ["Dst Port"])
            for line in logscans:
                spamWriter.writerow([line.time]
                                    + [line.ipsrc.ip]
                                    + [line.event_src]
                                    + [line.device]
                                    + [line.protocol]
                                    + [line.ttl]
                                    + [line.src_port]
                                    + [line.dst_port])

            print "File saved to %s" % filename
        except Exception as e:
            print "Erro: %s" % e

    def pdf(self):
        try:
            print "File saved to %s.pdf" % self.filename
        except Exception as e:
            print "Erro: %s" % e
