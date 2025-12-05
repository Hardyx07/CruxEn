"""Pytest configuration and fixtures."""

import os
import pytest
from unittest.mock import Mock, patch

# Set testing environment before importing app
os.environ["FLASK_ENV"] = "testing"
os.environ["GROQ_API_KEY"] = "test-api-key"

from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_llm_service():
    """Mock LLM service for tests."""
    with patch("app.llm_service") as mock:
        mock_response = Mock()
        mock_response.content = "Optimized test prompt"
        mock_response.model = "test-model"
        mock_response.usage = {"prompt_tokens": 10, "completion_tokens": 20}
        mock.optimize_prompt.return_value = mock_response
        yield mock


@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return "Write a Python function to sort an array"


@pytest.fixture
def sample_framework():
    """Sample framework ID for testing."""
    return "coding_technical"
