from shutil import copyfile
from classes import Con
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import NmapScanDB, ConScanDB, LogScanDB
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

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
            filename = "%s.pdf" % self.filename
            c = canvas.Canvas(filename)
            textobject = c.beginText()
            textobject.setTextOrigin(inch, 10 * inch)
            textobject.setFont("Helvetica-Oblique", 14)
            
            conscans = self.session.query(ConScanDB).all()
            textobject.textLine("LOCAL CONNECTIONS")
            textobject.textLine("[Time], [Local Port], [Remote IP], [Remote Port]")       
            for line in conscans:
		textobject.textLine("%s, %s, %s, %s" % (
                        line.time,
                        line.local_port, 
                        line.remote_ip.ip, 
                        line.remote_port))
            textobject.setFillGray(0.4)

            portscans = self.session.query(NmapScanDB).all()
            textobject.textLine("PORT SCANS")
            textobject.textLine("[Time], [IP], [Protocol], [Port]")       
            for line in portscans:
		textobject.textLine("%s, %s, %s, %s" % (
                        line.time,
                        line.ip.ip, 
                        line.protocol, 
                        line.port))

            logscans = self.session.query(LogScanDB).all()
            textobject.textLine("LOG SCANS")
            textobject.textLine("[Time], [IP], [Event], [Device], [Protocol], [TTL], [Src Port], [Dst Port]")       
            for line in logscans:
		textobject.textLine("%s, %s, %s, %s, %s, %s, %s, %s" % (
                        line.time,
                        line.ipsrc.ip, 
                        line.event_src, 
                        line.device,
                        line.protocol,
                        line.ttl,
                        line.src_port,
                        line.dst_port))

            c.drawText(textobject)
            c.save()
            print "File saved to %s" % filename
        except Exception as e:
            print "Erro: %s" % e
