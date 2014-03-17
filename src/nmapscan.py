#!/usr/bin/python
import nmap
import sys

def main(arg1, arg2):
	nm = nmap.PortScanner()
	nm.scan(arg1, arg2)
	#print nm.scaninfo()
	#print nm.all_hosts()
	for host in nm.all_hosts():
		print('----------------------------------------------------')
		print('Host : %s (%s)' % (host, nm[host].hostname()))
		print('State : %s' % nm[host].state())

		for proto in nm[host].all_protocols():
			print('----------')
			print('Protocol : %s' % proto)

			lport = nm[host][proto].keys()
			lport.sort()
			print "Ports:",
			for port in lport:
				print ('%s (%s), ' % (port, nm[host][proto][port]['state'])),
			print ""


if __name__ == "__main__":
     if len(sys.argv) == 3:
		main(sys.argv[1],sys.argv[2])
     else:        
		print """____________________________
        Usage :
		python code.py ipaddr startport-endport
		python code.py 192.168.1.254 22-443 
		_________________________________"""
		sys.exit()
		       
