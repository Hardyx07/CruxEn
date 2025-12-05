"""
Input Validation Middleware
===========================

This module provides input validation utilities for the Flask API.
It ensures all user input is properly validated before processing,
protecting against:

- Missing or invalid fields
- Malicious content (XSS, injection attacks)
- Oversized inputs (DoS prevention)
- Invalid data types

Classes:
--------
- ValidationError: Custom exception for validation failures

Functions:
----------
- validate_prompt_input(): Validate POST body for prompt endpoints
- validate_content_type(): Ensure correct Content-Type header
- validate_framework_id(): Validate framework ID URL parameters

Security Patterns Blocked:
--------------------------
- <script> tags (XSS)
- javascript: URLs
- data:text/html URLs
- Template injection ({{ }})
- Expression injection (${ })

Usage:
------
    from middleware.validation import validate_prompt_input, ValidationError
    
    try:
        prompt, framework = validate_prompt_input(request.get_json())
    except ValidationError as e:
        return jsonify(e.to_dict()), e.status_code
"""

import re
from typing import Any, Dict, Optional, Tuple

from flask import request


# =============================================================================
# CUSTOM EXCEPTION
# =============================================================================

class ValidationError(Exception):
    """
    Custom exception for input validation errors.
    
    This exception carries structured information about validation failures
    that can be easily converted to API error responses.
    
    Attributes:
        message (str): Human-readable error message
        field (str, optional): Name of the field that failed validation
        status_code (int): HTTP status code (default: 400 Bad Request)
    
    Example:
        raise ValidationError(
            message="Prompt must be at least 3 characters",
            field="prompt",
            status_code=400
        )
    """

    def __init__(self, message: str, field: Optional[str] = None, status_code: int = 400):
        self.message = message
        self.field = field
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to JSON-serializable dictionary for API responses.
        
        Returns:
            dict: Error details suitable for JSON response
        
        Example output:
            {"error": "Prompt is required", "field": "prompt"}
        """
        result = {"error": self.message}
        if self.field:
            result["field"] = self.field
        return result


# =============================================================================
# MAIN VALIDATION FUNCTIONS
# =============================================================================

def validate_prompt_input(
    data: Optional[Dict[str, Any]],
    max_length: int = 10000,
    min_length: int = 3,
    require_prompt: bool = True,
) -> Tuple[str, Optional[str]]:
    """
    Validate prompt input data from request body.
    
    This function performs comprehensive validation on the JSON request body
    for prompt-related endpoints (/optimize, /chat).
    
    Validation Steps:
    1. Check that data is valid JSON object
    2. Validate prompt is present (if required)
    3. Validate prompt is a string
    4. Check prompt length (min/max)
    5. Scan for malicious patterns
    6. Validate framework format (if provided)
    
    Args:
        data: Parsed JSON request body (or None if parsing failed)
        max_length: Maximum allowed prompt length (default: 10000)
        min_length: Minimum required prompt length (default: 3)
        require_prompt: Whether the prompt field is required (default: True)
    
    Returns:
        Tuple[str, Optional[str]]: (validated_prompt, validated_framework)
            - prompt is stripped of leading/trailing whitespace
            - framework is normalized to lowercase (or None if not provided)
    
    Raises:
        ValidationError: On any validation failure with appropriate message
    
    Example:
        data = request.get_json(silent=True)
        prompt, framework = validate_prompt_input(data, max_length=5000)
    """
    # -------------------------------------------------------------------------
    # Step 1: Validate request body structure
    # -------------------------------------------------------------------------
    if data is None:
        raise ValidationError("Request body must be JSON", status_code=400)

    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object", status_code=400)

    # Extract fields
    prompt = data.get("prompt")
    framework = data.get("framework")

    # -------------------------------------------------------------------------
    # Step 2: Validate prompt field
    # -------------------------------------------------------------------------
    
    # Check if prompt is required and present
    if require_prompt and not prompt:
        raise ValidationError("Prompt is required", field="prompt")

    if prompt is not None:
        # Type check - must be a string
        if not isinstance(prompt, str):
            raise ValidationError("Prompt must be a string", field="prompt")

        # Strip whitespace and validate length
        prompt = prompt.strip()

        # Check minimum length (prevents trivial/empty prompts)
        if len(prompt) < min_length:
            raise ValidationError(
                f"Prompt must be at least {min_length} characters",
                field="prompt",
            )

        # Check maximum length (prevents oversized requests)
        if len(prompt) > max_length:
            raise ValidationError(
                f"Prompt must not exceed {max_length} characters",
                field="prompt",
            )

        # Security check - scan for malicious patterns
        if _contains_suspicious_patterns(prompt):
            raise ValidationError(
                "Prompt contains invalid content",
                field="prompt",
            )

    # -------------------------------------------------------------------------
    # Step 3: Validate framework field (if provided)
    # -------------------------------------------------------------------------
    if framework is not None:
        # Type check
        if not isinstance(framework, str):
            raise ValidationError("Framework must be a string", field="framework")

        # Normalize to lowercase
        framework = framework.strip().lower()

        # Format validation - only allow valid framework ID characters
        # Valid format: lowercase letters and underscores (e.g., "coding_technical")
        if not re.match(r"^[a-z_]+$", framework):
            raise ValidationError(
                "Framework must contain only lowercase letters and underscores",
                field="framework",
            )

    return prompt, framework


# =============================================================================
# SECURITY VALIDATION
# =============================================================================

def _contains_suspicious_patterns(text: str) -> bool:
    """
    Check for suspicious patterns that might indicate malicious input.
    
    This function scans the input text for common attack patterns including:
    - XSS (Cross-Site Scripting) attempts
    - JavaScript injection
    - Template injection (Jinja2, etc.)
    - Expression injection
    
    Note: This is a basic check. Production systems may need more
    sophisticated validation (e.g., using a dedicated security library).
    
    Args:
        text: The input text to scan
    
    Returns:
        bool: True if suspicious patterns found, False otherwise
    """
    # List of regex patterns to check for
    suspicious_patterns = [
        r"<script\b",       # HTML script tags (XSS)
        r"javascript:",     # JavaScript URLs
        r"data:text/html",  # Data URLs with HTML content
        r"\{\{.*\}\}",      # Template injection (e.g., Jinja2: {{ code }})
        r"\$\{.*\}",        # Expression injection (e.g., ${code})
    ]

    # Check each pattern against lowercase text
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


# =============================================================================
# CONTENT TYPE VALIDATION
# =============================================================================

def validate_content_type() -> None:
    """
    Validate that the request has the correct Content-Type header.
    
    For POST, PUT, and PATCH requests, the Content-Type must be
    application/json. This ensures the request body can be properly
    parsed as JSON.
    
    Raises:
        ValidationError: If Content-Type is not application/json
            (status code 415 Unsupported Media Type)
    
    Example:
        @app.route('/api/data', methods=['POST'])
        def create_data():
            validate_content_type()  # Raises if not JSON
            data = request.get_json()
            ...
    """
    content_type = request.content_type or ""

    # Only check for methods that have request bodies
    if request.method in ("POST", "PUT", "PATCH"):
        if "application/json" not in content_type:
            raise ValidationError(
                "Content-Type must be application/json",
                status_code=415,  # Unsupported Media Type
            )


# =============================================================================
# URL PARAMETER VALIDATION
# =============================================================================

def validate_framework_id(framework_id: str) -> str:
    """
    Validate a framework ID from URL parameters.
    
    Framework IDs must follow the format used in the framework registry:
    lowercase letters and underscores only (e.g., "coding_technical").
    
    Args:
        framework_id: The framework ID from the URL path
    
    Returns:
        str: Validated and normalized (lowercase) framework ID
    
    Raises:
        ValidationError: If framework ID is invalid
    
    Example:
        @app.route('/frameworks/<framework_id>')
        def get_framework(framework_id):
            framework_id = validate_framework_id(framework_id)
            ...
    """
    # Check for empty/missing ID
    if not framework_id:
        raise ValidationError("Framework ID is required")

    # Normalize: strip whitespace and convert to lowercase
    framework_id = framework_id.strip().lower()

    # Format validation - must match expected pattern
    if not re.match(r"^[a-z_]+$", framework_id):
        raise ValidationError(
            "Framework ID must contain only lowercase letters and underscores"
        )

    # Length limit to prevent abuse
    if len(framework_id) > 50:
        raise ValidationError("Framework ID is too long")

    return framework_id
