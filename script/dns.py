#!/usr/bin/python3 
import threading
import sys
import socket
import yaml

#yaml_file = sys.argv[1]

def perform_dns_lookup(domain,yaml_file):
    try:
        ip = socket.gethostbyname(domain)
        ip = '"' + ip + '"'
        domain = str(domain)
        print("dns_record,domain=" + domain + " ip=" + ip)
    except socket.gaierror as e:
        print("dns_record,domain=" + domain + " ip=not_resolved")

if __name__ == "__main__":
    threads = []
    yaml_file = sys.argv[1] 
    with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)

    for entry in config:
        domain = entry['domain']
        thread = threading.Thread(target=perform_dns_lookup, args=(domain,yaml_file))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
