"""Tests for API endpoints."""

import json
import pytest
from unittest.mock import patch, Mock


class TestHealthEndpoint:
    """Tests for health/root endpoint."""

    def test_root_returns_200(self, client):
        """Test root endpoint returns 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"


class TestFrameworksEndpoint:
    """Tests for /frameworks endpoint."""

    def test_get_frameworks_returns_list(self, client):
        """Test getting all frameworks returns a list."""
        response = client.get("/frameworks")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_frameworks_have_required_fields(self, client):
        """Test frameworks contain required fields."""
        response = client.get("/frameworks")
        data = json.loads(response.data)

        required_fields = ["id", "name", "description", "ideal_for"]
        for framework in data:
            for field in required_fields:
                assert field in framework, f"Missing field: {field}"


class TestFrameworkDetailEndpoint:
    """Tests for /frameworks/<id> endpoint."""

    def test_get_valid_framework(self, client, sample_framework):
        """Test getting a valid framework returns details."""
        response = client.get(f"/frameworks/{sample_framework}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_framework

    def test_get_invalid_framework_returns_404(self, client):
        """Test getting invalid framework returns 404."""
        response = client.get("/frameworks/nonexistent_framework")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data


class TestOptimizeEndpoint:
    """Tests for /optimize endpoint."""

    def test_optimize_requires_prompt(self, client):
        """Test optimize endpoint requires prompt."""
        response = client.post(
            "/optimize",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_optimize_with_valid_prompt(self, client, sample_prompt):
        """Test optimize with valid prompt."""
        response = client.post(
            "/optimize",
            data=json.dumps({"prompt": sample_prompt}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "optimized_prompt" in data
        assert "framework" in data

    def test_optimize_with_explicit_framework(self, client, sample_prompt, sample_framework):
        """Test optimize with explicit framework selection."""
        response = client.post(
            "/optimize",
            data=json.dumps({
                "prompt": sample_prompt,
                "framework": sample_framework,
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["framework"]["id"] == sample_framework

    def test_optimize_rejects_empty_prompt(self, client):
        """Test optimize rejects empty prompt."""
        response = client.post(
            "/optimize",
            data=json.dumps({"prompt": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_optimize_rejects_too_short_prompt(self, client):
        """Test optimize rejects too short prompt."""
        response = client.post(
            "/optimize",
            data=json.dumps({"prompt": "ab"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_optimize_requires_json_content_type(self, client, sample_prompt):
        """Test optimize requires JSON content type."""
        response = client.post(
            "/optimize",
            data=f'{{"prompt": "{sample_prompt}"}}',
            content_type="text/plain",
        )
        assert response.status_code == 415


class TestChatEndpoint:
    """Tests for /chat endpoint."""

    def test_chat_requires_prompt(self, client):
        """Test chat endpoint requires prompt."""
        response = client.post(
            "/chat",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("app.llm_service")
    def test_chat_with_valid_prompt(self, mock_llm, client, sample_prompt):
        """Test chat with valid prompt and mocked LLM."""
        from services.llm_service import LLMResponse
        mock_response = LLMResponse(
            content="Optimized test prompt",
            model="test-model",
        )
        mock_llm.optimize_prompt.return_value = mock_response

        response = client.post(
            "/chat",
            data=json.dumps({"prompt": sample_prompt}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "optimized_prompt" in data

    @patch("app.llm_service")
    def test_chat_with_metadata(self, mock_llm, client, sample_prompt):
        """Test chat returns metadata when requested."""
        from services.llm_service import LLMResponse
        mock_response = LLMResponse(
            content="Optimized test prompt",
            model="test-model",
            usage={"prompt_tokens": 10, "completion_tokens": 20},
        )
        mock_llm.optimize_prompt.return_value = mock_response

        response = client.post(
            "/chat",
            data=json.dumps({
                "prompt": sample_prompt,
                "include_meta": True,
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "metadata" in data

    @patch("app.llm_service")
    def test_chat_handles_llm_timeout(self, mock_llm, client, sample_prompt):
        """Test chat handles LLM timeout gracefully."""
        from services.llm_service import LLMError

        mock_llm.optimize_prompt.side_effect = LLMError(
            "Timeout", status_code=504
        )

        response = client.post(
            "/chat",
            data=json.dumps({"prompt": sample_prompt}),
            content_type="application/json",
        )
        assert response.status_code == 504


class TestInputValidation:
    """Tests for input validation."""

    def test_rejects_script_injection(self, client):
        """Test prompt with script tags is rejected."""
        response = client.post(
            "/optimize",
            data=json.dumps({"prompt": "<script>alert('xss')</script>"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_rejects_template_injection(self, client):
        """Test prompt with template injection is rejected."""
        response = client.post(
            "/optimize",
            data=json.dumps({"prompt": "test {{malicious}} content"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_accepts_valid_special_characters(self, client):
        """Test valid prompts with special characters work."""
        response = client.post(
            "/optimize",
            data=json.dumps({
                "prompt": "Write a function that calculates x^2 + y^2"
            }),
            content_type="application/json",
        )
        assert response.status_code == 200


class TestCORSHeaders:
    """Tests for CORS headers."""

    def test_cors_headers_present(self, client):
        """Test CORS headers are present in response."""
        response = client.options("/optimize")
        # Should have CORS headers for allowed origins
        assert response.status_code in (200, 204)


class TestRequestTracking:
    """Tests for request ID tracking."""

    def test_response_includes_request_id(self, client):
        """Test response includes X-Request-ID header."""
        response = client.get("/health")
        assert "X-Request-ID" in response.headers

    def test_custom_request_id_is_used(self, client):
        """Test custom X-Request-ID is preserved."""
        custom_id = "test-123"
        response = client.get(
            "/health",
            headers={"X-Request-ID": custom_id}
        )
        assert response.headers.get("X-Request-ID") == custom_id

    def test_response_includes_timing(self, client):
        """Test response includes timing header."""
        response = client.get("/health")
        assert "X-Response-Time" in response.headers
