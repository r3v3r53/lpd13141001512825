#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://docs.python.org/2/library/argparse.html#choices
'''
Network Security Application

USAGE:

./scanner.py -u <username> -portscan <ip ports>
./scanner.py -u <username> -conscan
./scanner.py -u <username> -logscan <logfile>
./scanner.py -u <username> -export <filename type:[bd, pdf, csv]>
./scanner.py -u <username> -delete

@author Pedro Moreira
@author João Carlos Mendes
@date 20140323

'''
import sys, getopt, argparse, os, getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from classes import Con
from ConScan import ConScan
from NmapScan import NmapScan
from LogScan import LogScan
from Export import Export
 
Base = declarative_base()
def main(argv):
    """
    Fazer o parse dos argumentos fornecidos pelo user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        required=True)
    parser.add_argument("-portscan", nargs=2, metavar=('ip', 'ports'),
                        required=False,
                        help="Perform a portscan")
    parser.add_argument("-conscan", action='store_true',
                        required=False,
                        help="Scan for local connections")
    parser.add_argument("-logscan", nargs=1, metavar=('file'),
                        required=False,
                        help="Store log connections into database")
    parser.add_argument("-export", nargs=2, metavar=('filename', 'filetype'),
                        required=False,
                        help="export database [db, csv, pdf]")
    parser.add_argument("-delete", action="store_true",
                        required=False,
                        help="Delete database")

    args = parser.parse_args()
    #Solicitar password
    password = getpass.getpass('Password:')
    # Fazer ligação à base de dados
    con = Con(args.username, password)
    try:                  
        if args.portscan:
            scan = NmapScan(con.db_name, con.base, args.portscan[0], args.portscan[1])        
        elif args.conscan:
            scan = ConScan(con.db_name, con.base)
        elif args.logscan:
            scan = LogScan(con.db_name, con.base, args.logscan[0])
        elif args.export:
            scan = Export(con.db_name, con.base, args.export[0], args.export[1])
        elif args.delete:
            con.delete()
    finally:
        # A ligação à base de dados tem de ser sempre fechada 
        # para que esta volte a ser cifrada 
        con.close()

if __name__ == "__main__":
    main(sys.argv[1:])
