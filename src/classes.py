# -*- coding: utf-8 -*-
# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
#
# http://stackoverflow.com/questions/20852664/python-pycrypto-encrypt-decrypt-text-files-with-aes 
# pip install -U setuptools
# https://github.com/maxmind/geoip-api-python
# apt-get install libgeoip-dev --> https://trac.torproject.org/projects/tor/ticket/10625
# https://github.com/maxmind/geoip-api-python/blob/master/README.rst
# http://www.pip-installer.org/en/latest/installing.html#install-or-upgrade-pip
'''
Network Security Application Database classes
A base de dados é gerada com auxílio do Alchemy
O nome da base de dados é criada a partir 
do username e password fornecidos.
Caso o ficheiro exista, este é decifrado para ser utilizado
no final das operações deve ser cifrado de novo

@author Pedro Moreira
@author João Carlos Mendes
@date 20140323

''' 
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from sqlalchemy.ext.declarative import declarative_base
from os import remove

Base = declarative_base()

class IP(Base):
    '''
    Classe para a criação da tabela IP
    Armazena os endereços ip relacionados 
    com todos os scans efectuados
    '''
    __tablename__ = 'ip'
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False, unique=True)
    country = Column(String(5))
    country_name = Column(String(50))
    lon = Column(String(50))
    lat = Column(String(50))

class LogScanDB(Base):
    '''
    Classe para a criação da tabela logscan
    Armazena todos os logscan efectuados
    '''
    __tablename__ = 'logscan'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    ipsrc_id = Column(Integer, ForeignKey('ip.id',
                                            onupdate="CASCADE",
                                            ondelete="CASCADE"))
    event_src = Column(String(10))
    device = Column(String(5))
    protocol = Column(String(10))
    ttl = Column(Integer)
    src_port = Column(Integer)
    dst_port = Column(Integer)
    ipsrc = relationship(IP)
    
class ConScanDB(Base):
    '''
    Classe para a criação da tabela conscan
    Armazena todas as conecções existentes na máquina local
    '''
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
    '''
    Classe para a criação da tabela portscan
    Armazena todos os portscan efectuados
    '''
    __tablename__ = 'portscan'
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    time = Column(DateTime)
    protocol = Column(String(15))
    ip_id = Column(Integer, ForeignKey('ip.id',
                                       onupdate="CASCADE",
                                       ondelete="CASCADE"))
    ip = relationship(IP)

class Con:
    '''
    Classe para gerir a ligação à base de dados
    @arg username
    @arg password
    '''
    def __init__(self, username, password):
        '''
        Constructor:
        gera o hash md5 do username e da password
        de seguida é efectuado o XOR entre os dois hashes
        o resultado desta operação é o nome utilizado
        para a base de dados do utilizador.
        A base de dados é então decifrada com a password fornecida
        '''
        self.deleted = False
        self.base = Base
        u = hashlib.md5()
        u.update(username)
        self.username = u.hexdigest()
        p = hashlib.md5()
        p.update(password)
        self.password = p.hexdigest()
        # XOR entre os hash md5 do username e password
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
        engine = create_engine('sqlite:///%s' % self.db_name)
        Base.metadata.create_all(engine)

    def pad(self, s):
        '''
        preencher string para ter o tamanho da chave 
        a utilizar para a cifra

        @arg s: string a converter
        @return string com o tamanho da chave a utilizar
        '''
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        '''
        função para cifrar um texto com aes-cbc

        @arg message: texto a cifrar
        @arg key: chave para cifra
        @arg key_size: tamanho da cifra (256 por default)
        @return texto cifrado
        '''
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        '''
        função para decifrar um texto com aes-cbc

        @arg message: texto a decifrar
        @arg key: chave para decifrar
        @return texto decifrado
        '''
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    
    def encrypt_file(self, file_name, key):
        '''
        função para cifrar um ficheiro com aes-cbc

        @arg file_name: ficheiro a cifrar
        @arg key: chave para cifrar
        '''
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, key)
        with open(file_name, 'wb') as fo:
            fo.write(enc)

    def decrypt_file(self, file_name, key):
        '''
        função para decifrar um ficheiro com aes-cbc

        @arg file_name: ficheiro a decifrar
        @arg key: chave para decifrar
        '''
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, key)
        with open(file_name, 'wb') as fo:
            fo.write(dec)        

    def close(self):
        '''
        função utilizada para cifrar a base de dados,
        caso esta não tenha sido eliminada
        Esta função deve ser chamada 
        no final da execução do programa
        '''
        if self.deleted == False:
            self.encrypt_file(self.db_name, self.password)
        pass

    def delete(self):
        '''
        função utilizada para eliminar a base de dados
        '''
        try:
            remove(self.db_name)
            self.deleted = True
        except Exception as e:
            print "Erro: %s" % e
