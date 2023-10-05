import threading
import socket
import yaml

# Initialize a set to keep track of already resolved domains
resolved_domains = set()

def perform_dns_lookup(domain):
    try:
        # Check if the domain has already been resolved
        if domain not in resolved_domains:
            ip = socket.gethostbyname(domain)
            resolved_domains.add(domain)  # Add the domain to the set of resolved domains
            ip = '"' + ip + '"'
            domain = str(domain)
            print("dns_record,domain=" + domain + " ip=" + ip)
        else:
            print("dns_record,domain=" + domain + " ip=already_resolved")
    except socket.gaierror as e:
        print("dns_record,domain=" + domain + " ip=not_resolved")

if __name__ == "__main__":
    # Read domains and URIs from a YAML file
    with open('domain.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    # Create threads for DNS lookups
    threads = []
    for entry in config_data:
        domain = entry.get('domain')
        thread = threading.Thread(target=perform_dns_lookup, args=(domain,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

