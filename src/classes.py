# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
#
# Parte de tentar cifrar / decifrar a bd
# http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import hashlib
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
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

class Con:
    def __init__(self, username, password):
        self.base = Base
        db = ''.join(chr(ord(a) ^ ord(b))
                     for a,b in zip(username, password))
        m = md5()
        m.update(db)
        p = md5(password)
        self.psw = p.hexdigest()
        self.hash = m.hexdigest()
        self.db_name = '%s.db' % self.hash
        with open(self.db_name, 'rb') as in_file, open(self.db_name, 'wb') as out_file:
            decrypt(in_file, out_file, psw)
        engine = create_engine('sqlite:///%s.db' % self.hash)
        Base.metadata.create_all(engine)

    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(in_file, out_file, password, key_length=256):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))
            
    def decrypt(in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
        out_file.write(chunk)

    def close(self):
        with open(self.db_name, 'rb') as in_file, open(self.db_name, 'wb') as out_file:
            encrypt(in_file, out_file, self.psw)

