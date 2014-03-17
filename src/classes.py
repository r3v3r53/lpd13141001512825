# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import hashlib
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IP(Base):
    __tablename__ = 'ip'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
 
class PortScanDB(Base):
    __tablename__ = 'portscan'
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    time = Column(DateTime)
    ip_id = Column(Integer, ForeignKey('ip.id'))
    ip = relationship(IP)

class ConScanDB(Base):
    __tablename__ = 'conscan'
    id = Column(Integer, primary_key=True)
    local_port = Column(Integer, nullable=False)
    remote_port = Column(Integer, nullable=False)
    time = Column(DateTime)
    remote_ip_id = Column(Integer, ForeignKey('ip.id'))
    remote_ip = relationship(IP)

class Con:
    def __init__(self, username, password):
        db = ''.join(chr(ord(a) ^ ord(b))
                     for a,b in zip(username, password))
        m = hashlib.md5()
        m.update(db)
        self.hash = m.hexdigest()
        engine = create_engine('sqlite:///%s.db' % self.hash)
        Base.metadata.create_all(engine)
