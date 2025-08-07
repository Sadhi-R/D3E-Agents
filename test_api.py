import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def test_claude_api():
    """Test Claude API directly"""
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-sonnet-20240229",  # Use a known working model
        "max_tokens": 2048,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user", 
                "content": "Create a simple D3E widget for a login form with email and password fields. Use proper D3E JSON format."
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return ''.join([part.get("text", "") for part in data.get("content", [])])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_openai_api():
    """Test OpenAI API directly"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Create a simple D3E widget for a login form with email and password fields. Use proper D3E JSON format."
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    print("Testing Claude API...")
    claude_result = test_claude_api()
    
    print("\n" + "="*50 + "\n")
    
    print("Testing OpenAI API...")
    openai_result = test_openai_api()
    
    print("\n" + "="*50 + "\n")
    
    if claude_result:
        print("Claude Result:")
        print(claude_result)
    
    if openai_result:
        print("OpenAI Result:")
        print(openai_result)
