#!/usr/bin/python
import nmap
import sys

def main(arg1, arg2):

	nm = nmap.PortScanner()
	nm.scan(arg1, arg2)
	nm.scaninfo()
	nm.all_hosts()
	print nm.all_hosts()
	
	for host in nm.all_hosts():
		print ('%s (%s)' % (host, nm[host].hostname() ) )
		for proto in nm[host].all_protocols():
			print ( 'Protocol: %s' % (proto) )
			lport = nm[host][proto].keys()
			lport.sort()
			for port in lport:
				print "port:", port, type(port)
				print """__________________________________
				Host: %s (%s)' - %s
				Protocol: %s
				Port: %s - %s'
				__________________________________"
				"""%(host, nm[host].hostname(), nm[host].state(),protocol,port,nm[host][protocol][port]['state'])

if __name__ == "__main__":
     if len(sys.argv) == 3:
		main(sys.argv[1],sys.argv[2])
     else:        
		print """____________________________
        Usage :
		python code.py ipaddr startport-endport
		python code.py 120.0.0.1 22-443
		_________________________________"""
		sys.exit()
		       
