#!/usr/bin/python
import sys, getopt, argparse
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from classes import Con
from ConScan import ConScan
from NmapScan import NmapScan
 
Base = declarative_base()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        required=True)
    parser.add_argument("-p", "--password",
                        required=True)
    parser.add_argument("-a", "--action",
                        required=True,
                        choices=["portscan", "conscan", "logscan"],
                        help="Perform a scan for ips in a network")
    parser.add_argument("-ip",
                        required=False,
                        help="IP (or range) toScan")
    parser.add_argument("-ports",
                        required=False,
                        help="Port (or range) to scan")

    args = parser.parse_args()
    con = Con(args.username, args.password)
   
    if args.action == 'portscan':
        scan = NmapScan(con.db_name, con.base, args.ip, args.ports)
        
    elif args.action == 'conscan':
        scan = ConScan(con.db_name, con.base)
        
    try:
        scan.scan()
    finally:
        con.close()

if __name__ == "__main__":
    main(sys.argv[1:])
