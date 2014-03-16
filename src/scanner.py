#!/usr/bin/python
import sys, getopt, argparse
import os
import sys
import hashlib
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import classes

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
    parser.add_argument("-f", "--filename",
                        required=False,
                        help="Filename to save")
    parser.add_argument("-ip",
                        required=False,
                        help="IP to Port Scan")
    parser.add_argument("-g", "--group",
                        required=False,
                        help="How info is to be grouped in the report")
    parser.add_argument("-s", "--start",
                        required=False,
                        help="Port or IP to start")
    parser.add_argument("-e", "--end",
                        required=False,
                        help="Port or IP to end")
    args = parser.parse_args()


    
    if args.action == 'portscan':
        print "Starting Portscan:", args.start, "-", args.end

if __name__ == "__main__":
    main(sys.argv[1:])
