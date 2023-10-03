#! /usr/bin/python3
import threading
import socket
import csv
import time
with open('/opt/domain', 'r') as file:
    domains = file.read().splitlines()

# Define a function to perform a DNS lookup for a domain
def perform_dns_lookup(domain):
    try:
        timestamp = int(time.time())
        ip =  socket.gethostbyname(domain)
        ip = '"' + ip + '"'
        domain = str(domain)
        print("dns_record,domain=" + domain + " ip=" + ip  )
    except socket.gaierror as e:
        print(f"Error looking up IP for {domain}: {e}")

# Create a thread for each domain and start them
threads = []
for domain in domains:
    thread = threading.Thread(target=perform_dns_lookup, args=(domain,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
