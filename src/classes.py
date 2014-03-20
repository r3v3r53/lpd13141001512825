# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
#
# http://stackoverflow.com/questions/20852664/python-pycrypto-encrypt-decrypt-text-files-with-aes 
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IP(Base):
    __tablename__ = 'ip'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False, unique=True)
 
class PortScanDB(Base):
    __tablename__ = 'portscan'
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    time = Column(DateTime)
    ip_id = Column(Integer, ForeignKey('ip.id', 
                                       onupdate="CASCADE", 
                                       ondelete="CASCADE"))
    ip = relationship(IP)

class LogScanDB(Base):
    __tablename__ = 'logscan'
    id = Column(Integer, primary_key=True)
    local_port = Column(Integer, nullable=False)
    remote_port = Column(Integer, nullable=False)
    time = Column(DateTime)
    remote_ip_id = Column(Integer, ForeignKey('ip.id',
                                              onupdate="CASCADE",
                                              ondelete="CASCADE"))
    remote_ip = relationship(IP)
    
class ConScanDB(Base):
    __tablename__ = 'conscan'
    id = Column(Integer, primary_key=True)
    local_port = Column(Integer, nullable=False)
    remote_port = Column(Integer, nullable=False)
    time = Column(DateTime)
    remote_ip_id = Column(Integer, ForeignKey('ip.id',
                                              onupdate="CASCADE",
                                              ondelete="CASCADE"))
    remote_ip = relationship(IP)

class NmapScanDB(Base):
    __tablename__ = 'nmapscan'
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    time = Column(DateTime)
    protocol = Column(String(15))
    ip_id = Column(Integer, ForeignKey('ip.id',
                                       onupdate="CASCADE",
                                       ondelete="CASCADE"))
    ip = relationship(IP)

class Con:
    def __init__(self, username, password):
        self.base = Base
        u = hashlib.md5()
        u.update(username)
        self.username = u.hexdigest()
        p = hashlib.md5()
        p.update(password)
        self.password = p.hexdigest()

        db = ''.join(chr(ord(a) ^ ord(b))
                     for a,b in zip(self.username, self.password))
        m = hashlib.md5()
        m.update(db)
        self.hash = m.hexdigest()
        self.db_name = '%s.db' % self.hash
        
        try:
            self.decrypt_file(self.db_name, self.password)
        except:
            pass
        print self.db_name
        engine = create_engine('sqlite:///%s' % self.db_name)
        Base.metadata.create_all(engine)

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    
    def encrypt_file(self, file_name, key):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, key)
        with open(file_name, 'wb') as fo:
            fo.write(enc)

    def decrypt_file(self, file_name, key):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, key)
        with open(file_name, 'wb') as fo:
            fo.write(dec)

    def close(self):
        self.encrypt_file(self.db_name, self.password)
        pass
