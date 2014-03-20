#!/usr/bin/python
# ver ArgumentParser.add_subparsers
# http://docs.python.org/2/library/argparse.html#choices
import sys, getopt, argparse
import os
import sys
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        required=True)
    parser.add_argument("-p", "--password",
                        required=True)
    parser.add_argument("-a", "--action",
                        required=True,
                        choices=["portscan", "conscan", "logscan", "export"],
                        help="Perform a scan for ips in a network")
    parser.add_argument("-ip",
                        required=False,
                        help="IP (or range) toScan")
    parser.add_argument("-ports",
                        required=False,
                        help="Port (or range) to scan")
    parser.add_argument("-f", "--file",
                        required=False,
                        help="Log File to scan")
    parser.add_argument("-t", "--type",
                        required=False,
                        help="Type of export (pdf, csv or db)")
    parser.add_argument("-filename", nargs=2, metavar=('name','type'),
                        required=False,
                        help="File name and type to export")
                        

    args = parser.parse_args()
    con = Con(args.username, args.password)
   
    if args.action == 'portscan':
        scan = NmapScan(con.db_name, con.base, args.ip, args.ports)
        
    elif args.action == 'conscan':
        scan = ConScan(con.db_name, con.base)

    elif args.action == 'logscan':
        scan = LogScan(con.db_name, con.base, args.file)
    elif args.action == 'export':
        print args.filename
        scan = Export(con.db_name, args.type, args.filename)
    try:
        scan.scan()
    finally:
        con.close()

if __name__ == "__main__":
    main(sys.argv[1:])
