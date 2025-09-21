#!/usr/bin/env python3
"""
Simple test script for the Odisha Health Chatbot
"""
from fastapi.testclient import TestClient
from main import app
import sys
import os
sys.path.append(os.path.dirname(__file__))


def test_chatbot():
    """Test the chatbot with various queries"""
    client = TestClient(app)

    # Test cases
    test_cases = [
        {
            "message": "Hello, I have a fever",
            "sender_id": "test_user1",
            "language": "en",
            "description": "Fever symptom query in English"
        },
        {
            "message": "Tell me about vaccination",
            "sender_id": "test_user2",
            "language": "en",
            "description": "Vaccination information query"
        },
        {
            "message": "ନମସ୍କାର",
            "sender_id": "test_user3",
            "language": "or",
            "description": "Greeting in Odia"
        },
        {
            "message": "गर्भावस्था के दौरान क्या सावधानी बरतनी चाहिए?",
            "sender_id": "test_user4",
            "language": "hi",
            "description": "Pregnancy care query in Hindi"
        }
    ]

    print("=== Odisha Health Chatbot Test Results ===\n")

    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['description']}")
        print(f"   Input: {test_case['message']}")

        response = client.post("/chat", json={
            "message": test_case["message"],
            "sender_id": test_case["sender_id"],
            "language": test_case["language"]
        })

        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   ✓ Intent: {result['intent']}")
            print(f"   ✓ Language: {result['language']}")
            print(f"   ✓ Response: {result['response']}")
        else:
            print(f"   ✗ Error: {response.status_code}")
            print(f"   ✗ Details: {response.text}")

        print("-" * 60)


if __name__ == "__main__":
    test_chatbot()
