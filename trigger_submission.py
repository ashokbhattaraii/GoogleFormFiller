import requests
import json

with open('generated_60_responses.json', 'r') as f:
    data = json.load(f)

print(f"Sending {len(data)} records to the backend...")

response = requests.post(
    'http://localhost:8000/api/v1/submit',
    json={"data": data}
)

if response.status_code == 200:
    print("Success! The background job has started.")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
