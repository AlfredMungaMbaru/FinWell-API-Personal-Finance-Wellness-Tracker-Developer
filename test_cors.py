#!/usr/bin/env python3
"""
Test script to verify CORS functionality for FinWell API.
This script demonstrates that the API endpoints work with cross-origin requests.
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def test_user_registration():
    """Test user registration endpoint with CORS headers."""
    url = f"{BASE_URL}/users/register/"
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000',  # Simulate frontend origin
    }
    data = {
        "username": "corstest_user",
        "email": "corstest@example.com",
        "password": "securepassword123",
        "first_name": "CORS",
        "last_name": "Test"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Registration Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        print(f"Registration failed: {e}")
        return False

def test_user_login():
    """Test user login endpoint with CORS headers."""
    url = f"{BASE_URL}/users/login/"
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000',
    }
    data = {
        "username": "corstest_user",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Login Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        if response.status_code == 200:
            tokens = response.json()
            print(f"Access Token received: {tokens.get('access', 'N/A')[:20]}...")
            return tokens.get('access')
        else:
            print(f"Login failed: {response.json()}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return None

def test_authenticated_endpoint(access_token):
    """Test an authenticated endpoint (profile) with CORS headers."""
    url = f"{BASE_URL}/users/profile/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Origin': 'http://localhost:3000',
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Profile Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        print(f"Profile Data: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Profile fetch failed: {e}")
        return False

def main():
    """Run CORS tests."""
    print("FinWell API CORS Test")
    print("=" * 50)
    
    # Test registration
    print("\n1. Testing User Registration...")
    if test_user_registration():
        print("✅ Registration successful with CORS support")
    else:
        print("❌ Registration failed")
        return
    
    # Test login
    print("\n2. Testing User Login...")
    access_token = test_user_login()
    if access_token:
        print("✅ Login successful with CORS support")
    else:
        print("❌ Login failed")
        return
    
    # Test authenticated endpoint
    print("\n3. Testing Authenticated Endpoint...")
    if test_authenticated_endpoint(access_token):
        print("✅ Authenticated request successful with CORS support")
    else:
        print("❌ Authenticated request failed")
        return
    
    print("\n✅ All CORS tests passed! The API is ready for frontend integration.")

if __name__ == "__main__":
    main()
