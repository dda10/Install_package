#!/usr/bin/python3 
import sys
import socket
import time
import yaml
from scapy.all import *

def tcp_traceroute(target_host, max_hops=30, timeout=2):
    for ttl in range(1, max_hops + 1):
        total_rtt = 0
        successful_probes = 0

        for _ in range(3):  # Send 3 probes for each hop
            # Create an IP packet with an increasing TTL value and a TCP packet
            packet = IP(dst=target_host, ttl=ttl) / TCP(dport=443, flags='S')
            
            # Send the packet and record the start time
            reply = sr1(packet, verbose=0, timeout=timeout)

            if reply is not None:
                host_ip = reply.getlayer(IP).src
                rtt = (reply.time - packet.sent_time) * 1000  # Convert to milliseconds
                total_rtt += rtt
                successful_probes += 1
                # If the target host is reached, break out of the loop
                if host_ip == target_host:
                    break

        if successful_probes > 0:
            avg_rtt = total_rtt / successful_probes
            loss_percentage = (1 - (successful_probes / 3)) * 100
            print(f"traceroute,dest={target_host},hop={ttl},ip={host_ip} avg={avg_rtt:.2f},loss={100 - (successful_probes / 3 * 100):.1f},status=\"OK\"")

            # If the target host is reached, break out of the loop
            if target_host == host_ip:
                break
        else:
            print(f"traceroute,dest={target_host},hop={ttl},ip=* avg=*,loss=100,status=\"Timeout\"")


def main():
    yaml_file = sys.argv[1]
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
    
    for entry in data:
        target_host = entry['domain']
        tcp_traceroute(target_host)

if __name__ == "__main__":
    main()
