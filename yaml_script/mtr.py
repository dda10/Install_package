import argparse
import socket
import scapy.all as scapy
import yaml

def send_packet(target_ip, ttl):
    # Create an ICMP packet with the specified TTL
    packet = scapy.IP(dst=target_ip, ttl=ttl) / scapy.ICMP()

    # Send the packet and wait for a response
    reply = scapy.sr1(packet, verbose=False, timeout=1)

    if reply:
        # Calculate round-trip time (RTT) in milliseconds
        rtt_ms = reply.time * 1000
        return {
            'hop': ttl,
            'ip': target_ip,
            'avg': rtt_ms,
            'best': rtt_ms,
            'worst': rtt_ms,
            'loss': 0,  # Assuming no loss for simplicity
            'status': 'OK'
        }
    else:
        return {
            'hop': ttl,
            'ip': target_ip,
            'avg': 0,  # Set average RTT to 0 for non-responsive hops
            'best': 0,
            'worst': 0,
            'loss': 100,  # Set loss to 100% for non-responsive hops
            'status': 'UNREACHABLE'
        }

def mtr(target_ip, max_hops):
    results = []

    for ttl in range(1, max_hops + 1):
        result = send_packet(target_ip, ttl)
        results.append(result)

    return results
  
def main():
    parser = argparse.ArgumentParser(description='Python MTR (My Traceroute) Script')
    parser.add_argument('-c', '--config', default='config.yaml', help='YAML configuration file (default: config.yaml)')
    parser.add_argument('-m', '--max-hops', type=int, default=30, help='Maximum number of hops to trace (default: 30)')
    args = parser.parse_args()

    try:
        with open('domain.yaml', 'r') as file:
            config_data = yaml.safe_load(file)

        for entry in config_data:
            domain = entry.get('domain', '')
            uris = entry.get('uri', [])

            if domain:
                try:
                    target_ip = socket.gethostbyname(domain)
                    for uri in uris:
                        results = mtr(target_ip, args.max_hops)
                        for result in results:
                            print(f'mtr,dest={domain},hop={result["hop"]},ip={result["ip"]} avg={result["avg"]:.2f},best={result["best"]:.2f},worst={result["worst"]:.2f},loss={result["loss"]},status="{result["status"]}"')
                except socket.gaierror:
                    print(f'Unable to resolve target host: {domain}')
    except Exception as e:
        print(f"Error reading YAML file: {e}")

if __name__ == '__main__':
    main()
