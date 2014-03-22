#!/usr/bin/python
# http://docs.python.org/2/library/argparse.html#choices
import sys, getopt, argparse
import os, sys, getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from classes import Con
from ConScan import ConScan
from NmapScan import NmapScan
from LogScan import LogScan
from Export import Export
 
Base = declarative_base()
'''
Documentacao disto
'''
def main(argv):
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
    parser.add_argument("-export", nargs=2, metavar=('filetype', 'filename'),
                        required=False,
                        help="export database [db, csv, pdf]")
    parser.add_argument("-delete", action="store_true",
                        required=False,
                        help="Delete database")

    args = parser.parse_args()
    password = getpass.getpass('Password:')
    con = Con(args.username, password)
    try:                  
        if args.portscan:
            scan = NmapScan(con.db_name, con.base, args.portscan[0], args.portscan[1])        
        elif args.conscan:
            scan = ConScan(con.db_name, con.base)
        elif args.logscan:
            scan = LogScan(con.db_name, con.base, args.logscan[0])
        elif args.export:
            scan = Export(con.db_name, con.base, args.export[1], args.export[0])
        elif args.delete:
            con.delete()
    finally:
        con.close()

if __name__ == "__main__":
    main(sys.argv[1:])
