# http://stackoverflow.com/questions/9370699/how-to-split-reportlab-table-across-pdf-page-side-by-side
from shutil import copyfile
from classes import Con
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import NmapScanDB, ConScanDB, LogScanDB
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
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

            doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
            elements = []
            styles=getSampleStyleSheet()
            styleN = styles["Normal"]

            scans = self.session.query(ConScanDB).all()
            data = [["LOCAL CONNECTIONS"]]
            elements.append(self.drawTable(data, 1))

            data = [["Time","Local Port", "Remote IP", "Remote Port"]]
            for line in scans:
		data.append([line.time,
                             line.local_port, 
                             line.remote_ip.ip, 
                             line.remote_port])
            elements.append(self.drawTable(data))


            scans = self.session.query(NmapScanDB).all()
            data = [["PORT SCANS"]]
            elements.append(self.drawTable(data, 1))

            data = [["Time","IP", "Protocol", "Port"]]
            for line in scans:
		data.append([line.time,
                             line.ip.ip, 
                             line.protocol, 
                             line.port])
            elements.append(self.drawTable(data))


            scans = self.session.query(LogScanDB).all()
            data = [["LOG SCANS"]]
            elements.append(self.drawTable(data, 1))

            data = [["Time","IP", "Evt", "Dev", "Proto", "TTL", "SrcPrt", "DstPrt"]]
            for line in scans:
		data.append([line.time,
                             line.ipsrc.ip, 
                             line.event_src, 
                             line.device,
                             line.protocol,
                             line.ttl,
                             line.src_port,
                             line.dst_port])
            elements.append(self.drawTable(data))
            doc.build(elements)
            print "File saved to %s" % filename
        except Exception as e:
            print "Erro: %s" % e


    def drawTable(self, data, blank = 0):
        result = Table(data,  repeatRows=1)
        result.hAlign = 'LEFT'
        if blank == 1:
            tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                                   ('VALIGN',(0,0),(-1,-1),'TOP')])
            pass
        else:
            tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                                   ('VALIGN',(0,0),(-1,-1),'TOP'),
                                   ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                                   ('INNERGRID',(0,0),(-1,-1),1,colors.black),
                                   ('BOX',(0,0),(-1,-1),1,colors.black)])
            tblStyle.add('BACKGROUND',(0,0),(-1,-1),colors.lightblue)
            tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
            
        result.setStyle(tblStyle)
        return result

'''
            portscans = self.session.query(NmapScanDB).all()
            textobject.textLine("PORT SCANS")
            textobject.textLine("[Time], [IP], [Protocol], [Port]")       
            for line in portscans:
		textobject.textLine("%s, %s, %s, %s" % (
                        line.time,
                        line.ip.ip, 
                        line.protocol, 
                        line.port))
            c.drawText(textobject)
            c.showPage()

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
            c.showPage()
            c.save()
'''
