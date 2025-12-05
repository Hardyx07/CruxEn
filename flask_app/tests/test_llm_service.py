"""Tests for LLM service."""

import pytest
from unittest.mock import patch, Mock

from services.llm_service import LLMService, LLMResponse, LLMError


class TestLLMService:
    """Tests for LLMService class."""

    def test_init_requires_api_key(self):
        """Test initialization requires API key."""
        with pytest.raises(ValueError) as exc:
            LLMService(api_key="")
        assert "API key" in str(exc.value)

    def test_init_with_api_key(self):
        """Test initialization with valid API key."""
        service = LLMService(api_key="test-key")
        assert service.api_key == "test-key"

    def test_custom_configuration(self):
        """Test custom configuration is applied."""
        service = LLMService(
            api_key="test-key",
            api_url="https://custom.api.com",
            model="custom-model",
            timeout=60,
        )
        assert service.api_url == "https://custom.api.com"
        assert service.model == "custom-model"
        assert service.timeout == 60

    @patch("requests.post")
    def test_optimize_prompt_success(self, mock_post):
        """Test successful prompt optimization."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {"content": "Optimized prompt content"},
                    "finish_reason": "stop",
                }
            ],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }
        mock_post.return_value = mock_response

        service = LLMService(api_key="test-key")
        result = service.optimize_prompt(
            user_prompt="Test prompt",
            framework_name="Test Framework",
            framework_desc="Test description",
            role_template="Test role",
            confidence=0.9,
        )

        assert isinstance(result, LLMResponse)
        assert result.content == "Optimized prompt content"
        assert result.model == "test-model"

    @patch("requests.post")
    def test_optimize_prompt_api_error(self, mock_post):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        service = LLMService(api_key="test-key")

        with pytest.raises(LLMError) as exc:
            service.optimize_prompt(
                user_prompt="Test",
                framework_name="Test",
                framework_desc="Test",
                role_template="Test",
                confidence=0.9,
            )

        assert exc.value.status_code == 500

    @patch("requests.post")
    def test_optimize_prompt_timeout(self, mock_post):
        """Test timeout handling."""
        import requests as req

        mock_post.side_effect = req.exceptions.Timeout()

        service = LLMService(api_key="test-key")

        with pytest.raises(LLMError) as exc:
            service.optimize_prompt(
                user_prompt="Test",
                framework_name="Test",
                framework_desc="Test",
                role_template="Test",
                confidence=0.9,
            )

        assert exc.value.status_code == 504

    @patch("requests.post")
    def test_optimize_prompt_connection_error(self, mock_post):
        """Test connection error handling."""
        import requests as req

        mock_post.side_effect = req.exceptions.ConnectionError()

        service = LLMService(api_key="test-key")

        with pytest.raises(LLMError) as exc:
            service.optimize_prompt(
                user_prompt="Test",
                framework_name="Test",
                framework_desc="Test",
                role_template="Test",
                confidence=0.9,
            )

        assert exc.value.status_code == 502


class TestLLMResponse:
    """Tests for LLMResponse dataclass."""

    def test_response_creation(self):
        """Test LLMResponse creation."""
        response = LLMResponse(
            content="Test content",
            model="test-model",
            usage={"prompt_tokens": 10},
            finish_reason="stop",
        )

        assert response.content == "Test content"
        assert response.model == "test-model"
        assert response.usage == {"prompt_tokens": 10}
        assert response.finish_reason == "stop"

    def test_response_optional_fields(self):
        """Test LLMResponse with optional fields."""
        response = LLMResponse(content="Test", model="model")

        assert response.content == "Test"
        assert response.usage is None
        assert response.finish_reason is None


class TestLLMError:
    """Tests for LLMError class."""

    def test_error_creation(self):
        """Test LLMError creation."""
        error = LLMError(
            message="Test error",
            status_code=500,
            details="Detailed info",
        )

        assert error.message == "Test error"
        assert error.status_code == 500
        assert error.details == "Detailed info"

    def test_error_default_status_code(self):
        """Test LLMError default status code."""
        error = LLMError(message="Test error")
        assert error.status_code == 500

    def test_error_is_exception(self):
        """Test LLMError is an Exception."""
        error = LLMError(message="Test")
        assert isinstance(error, Exception)

        with pytest.raises(LLMError):
            raise error
