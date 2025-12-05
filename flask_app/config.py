"""
Application Configuration Module
================================

This module provides environment-based configuration for the Flask application.
It follows the 12-factor app methodology by loading settings from environment
variables with sensible defaults.

Configuration Classes:
---------------------
- Config: Base configuration with defaults
- DevelopmentConfig: Local development settings
- ProductionConfig: Production deployment settings  
- TestingConfig: Test suite settings

Environment Variables:
---------------------
- FLASK_ENV: Environment name (development/production/testing)
- ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins
- GROQ_API_KEY: API key for Groq LLM service
- GROQ_MODEL: LLM model to use (default: llama-3.3-70b-versatile)
- GROQ_TIMEOUT: API request timeout in seconds
- RATE_LIMIT_DEFAULT: Default rate limit (e.g., "100 per hour")
- RATE_LIMIT_CHAT: Rate limit for /chat endpoint
- RATE_LIMIT_OPTIMIZE: Rate limit for /optimize endpoint
- MAX_PROMPT_LENGTH: Maximum allowed prompt length
- MIN_PROMPT_LENGTH: Minimum required prompt length

Usage:
------
    from config import get_config
    config = get_config()
    print(config.GROQ_MODEL)
"""

import os
from typing import List

from dotenv import load_dotenv

# Load environment variables from .env file (if present)
# This allows local development without setting system env vars
load_dotenv()


# =============================================================================
# BASE CONFIGURATION
# =============================================================================

class Config:
    """
    Base configuration class with default values.
    
    All configuration values can be overridden via environment variables.
    This class serves as the foundation for environment-specific configs.
    """

    # -------------------------------------------------------------------------
    # Flask Core Settings
    # -------------------------------------------------------------------------
    DEBUG = False      # Disable debug mode by default (security)
    TESTING = False    # Not in test mode by default

    # -------------------------------------------------------------------------
    # CORS (Cross-Origin Resource Sharing) Settings
    # -------------------------------------------------------------------------
    # Allowed origins for cross-origin requests
    # Format in env: comma-separated URLs (e.g., "http://localhost:3000,https://app.example.com")
    ALLOWED_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,https://crux-en.vercel.app"  # Default origins
        ).split(",")
        if origin.strip()  # Filter out empty strings
    ]

    # -------------------------------------------------------------------------
    # Groq LLM API Settings
    # -------------------------------------------------------------------------
    # API key for authentication (required for /chat endpoint)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Groq API endpoint (OpenAI-compatible)
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # LLM model to use (Groq supports various models)
    # Options: llama-3.3-70b-versatile, mixtral-8x7b-32768, etc.
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Request timeout in seconds (prevents hanging requests)
    GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "30"))

    # -------------------------------------------------------------------------
    # Rate Limiting Settings
    # -------------------------------------------------------------------------
    # Format: "<number> per <period>" (e.g., "100 per hour", "10 per minute")
    # Supported periods: second, minute, hour, day
    
    # Default limit for all endpoints
    RATE_LIMIT_DEFAULT = os.getenv("RATE_LIMIT_DEFAULT", "100 per hour")
    
    # Stricter limit for /chat (due to LLM API costs)
    RATE_LIMIT_CHAT = os.getenv("RATE_LIMIT_CHAT", "30 per minute")
    
    # Moderate limit for /optimize (local processing only)
    RATE_LIMIT_OPTIMIZE = os.getenv("RATE_LIMIT_OPTIMIZE", "60 per minute")

    # -------------------------------------------------------------------------
    # Input Validation Settings
    # -------------------------------------------------------------------------
    # Maximum characters allowed in a prompt
    MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "10000"))
    
    # Minimum characters required (prevents empty/trivial prompts)
    MIN_PROMPT_LENGTH = int(os.getenv("MIN_PROMPT_LENGTH", "3"))


# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    Optimized for local development with:
    - Debug mode enabled (auto-reload, detailed errors)
    - Localhost origins allowed
    - Verbose logging
    """

    DEBUG = True  # Enable debug mode for development
    
    # Allow all common localhost variations for development
    ALLOWED_ORIGINS = [
        "http://localhost:3000",    # Next.js default
        "http://127.0.0.1:3000",    # Alternative localhost
        "http://localhost:5000",     # Flask default
    ]


# =============================================================================
# PRODUCTION CONFIGURATION
# =============================================================================

class ProductionConfig(Config):
    """
    Production environment configuration.
    
    Hardened settings for production deployment:
    - Debug mode disabled (security)
    - Restricted CORS origins
    - Production-only origins
    """

    DEBUG = False  # NEVER enable debug in production
    
    # Only allow production origins (loaded from env)
    # Set ALLOWED_ORIGINS env var in production deployment
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "https://crux-en.vercel.app"  # Production frontend URL
        ).split(",")
        if origin.strip()
    ]


# =============================================================================
# TESTING CONFIGURATION
# =============================================================================

class TestingConfig(Config):
    """
    Testing environment configuration.
    
    Optimized for running test suites:
    - Testing mode enabled (disables error catching)
    - Mock API key for tests
    - Relaxed rate limits (no blocking during tests)
    """

    TESTING = True   # Enable Flask testing mode
    DEBUG = True     # Verbose output for test debugging
    
    # Test origins
    ALLOWED_ORIGINS = ["http://localhost:3000", "http://testserver"]
    
    # Mock API key (tests should mock the actual API calls)
    GROQ_API_KEY = "test-api-key"
    
    # Relaxed rate limits for test speed
    RATE_LIMIT_DEFAULT = "1000 per hour"
    RATE_LIMIT_CHAT = "1000 per minute"
    RATE_LIMIT_OPTIMIZE = "1000 per minute"


# =============================================================================
# CONFIGURATION FACTORY
# =============================================================================

def get_config():
    """
    Get the appropriate configuration based on FLASK_ENV environment variable.
    
    Environment Detection:
    - FLASK_ENV=development -> DevelopmentConfig
    - FLASK_ENV=production  -> ProductionConfig
    - FLASK_ENV=testing     -> TestingConfig
    - (default)             -> DevelopmentConfig
    
    Returns:
        Config: Instantiated configuration object
    
    Example:
        config = get_config()
        print(f"Debug mode: {config.DEBUG}")
        print(f"Allowed origins: {config.ALLOWED_ORIGINS}")
    """
    # Read environment, default to development for safety
    env = os.getenv("FLASK_ENV", "development").lower()
    
    # Map environment names to config classes
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    # Return instantiated config (defaults to DevelopmentConfig if unknown env)
    return configs.get(env, DevelopmentConfig)()
