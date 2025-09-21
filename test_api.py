#!/usr/bin/env python3
"""
Test script for Ama Arogya ChatBot API
"""
import requests
import json


def test_api():
    base_url = "http://127.0.0.1:8001"

    print("Testing Ama Arogya ChatBot API...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        return False

    # Test chat endpoint
    try:
        chat_data = {
            "message": "I have fever",
            "sender_id": "test_user",
            "language": "en"
        }

        response = requests.post(
            f"{base_url}/chat",
            json=chat_data,
            timeout=10
        )
        print(f"\nChat test: {response.status_code}")
        if response.status_code == 200:
            chat_response = response.json()
            print(f"Bot response: {chat_response['response']}")
            print(f"Intent: {chat_response['intent']}")
            print(f"Response time: {chat_response['response_time_ms']:.2f}ms")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Chat test failed: {e}")
        return False

    # Test stats endpoint
    try:
        response = requests.get(f"{base_url}/stats", timeout=5)
        print(f"\nStats test: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"Total interactions: {stats['total_interactions']}")
            print(f"Average response time: {stats['response_time_avg']:.2f}ms")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Stats test failed: {e}")

    return True


if __name__ == "__main__":
    print("Make sure the server is running first with: python main.py")
    print("Then run this test script.")
    print("\nTest results:")
    test_api()
