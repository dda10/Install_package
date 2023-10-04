#!/usr/bin/python3

import subprocess
import re

def ping_domain(domain):
    try:
        # Run the ping command and capture the output
        completed_process = subprocess.run(['ping', '-c', '4', domain], text=True, capture_output=True, check=True)

        # Extract the exit code and output
        exit_code = completed_process.returncode
        output = completed_process.stdout

        if exit_code == 0:
            # If the exit code is 0, indicating success
            avg_time = float(re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', output).group(2))
            max_time = float(re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', output).group(3))
            min_time = float(re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', output).group(1))
            packet_loss_percentage = int(re.search(r'(\d+)% packet loss', output).group(1))
            ttl = int(re.search(r'ttl=(\d+)', output).group(1))

            # Generate the output string
            output_string = f'ping,domain={domain} average_response_ms={avg_time:.3f},maximum_response_ms={max_time:.3f},minimum_response_ms={min_time:.3f},percent_packet_loss={packet_loss_percentage},ttl={ttl}'
        else:
            # If the exit code is non-zero, indicating failure
            output_string = f'ping,domain={domain} average_response_ms=0.000,maximum_response_ms=0.000,minimum_response_ms=0.000,percent_packet_loss=100,ttl=0'

        return output_string
    except subprocess.CalledProcessError:
        print(f"Failed to ping {domain}")
        return None

with open('/opt/domain', 'r') as file:
    domains = file.read().splitlines()

if __name__ == "__main__":
    for domain in domains:
        result = ping_domain(domain)
        if result:
            print(result)
