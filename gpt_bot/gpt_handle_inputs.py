import requests

# URL of the Flask app
url = 'http://127.0.0.1:5000/'

# User input
prompt = input('Enter prompt: ')

# JSON payload to send to the server
payload = {'prompt': prompt}

# Send POST request to the Flask app
response = requests.post(url, json=payload)

