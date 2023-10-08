import json
import base64
import requests
import yaml

url = "https://hopdongdientu.viettel.vn/scontract-web-api/api/auth/login"
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*" ,
    "Accept-Encoding":"gzip,deflate,br",
    "Connection":"keep-alive"

}

def get_token(user):
    with open('secret.yaml', 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    if user in data:
        username = data[user]['username']
        password = data[user]['password']
        
        payload = {
            "username": f"{username}",
            "password": f"{password}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            base64_data = response.content
            decoded_data = base64.b64decode(base64_data)
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
            
print(get_token('user2'))