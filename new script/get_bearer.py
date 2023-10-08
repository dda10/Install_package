import json
import base64
import requests

url = "https://hopdongdientu.viettel.vn/scontract-web-api/api/auth/login"

data = {
    "username": "",
    "password": ""
}

headers = {
    "Content-Type": "application/json",
    "Accept": "*/*" ,
    "Accept-Encoding":"gzip,deflate,br",
    "Connection":"keep-alive"

}

# Send the POST request with custom headers
response = requests.post(url, headers=headers, json=data)
def get_token():
    if response.status_code == 200:
        # Decode the base64 response content
        base64_data = response.content
        decoded_data = base64.b64decode(base64_data)

        # Assuming the decoded data is a JSON string, parse it
        try:
            json_string = json.loads(decoded_data.decode('utf-8'))
            data_string = json_string.get('data')
            data = json.loads(data_string)
            token = data["token"]
            return token
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
    else:
        print("POST request failed with status code:", response.status_code)