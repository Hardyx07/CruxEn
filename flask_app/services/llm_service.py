"""
LLM Service Module
==================

This module handles all interactions with Large Language Model (LLM) APIs,
specifically the Groq API which provides an OpenAI-compatible interface.

The service is designed to:
- Encapsulate all LLM-related logic in one place
- Provide clean error handling with custom exceptions
- Return structured responses using dataclasses
- Support logging for debugging and monitoring

Classes:
--------
- LLMError: Custom exception for LLM-related errors
- LLMResponse: Structured response from LLM API
- LLMService: Main service class for LLM interactions

Usage:
------
    from services.llm_service import LLMService, LLMError
    
    service = LLMService(api_key="your-api-key")
    
    try:
        response = service.optimize_prompt(
            user_prompt="Write code to sort a list",
            framework_name="Coding & Technical",
            framework_desc="Code generation and debugging",
            role_template="Senior Software Engineer",
            confidence=0.85
        )
        print(response.content)
    except LLMError as e:
        print(f"Error: {e.message} (Status: {e.status_code})")
"""

import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests

# Module-level logger for LLM service operations
logger = logging.getLogger(__name__)


# =============================================================================
# CUSTOM EXCEPTION
# =============================================================================

class LLMError(Exception):
    """
    Custom exception for LLM-related errors.
    
    This exception provides structured error information that can be
    easily converted to HTTP responses by the Flask error handler.
    
    Attributes:
        message (str): Human-readable error message
        status_code (int): HTTP status code to return (default: 500)
        details (str, optional): Additional error details (e.g., API response)
    
    Example:
        raise LLMError(
            message="API rate limit exceeded",
            status_code=429,
            details="Retry after 60 seconds"
        )
    """

    def __init__(self, message: str, status_code: int = 500, details: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


# =============================================================================
# RESPONSE DATACLASS
# =============================================================================

@dataclass
class LLMResponse:
    """
    Structured response from LLM API calls.
    
    Using a dataclass provides:
    - Type hints for IDE support
    - Automatic __init__, __repr__, etc.
    - Clean attribute access (response.content vs response['content'])
    
    Attributes:
        content (str): The generated text content from the LLM
        model (str): The model that generated the response
        usage (dict, optional): Token usage statistics
            - prompt_tokens: Tokens in the input
            - completion_tokens: Tokens in the output
            - total_tokens: Sum of both
        finish_reason (str, optional): Why generation stopped
            - "stop": Natural completion
            - "length": Hit max_tokens limit
            - "content_filter": Blocked by safety filter
    """

    content: str                              # The LLM's response text
    model: str                                # Model identifier
    usage: Optional[Dict[str, int]] = None    # Token usage stats
    finish_reason: Optional[str] = None       # Completion reason


# =============================================================================
# LLM SERVICE CLASS
# =============================================================================

class LLMService:
    """
    Service class for LLM API interactions.
    
    This class encapsulates all communication with the Groq API,
    providing a clean interface for prompt optimization.
    
    Attributes:
        api_key (str): Groq API authentication key
        api_url (str): API endpoint URL
        model (str): LLM model to use
        timeout (int): Request timeout in seconds
    
    Example:
        service = LLMService(
            api_key="gsk_...",
            model="llama-3.3-70b-versatile",
            timeout=30
        )
        
        response = service.optimize_prompt(
            user_prompt="Help me write better code",
            framework_name="Coding & Technical",
            framework_desc="...",
            role_template="Senior Developer",
            confidence=0.9
        )
    """

    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.groq.com/openai/v1/chat/completions",
        model: str = "llama-3.3-70b-versatile",
        timeout: int = 30,
    ):
        """
        Initialize the LLM service.
        
        Args:
            api_key: Groq API key (required)
            api_url: API endpoint (default: Groq's OpenAI-compatible endpoint)
            model: Model identifier (default: llama-3.3-70b-versatile)
            timeout: Request timeout in seconds (default: 30)
        
        Raises:
            ValueError: If api_key is empty or None
        """
        # Validate API key is provided
        if not api_key:
            raise ValueError("API key is required for LLM service")

        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for API requests.
        
        Returns:
            dict: Headers including Authorization and Content-Type
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # -------------------------------------------------------------------------
    # Main Public Method
    # -------------------------------------------------------------------------

    def optimize_prompt(
        self,
        user_prompt: str,
        framework_name: str,
        framework_desc: str,
        role_template: str,
        confidence: float,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        """
        Optimize a user prompt using the LLM with framework context.
        
        This method sends the user's prompt to the LLM along with context
        about the detected framework, allowing the LLM to rewrite the
        prompt in a more structured, effective way.
        
        Args:
            user_prompt: The original user prompt to optimize
            framework_name: Name of the detected/selected framework
                (e.g., "Coding & Technical")
            framework_desc: Description of what the framework is for
            role_template: Role persona for the optimization
                (e.g., "Senior Software Engineer")
            confidence: Framework detection confidence (0.0 to 1.0)
            temperature: LLM creativity setting (0.0 = deterministic,
                1.0 = creative). Default 0.7 balances both.
            max_tokens: Maximum tokens in the response. Default 2048
                is sufficient for most optimized prompts.
        
        Returns:
            LLMResponse: Structured response with optimized prompt
        
        Raises:
            LLMError: On API errors, timeouts, or parsing failures
        
        Example:
            response = service.optimize_prompt(
                user_prompt="write sorting code",
                framework_name="Coding & Technical",
                framework_desc="Code generation and debugging",
                role_template="Senior Software Engineer",
                confidence=0.85
            )
            print(response.content)  # The optimized prompt
        """
        # Build the system message with framework context
        system_message = self._build_system_message(
            framework_name, framework_desc, role_template, confidence
        )

        # Make the API request
        return self._make_chat_request(
            system_message=system_message,
            user_message=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    # -------------------------------------------------------------------------
    # Private Helper Methods
    # -------------------------------------------------------------------------

    def _build_system_message(
        self,
        framework_name: str,
        framework_desc: str,
        role_template: str,
        confidence: float,
    ) -> str:
        """
        Build the system message for prompt optimization.
        
        The system message instructs the LLM on how to behave and
        provides context about the framework to use.
        
        Args:
            framework_name: Name of the optimization framework
            framework_desc: Description of the framework
            role_template: Role persona to adopt
            confidence: Detection confidence percentage
        
        Returns:
            str: Formatted system message for the LLM
        """
        return f"""You are a prompt engineering specialist. 
Your task is to improve and optimize user prompts based on the following framework and context.

Framework: {framework_name}
Description: {framework_desc}
Role/Context: {role_template}
Confidence: {confidence:.0%}

Take the user's raw prompt and rewrite it to be more systematic, structured, and result-oriented using the specified framework principles.
Return ONLY the optimized prompt, nothing else."""

    def _make_chat_request(
        self,
        system_message: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        """
        Make a chat completion request to the LLM API.
        
        This method handles the actual HTTP communication with the API,
        including error handling for various failure modes.
        
        Args:
            system_message: System context/instructions for the LLM
            user_message: The user's message/prompt
            temperature: Creativity setting (0.0-1.0)
            max_tokens: Maximum response length
        
        Returns:
            LLMResponse: Parsed response from the API
        
        Raises:
            LLMError: On any API or processing error
                - 504 status: Timeout
                - 502 status: Connection error
                - Other: API-specific error codes
        """
        # Build the request payload (OpenAI-compatible format)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            # Log the request (useful for debugging)
            logger.info(
                "Making LLM request",
                extra={"model": self.model, "prompt_length": len(user_message)},
            )

            # Make the HTTP POST request
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout,
            )

            # Handle successful response
            if response.status_code == 200:
                return self._parse_response(response.json())
            
            # Handle API error responses
            else:
                logger.error(
                    "LLM API error",
                    extra={"status_code": response.status_code, "response": response.text},
                )
                raise LLMError(
                    message=f"LLM API error: {response.status_code}",
                    status_code=response.status_code,
                    details=response.text,
                )

        # Handle timeout errors
        except requests.exceptions.Timeout:
            logger.error("LLM API timeout", extra={"timeout": self.timeout})
            raise LLMError(
                message="LLM API request timed out",
                status_code=504,  # Gateway Timeout
            )
        
        # Handle connection/network errors
        except requests.exceptions.RequestException as e:
            logger.error("LLM API request failed", extra={"error": str(e)})
            raise LLMError(
                message=f"LLM API request failed: {str(e)}",
                status_code=502,  # Bad Gateway
            )

    def _parse_response(self, response_data: Dict[str, Any]) -> LLMResponse:
        """
        Parse the API response into an LLMResponse object.
        
        The Groq API returns responses in OpenAI-compatible format:
        {
            "choices": [
                {
                    "message": {"content": "..."},
                    "finish_reason": "stop"
                }
            ],
            "model": "llama-3.3-70b-versatile",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, ...}
        }
        
        Args:
            response_data: Raw JSON response from the API
        
        Returns:
            LLMResponse: Structured response object
        
        Raises:
            LLMError: If response format is unexpected
        """
        try:
            # Extract the first choice (we only request one)
            choice = response_data["choices"][0]
            
            return LLMResponse(
                content=choice["message"]["content"],
                model=response_data.get("model", self.model),
                usage=response_data.get("usage"),
                finish_reason=choice.get("finish_reason"),
            )
            
        except (KeyError, IndexError) as e:
            # Log and raise if response doesn't match expected format
            logger.error("Failed to parse LLM response", extra={"error": str(e)})
            raise LLMError(
                message="Failed to parse LLM response",
                status_code=500,
                details=str(e),
            )

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Check if the LLM service is accessible.
        
        Makes a minimal API request to verify connectivity and
        authentication. Useful for health check endpoints.
        
        Returns:
            bool: True if service is accessible, False otherwise
        
        Example:
            if service.health_check():
                print("LLM service is healthy")
            else:
                print("LLM service is unavailable")
        """
        try:
            # Make a minimal test request
            self._make_chat_request(
                system_message="Respond with 'ok'",
                user_message="test",
                max_tokens=5,  # Minimal tokens to reduce cost
            )
            return True
        except LLMError:
            return False
