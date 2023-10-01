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
        ip_addresses = socket.gethostbyname_ex(domain)
        ip_list = ', '.join(ip_addresses[2])
        print(f"dns_record,domain={domain},ip={ip_list} {timestamp}")
    except socket.gaierror as e:
        print(f"Error looking up IP for {domain}: {e}")

# List of domains to perform DNS lookup on
#domains = ["example.com", "google.com", "github.com"]  # Add as many domains as needed

# Create a thread for each domain and start them
threads = []
for domain in domains:
    thread = threading.Thread(target=perform_dns_lookup, args=(domain,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
