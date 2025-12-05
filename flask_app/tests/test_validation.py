"""Tests for input validation."""

import pytest
from middleware.validation import (
    validate_prompt_input,
    validate_framework_id,
    ValidationError,
)


class TestValidatePromptInput:
    """Tests for prompt input validation."""

    def test_valid_prompt(self):
        """Test valid prompt passes validation."""
        prompt, framework = validate_prompt_input(
            {"prompt": "This is a valid prompt"}
        )
        assert prompt == "This is a valid prompt"
        assert framework is None

    def test_valid_prompt_with_framework(self):
        """Test valid prompt with framework passes."""
        prompt, framework = validate_prompt_input(
            {"prompt": "Test prompt", "framework": "coding_technical"}
        )
        assert prompt == "Test prompt"
        assert framework == "coding_technical"

    def test_missing_prompt_raises_error(self):
        """Test missing prompt raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({})
        assert "required" in exc.value.message.lower()

    def test_empty_prompt_raises_error(self):
        """Test empty prompt raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": ""})
        assert exc.value.field == "prompt"

    def test_too_short_prompt_raises_error(self):
        """Test too short prompt raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": "ab"}, min_length=3)
        assert "at least" in exc.value.message.lower()

    def test_too_long_prompt_raises_error(self):
        """Test too long prompt raises ValidationError."""
        long_prompt = "a" * 101
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": long_prompt}, max_length=100)
        assert "exceed" in exc.value.message.lower()

    def test_non_string_prompt_raises_error(self):
        """Test non-string prompt raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": 123})
        assert "string" in exc.value.message.lower()

    def test_script_tag_rejected(self):
        """Test script tags are rejected."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": "<script>alert('test')</script>"})
        assert "invalid" in exc.value.message.lower()

    def test_javascript_url_rejected(self):
        """Test javascript: URLs are rejected."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": "javascript:void(0)"})
        assert "invalid" in exc.value.message.lower()

    def test_template_injection_rejected(self):
        """Test template injection is rejected."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input({"prompt": "test {{injection}}"})
        assert "invalid" in exc.value.message.lower()

    def test_null_data_raises_error(self):
        """Test null data raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input(None)
        assert "JSON" in exc.value.message

    def test_prompt_whitespace_trimmed(self):
        """Test prompt whitespace is trimmed."""
        prompt, _ = validate_prompt_input({"prompt": "  test prompt  "})
        assert prompt == "test prompt"

    def test_framework_normalized(self):
        """Test framework is normalized to lowercase."""
        _, framework = validate_prompt_input(
            {"prompt": "test", "framework": "CODING_TECHNICAL"}
        )
        assert framework == "coding_technical"

    def test_invalid_framework_format_rejected(self):
        """Test invalid framework format is rejected."""
        with pytest.raises(ValidationError) as exc:
            validate_prompt_input(
                {"prompt": "test", "framework": "invalid-format!"}
            )
        assert "framework" in exc.value.field.lower()


class TestValidateFrameworkId:
    """Tests for framework ID validation."""

    def test_valid_framework_id(self):
        """Test valid framework ID passes."""
        result = validate_framework_id("coding_technical")
        assert result == "coding_technical"

    def test_framework_id_normalized(self):
        """Test framework ID is normalized."""
        result = validate_framework_id("  CODING_TECHNICAL  ")
        assert result == "coding_technical"

    def test_empty_framework_id_rejected(self):
        """Test empty framework ID is rejected."""
        with pytest.raises(ValidationError):
            validate_framework_id("")

    def test_invalid_characters_rejected(self):
        """Test invalid characters are rejected."""
        with pytest.raises(ValidationError):
            validate_framework_id("coding-technical")

    def test_too_long_framework_id_rejected(self):
        """Test too long framework ID is rejected."""
        with pytest.raises(ValidationError):
            validate_framework_id("a" * 51)


class TestValidationErrorClass:
    """Tests for ValidationError class."""

    def test_error_message(self):
        """Test error message is set correctly."""
        error = ValidationError("Test error")
        assert error.message == "Test error"

    def test_error_field(self):
        """Test error field is set correctly."""
        error = ValidationError("Test error", field="test_field")
        assert error.field == "test_field"

    def test_error_status_code(self):
        """Test error status code is set correctly."""
        error = ValidationError("Test error", status_code=422)
        assert error.status_code == 422

    def test_to_dict(self):
        """Test to_dict serialization."""
        error = ValidationError("Test error", field="test_field")
        result = error.to_dict()
        assert result["error"] == "Test error"
        assert result["field"] == "test_field"

    def test_to_dict_without_field(self):
        """Test to_dict without field."""
        error = ValidationError("Test error")
        result = error.to_dict()
        assert "field" not in result
