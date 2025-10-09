#!/usr/bin/env python3
"""
Direct Venice AI Test Script
This script tests Venice AI exactly like your working curl command
"""

import requests
import http.client
import json

def test_with_requests():
    """Test using requests library (closest to curl)"""
    print("=" * 50)
    print("🧪 Testing Venice AI with REQUESTS (like curl)")
    print("=" * 50)
    
    api_key = "af9uD9UxvcrqR3kACGqyILz4gHQ7oN839m10wKy5pm"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "frequency_penalty": 0,
        "max_tokens": 4096,
        "messages": [
            {
                "content": "In 20 words or less, why is the sky blue?",
                "role": "user"
            }
        ],
        "model": "llama-3.2-3b",
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.95
    }
    
    try:
        print(f"📡 Making request to Venice AI...")
        response = requests.post(
            "https://api.venice.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"🎉 SUCCESS! AI Response: {message}")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

def test_with_http_client():
    """Test using http.client (like the bot)"""
    print("\n" + "=" * 50)
    print("🧪 Testing Venice AI with HTTP.CLIENT (like bot)")
    print("=" * 50)
    
    api_key = "af9uD9UxvcrqR3kACGqyILz4gHQ7oN839m10wKy5pm"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "frequency_penalty": 0,
        "max_tokens": 4096,
        "messages": [
            {
                "content": "In 20 words or less, why is the sky blue?",
                "role": "user"
            }
        ],
        "model": "llama-3.2-3b",
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.95
    }
    
    try:
        print(f"📡 Making request to Venice AI...")
        
        conn = http.client.HTTPSConnection("api.venice.ai")
        json_data = json.dumps(data)
        
        conn.request("POST", "/api/v1/chat/completions", json_data, headers)
        res = conn.getresponse()
        response_data = res.read()
        
        print(f"✅ Status Code: {res.status}")
        print(f"📝 Headers: {dict(res.getheaders())}")
        print(f"📄 Response: {response_data.decode('utf-8')}")
        
        if res.status == 200:
            result = json.loads(response_data.decode('utf-8'))
            message = result['choices'][0]['message']['content']
            print(f"🎉 SUCCESS! AI Response: {message}")
            return True
        else:
            print(f"❌ FAILED! Status: {res.status}")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Venice AI Connection Test")
    print("Comparing requests vs http.client methods")
    
    result1 = test_with_requests()
    result2 = test_with_http_client()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"   Requests: {'✅ SUCCESS' if result1 else '❌ FAILED'}")
    print(f"   HTTP Client: {'✅ SUCCESS' if result2 else '❌ FAILED'}")
    print("=" * 50)