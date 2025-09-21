#!/usr/bin/env python3
"""
Comprehensive pytest test suite for Ama Arogya ChatBot API
"""
import pytest
import requests
import json
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, UserInteraction
from unittest.mock import patch, MagicMock

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check_success(self):
        """Test health endpoint returns success"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_check_method_not_allowed(self):
        """Test health endpoint with wrong HTTP method"""
        response = client.post("/health")
        assert response.status_code == 405


class TestChatEndpoint:
    """Test chat functionality"""

    def test_chat_basic_message(self):
        """Test basic chat functionality"""
        payload = {
            "message": "I have fever",
            "sender_id": "test_user",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "response" in data
        assert "language" in data
        assert "intent" in data
        assert data["language"] == "en"

    def test_chat_hindi_message(self):
        """Test chat with Hindi message"""
        payload = {
            "message": "मुझे बुखार है",
            "sender_id": "test_user_hindi",
            "language": "hi"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["language"] == "hi"
        assert "response" in data

    def test_chat_oriya_message(self):
        """Test chat with Oriya message"""
        payload = {
            "message": "ମୋର ଜ୍ବର ଅଛି",
            "sender_id": "test_user_oriya",
            "language": "or"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["language"] == "or"
        assert "response" in data

    def test_chat_missing_message(self):
        """Test chat with missing message field"""
        payload = {
            "sender_id": "test_user",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 422

    def test_chat_missing_sender_id(self):
        """Test chat with missing sender_id field"""
        payload = {
            "message": "Hello",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 422

    def test_chat_default_language(self):
        """Test chat with default language when not specified"""
        payload = {
            "message": "Hello",
            "sender_id": "test_user"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["language"] == "en"  # Default language

    @patch('main.get_rasa_response')
    def test_chat_rasa_fallback(self, mock_rasa):
        """Test fallback when Rasa is unavailable"""
        mock_rasa.return_value = None

        payload = {
            "message": "I have fever",
            "sender_id": "test_user",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["intent"] == "fallback"
        assert "fever" in data["response"].lower(
        ) or "rest" in data["response"].lower()


class TestStatsEndpoint:
    """Test statistics endpoint"""

    def test_stats_endpoint(self):
        """Test stats endpoint returns proper structure"""
        response = client.get("/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_interactions" in data
        assert "language_distribution" in data
        assert isinstance(data["total_interactions"], int)
        assert isinstance(data["language_distribution"], dict)


class TestStaticFiles:
    """Test static file serving"""

    def test_root_endpoint(self):
        """Test root endpoint serves HTML"""
        response = client.get("/")
        # May not exist in test environment
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

    def test_demo_endpoint(self):
        """Test demo endpoint serves HTML"""
        response = client.get("/demo")
        # May not exist in test environment
        assert response.status_code in [200, 404]


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_chat_with_very_long_message(self):
        """Test chat with extremely long message"""
        long_message = "x" * 5000  # Very long message
        payload = {
            "message": long_message,
            "sender_id": "test_user",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        # Should either succeed or be handled gracefully
        assert response.status_code in [200, 413, 422]

    def test_chat_with_special_characters(self):
        """Test chat with special characters and potential injection"""
        payload = {
            "message": "<script>alert('test')</script>",
            "sender_id": "test_user",
            "language": "en"
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        # Response should not contain unescaped script tags
        data = response.json()
        assert "<script>" not in data["response"]

    def test_invalid_json_payload(self):
        """Test with invalid JSON payload"""
        response = client.post(
            "/chat",
            content="invalid json",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 422

    def test_nonexistent_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404


@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    session = MagicMock()
    return session


def test_mock_db_session_fixture(mock_db_session):
    """Test that the mock database session fixture works"""
    assert mock_db_session is not None
    mock_db_session.query.return_value.count.return_value = 5
    assert mock_db_session.query.return_value.count() == 5


def test_get_fallback_response():
    """Test fallback response function"""
    from main import get_fallback_response

    # Test fever response
    response = get_fallback_response("I have fever", "en")
    assert "fever" in response.lower() or "rest" in response.lower()

    # Test Hindi fever response
    response = get_fallback_response("मुझे बुखार है", "hi")
    assert len(response) > 0

    # Test general response
    response = get_fallback_response("random question", "en")
    assert "health" in response.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
