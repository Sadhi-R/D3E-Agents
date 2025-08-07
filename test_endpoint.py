import requests
import json

def test_endpoint():
    url = "http://localhost:8001/api/ai/generate"
    data = {
        "prompt": "Create a login page widget with email and password inputs",
        "project": "Syllabus Management"
    }
    
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Result preview: {result['result'][:500]}...")
    
if __name__ == "__main__":
    test_endpoint()
