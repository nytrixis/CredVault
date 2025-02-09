import requests

response = requests.post(
    "http://localhost:8000/verify-resume",
    json=test_resume
)

print(response.json())
