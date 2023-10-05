import ssl
import socket
import datetime
import yaml

# A dictionary to keep track of already checked domains
checked_domains = {}

def check_ssl_cert(domain, port=443):
    try:
        # Create an SSL context
        context = ssl.create_default_context()

        # Connect to the domain and retrieve the SSL certificate
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        # Parse certificate fields
        not_after_str = cert['notAfter']
        not_after = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")

        current_time = datetime.datetime.now()

        # Calculate time to expiry in seconds
        time_to_expiry = (not_after - current_time).total_seconds()

        return domain, "valid" if time_to_expiry > 0 else "expired", int(time_to_expiry)

    except Exception as e:
        return domain, "invalid", str(e)

if __name__ == "__main__":
    with open('domain.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    for entry in config_data:
        domain = entry.get('domain')
        uris = entry.get('uri', [])

        # Check if the domain has already been checked
        if domain not in checked_domains:
            domain_name, validity, time_to_expiry = check_ssl_cert(domain)
            print(f"cert_check,domain={domain_name} verification=" + '"' + f"{validity}" + '"' + f",expiry={int(time_to_expiry)}")

            # Mark the domain as checked
            checked_domains[domain] = True


