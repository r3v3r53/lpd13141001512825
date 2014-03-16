# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class IP(Base):
    __tablename__ = 'ip'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
 
class PortScan(Base):
    __tablename__ = 'portscan'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    time = Column(DateTime)
    ip_id = Column(Integer, ForeignKey('ip.id'))
    ip = relationship(IP)


db = ''.join(chr(ord(a) ^ ord(b))
             for a,b in zip(username, password))
m = hashlib.md5()
m.update(db)

engine = create_engine('sqlite:///%s.db' % (m.hexdigest()))
Base.metadata.create_all(engine)
