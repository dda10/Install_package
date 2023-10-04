#! /usr/bin/python3
import requests
import datetime
import time

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
def check_website(url):
    url = f"https://{domain}{uri}"
    try:
        start_time = datetime.datetime.now()
        response = requests.get (url)
        end_time = datetime.datetime.now()

        status_code = response.status_code
        response_time = (end_time - start_time).total_seconds()
        content_length = len(response.content)

        result = http_response_map.get(status_code, "Unknown")
        timestamp = int(time.time())

        return result, url, status_code, response_time, content_length, timestamp
    except Exception as e:
        return "Error", 0, 0, 0, datetime.datetime.now()

# Read the list of websites from a file
with open('/opt/https_domain', 'r') as file:
    lines = file.read().splitlines()

# Iterate through the list of websites and check their responses
for line in lines:
    domain, uri = line.strip().split()
    result, url, status_code, response_time, content_length, timestamp = check_website(line)
    content_length = int(content_length)
    http_response_code = int(status_code)
    result_type ='"' + result + '"'
    response_time = float(response_time)
    print(
    "url_response,"
    f"domain={domain},"
    f"uri={uri},"
    f"url={url} "
    f"content_length={content_length},"
    f"http_response_code={http_response_code},"
    f"response_time={response_time},"
    f"result_type={result_type}"
    )
