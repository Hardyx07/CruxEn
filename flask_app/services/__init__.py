"""
Services Package
================

This package contains service modules that encapsulate external integrations
and business logic, following the Service Layer pattern.

Available Services:
------------------
- LLMService: Handles all interactions with Groq/LLM APIs
- LLMResponse: Structured response dataclass from LLM calls
- LLMError: Custom exception for LLM-related errors

Design Principles:
-----------------
1. Single Responsibility: Each service handles one external integration
2. Dependency Injection: Services receive configuration via constructor
3. Error Handling: Custom exceptions with HTTP status codes
4. Testability: Services can be easily mocked in tests

Usage:
------
    from services import LLMService, LLMError, LLMResponse
    
    service = LLMService(api_key="your-key")
    try:
        response = service.optimize_prompt(...)
    except LLMError as e:
        print(f"Error: {e.message}")
"""

from .llm_service import LLMService, LLMResponse, LLMError

# Public API - these are importable from 'services' package directly
__all__ = ["LLMService", "LLMResponse", "LLMError"]
