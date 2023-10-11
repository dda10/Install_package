import socket
import yaml
from scapy.all import *

def traceroute_tcp(ip_backend, max_hops=30, dest_port=443):
    result = []
    for ttl in range(1, max_hops + 1):
        times = []
        for _ in range(3):  # Send 3 packets per hop
            pkt = IP(dst=ip_backend, ttl=ttl) / TCP(dport=dest_port, flags="S")
            start_time = time.time()
            reply = sr1(pkt, verbose=0, timeout=2)
            end_time = time.time()

            if reply is not None:
                times.append((end_time - start_time) * 1000)  # Calculate round-trip time in milliseconds

        if not times:
            result.append({
                'hop': ttl,
                'ip': '*',
                'avg': 0,
                'loss': 100,
                'status': 'Timeout',
            })
        else:
            result.append({
                'hop': ttl,
                'ip': reply.src,
                'avg': sum(times) / len(times),  # Calculate the average
                'loss': 0,
                'status': 'OK',
            })

            if reply.src == ip_backend:
                break

    return result

if __name__ == '__main__':
    yaml_file = sys.argv[1]
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    for entry in config:
        domain = entry['domain']
        ip_backend = entry['ip_backend']
        traceroute_result = traceroute_tcp(ip_backend)
        for entry in traceroute_result:

            if entry["avg"] != 0:
                avg_str = f'{entry["avg"]:.2f}ms'
            else:
                avg_str = '0'
            print(f'mtr,domain={domain},ip_backend={ip_backend},hop={entry["hop"]},ip={entry["ip"]} avg={avg_str},loss={entry["loss"]},status="{entry["status"]}"')
