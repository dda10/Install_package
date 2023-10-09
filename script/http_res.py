#!/usr/bin/python3
import sys
import requests
import time
import yaml
import json
import base64
from requests.exceptions import ConnectTimeout

http_response_map = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

def get_token_bearer(url_auth,headers_auth,data,default_token,r_timeout):
    try:
        response_auth = requests.post(url_auth, headers=headers_auth, json=data, timeout=(r_timeout))
    except ConnectTimeout:
        return default_token

    if response_auth.status_code == 200:
        base64_data = response_auth.content
        decoded_data = base64.b64decode(base64_data)

        try:
            json_string = json.loads(decoded_data.decode('utf-8'))
            data_string = json_string.get('data')
            data = json.loads(data_string)
            token = data["token"]
            return token
        except json.JSONDecodeError as e:
            return default_token
    else:
        return default_token


# Function to send a request and measure response time
def send_request(url, r_timeout):
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers_auth, timeout=r_timeout)
        end_time = time.time()
        status_code = response.status_code
        response_time = end_time - start_time
        result = http_response_map.get(status_code, "Unknown")
        return url,response_time, response, result

    except requests.exceptions.Timeout:
        return None, None


yaml_file = sys.argv[1]
with open(yaml_file, 'r') as file:
    config = yaml.safe_load(file)

for entry in config:
    domain = entry['domain']
    http_profiles = entry['http_profile']

    for profile in http_profiles:
        
        uri = profile['uri']
        url = f"https://{domain}{uri}"
        method = profile['method']
        requires_authentication = profile.get('requires_authentication', False)
        r_time_kpi = profile.get('r_time_kpi',5)
        r_timeout = profile.get('r_timeout', 10)

        
        default_token = profile.get('auth_profile', {}).get('default_token', None)
        url_auth = profile.get('auth_profile', {}).get('url_auth', None)
        headers_auth = profile.get('auth_profile', {}).get('headers_auth', {})
        data = profile.get('auth_profile', {}).get('data', {})

        if requires_authentication:
            token = get_token_bearer(url_auth,headers_auth,data,default_token,r_timeout)
            headers_auth['Authorization'] = f'Bearer {token}'

        url, response_time, response, result = send_request(url, r_timeout)
        result_type = '"' + result + '"'
        if response is not None:
            output = f'https_response,domain={domain},uri={uri},url=https://{domain}{uri} http_response_code={response.status_code},response_time={response_time:.9f},result_type="{result_type}"'
            print(output)
        else:
            print(f'https_response,domain={domain},uri={uri},url=https://{domain}{uri} http_response_code=0,response_time=0.000000000,result_type="Request Timeout"')


