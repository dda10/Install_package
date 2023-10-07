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
    threads = []
    with open('domain.yml', 'r') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Iterate through domains and URIs
    for domain_data in data['domains']:
        domain = domain_data['domain']
        thread = threading.Thread(target=perform_dns_lookup, args=(domain,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

