import requests
import time
import yaml
from get_bearer import get_token

# Function to send a request and measure response time
def send_request(domain, uri, method, requires_auth, timeout_seconds):
    url = f"https://{domain}{uri}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*" ,
        "Accept-Encoding":"gzip,deflate,br",
        "Connection":"keep-alive"
    }
    if requires_auth:
        headers['Authorization'] = f'Bearer {get_token()}'
        pass
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, timeout=timeout_seconds)
        end_time = time.time()
        response_time = end_time - start_time
        return response_time, response
    except requests.exceptions.Timeout:
        return None, None
    
# Load the YAML file
with open('domain.yml', 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Iterate through domains and URIs
for domain_data in data['domains']:
    domain_name = domain_data['domain']
    uris = domain_data['uris']

    for uri_data in uris:
        uri_path = uri_data['uri']
        http_method = uri_data['method']
        requires_auth = uri_data['requires_authentication']
        timeout_seconds = uri_data.get('timeout_seconds', 5)  # Set a default timeout of 5 seconds if not specified
        response_time, response = send_request(domain_name, uri_path, http_method, requires_auth, timeout_seconds)

        if response is not None:
            output = f'url_response,domain={domain_name},uri={uri_path},url=https://{domain_name}{uri_path} http_response_code={response.status_code},response_time={response_time:.9f},result_type="OK"'
            print(output)
        else:
            print(f'url_response,domain={domain_name},uri={uri_path},url=https://{domain_name}{uri_path} http_response_code=0,response_time=0.000000000,result_type="Request Timeout"')
