#!/usr/bin/env python3
"""
Focused test for the previously failing endpoints
"""

import requests
import json

BASE_URL = "https://tribe-multiverse.preview.emergentagent.com/api"
TEST_USER_EMAIL = "test.user@tribeai.com"
TEST_USER_PASSWORD = "SecurePassword123!"

def get_auth_token():
    """Get authentication token"""
    session = requests.Session()
    
    # Login
    data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    if response.status_code == 200:
        # Extract token from cookies if available
        if "session_token" in response.cookies:
            return response.cookies["session_token"], session
    return None, session

def test_law_search():
    """Test legal information search"""
    token, session = get_auth_token()
    
    data = {
        "query": "tenant rights and landlord responsibilities",
        "category": "Landlord-Tenant"
    }
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = session.post(f"{BASE_URL}/law/search", json=data, headers=headers)
    print(f"Law Search: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    else:
        result = response.json()
        print(f"Success: Got information and {len(result.get('resources', []))} resources")

def test_law_assist():
    """Test AI-guided form filling"""
    token, session = get_auth_token()
    
    data = {
        "form_type": "rental_agreement",
        "conversation": [
            {"role": "user", "content": "I need help filling out a rental agreement"}
        ],
        "current_data": {}
    }
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = session.post(f"{BASE_URL}/law/assist", json=data, headers=headers)
    print(f"Law Assist: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    else:
        result = response.json()
        print(f"Success: {result.get('message', '')[:100]}...")

def test_studio_video():
    """Test AI video generation with form data"""
    token, session = get_auth_token()
    
    data = {
        "prompt": "A cat playing with a ball of yarn in a sunny room",
        "style": "realistic",
        "service": "modelscope"
    }
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = session.post(f"{BASE_URL}/studio/generate-video", data=data, headers=headers)
    print(f"Studio Video: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    else:
        result = response.json()
        print(f"Success: {result.get('message', '')}")

if __name__ == "__main__":
    print("Testing previously failing endpoints...")
    test_law_search()
    test_law_assist()
    test_studio_video()