#! /usr/bin/python3
import threading
import socket
import csv
import time
with open('/opt/domain', 'r') as file:
    lines = file.read().splitlines()

# Define a function to perform a DNS lookup for a domain
for line in lines:
    domain, uri = line.strip().split()
  
def perform_dns_lookup(domain):
    try:
        ip =  socket.gethostbyname(domain)
        ip = '"' + ip + '"'
        domain = str(domain)
        print("dns_record,domain=" + domain + " ip=" + ip  )
    except socket.gaierror as e:
        print("dns_record,domain=" + domain + " ip=" + ip  )
        
#for line in lines:
#    domain, uri = line.strip().split()
#    perform_dns_lookup(domain) 

threads = []
for line in lines:
    domain, uri = line.strip().split()
    thread = threading.Thread(target=perform_dns_lookup, args=(domain,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
