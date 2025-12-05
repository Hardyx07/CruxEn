"""
Middleware Package
==================

This package contains middleware components for request processing,
including logging, validation, and security checks.

Available Components:
--------------------

Logging:
    - setup_logging: Configure structured logging with request IDs
    - RequestLoggingMiddleware: Automatic request/response logging

Validation:
    - validate_prompt_input: Validate POST body for prompt endpoints
    - validate_content_type: Ensure correct Content-Type header
    - validate_framework_id: Validate URL parameters
    - ValidationError: Custom exception for validation failures

Design Principles:
-----------------
1. Separation of Concerns: Each middleware handles one aspect
2. Fail Fast: Validation errors raised early before processing
3. Security First: Input sanitization against XSS/injection
4. Observability: Request tracking with unique IDs

Usage:
------
    from middleware import (
        setup_logging,
        RequestLoggingMiddleware,
        validate_prompt_input,
        ValidationError,
    )
    
    # Setup logging
    setup_logging(app, level=logging.INFO)
    RequestLoggingMiddleware(app)
    
    # Validate input
    try:
        prompt, framework = validate_prompt_input(data)
    except ValidationError as e:
        return jsonify(e.to_dict()), e.status_code
"""

from .logging_middleware import setup_logging, RequestLoggingMiddleware
from .validation import validate_prompt_input, ValidationError

# Public API
__all__ = [
    # Logging
    "setup_logging",
    "RequestLoggingMiddleware",
    # Validation
    "validate_prompt_input",
    "ValidationError",
]
