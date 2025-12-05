"""
CruxEn Flask API - Prompt Optimization Service
===============================================

A production-ready REST API for intelligent prompt optimization using
framework-based detection and LLM enhancement.

Features:
---------
- CORS restricted to specific origins (security)
- Input validation and sanitization (XSS/injection protection)
- Rate limiting to prevent abuse (configurable limits)
- Structured logging with request IDs (debugging/monitoring)
- Separated LLM service layer (clean architecture)

Endpoints:
----------
- GET  /           : Service info and status
- GET  /health     : Health check for monitoring
- GET  /frameworks : List all available optimization frameworks
- GET  /frameworks/<id> : Get details of a specific framework
- POST /optimize   : Optimize a prompt using framework detection
- POST /chat       : LLM-enhanced prompt optimization

Author: CruxEn Team
Version: 2.0
"""

import logging
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import get_config
from prompt_optimizer import PromptOptimizationSystem
from services.llm_service import LLMService, LLMError
from middleware.logging_middleware import setup_logging, RequestLoggingMiddleware
from middleware.validation import (
    validate_prompt_input,
    validate_content_type,
    validate_framework_id,
    ValidationError,
)

# =============================================================================
# GLOBAL INSTANCES
# =============================================================================
# These are initialized in create_app() using the application factory pattern.
# Using globals allows access from route handlers while maintaining testability.

prompt_system: PromptOptimizationSystem = None  # Framework detection & optimization
llm_service: LLMService = None                   # Groq/LLM API integration
limiter: Limiter = None                          # Rate limiting middleware


# =============================================================================
# APPLICATION FACTORY
# =============================================================================

def create_app(config=None):
    """
    Application factory pattern for creating Flask app instances.
    
    This pattern allows:
    - Multiple app instances (useful for testing)
    - Different configurations per instance
    - Lazy initialization of extensions
    
    Args:
        config: Optional configuration object. If None, loads from environment.
    
    Returns:
        Flask: Configured Flask application instance
    
    Example:
        # Production
        app = create_app()
        
        # Testing
        from config import TestingConfig
        test_app = create_app(TestingConfig())
    """
    global prompt_system, llm_service, limiter

    app = Flask(__name__)

    # -------------------------------------------------------------------------
    # Configuration Loading
    # -------------------------------------------------------------------------
    # Load environment-specific config (development/production/testing)
    if config is None:
        config = get_config()

    # Store frequently accessed config values in app.config for easy access
    app.config["ALLOWED_ORIGINS"] = config.ALLOWED_ORIGINS
    app.config["MAX_PROMPT_LENGTH"] = config.MAX_PROMPT_LENGTH
    app.config["MIN_PROMPT_LENGTH"] = config.MIN_PROMPT_LENGTH
    app.config["TESTING"] = config.TESTING

    # -------------------------------------------------------------------------
    # Logging Setup
    # -------------------------------------------------------------------------
    # Configure structured logging with request IDs for traceability
    log_level = logging.DEBUG if config.DEBUG else logging.INFO
    setup_logging(app, level=log_level)

    # -------------------------------------------------------------------------
    # CORS Configuration
    # -------------------------------------------------------------------------
    # Restrict cross-origin requests to specific allowed domains
    # This prevents unauthorized domains from making API requests
    CORS(
        app,
        resources={r"/*": {"origins": config.ALLOWED_ORIGINS}},
        supports_credentials=True,  # Allow cookies/auth headers
    )

    # -------------------------------------------------------------------------
    # Rate Limiting
    # -------------------------------------------------------------------------
    # Protect against abuse by limiting requests per IP address
    # Uses in-memory storage (consider Redis for production clusters)
    limiter = Limiter(
        key_func=get_remote_address,  # Rate limit by client IP
        app=app,
        default_limits=[config.RATE_LIMIT_DEFAULT],  # e.g., "100 per hour"
        storage_uri="memory://",  # In-memory storage (use redis:// for production)
    )

    # -------------------------------------------------------------------------
    # Middleware Registration
    # -------------------------------------------------------------------------
    # Add request logging with timing and unique request IDs
    RequestLoggingMiddleware(app)

    # -------------------------------------------------------------------------
    # Service Initialization
    # -------------------------------------------------------------------------
    # Initialize the prompt optimization system (framework detection)
    prompt_system = PromptOptimizationSystem()

    # Initialize LLM service if API key is available
    # The /chat endpoint requires this; /optimize works without it
    if config.GROQ_API_KEY:
        llm_service = LLMService(
            api_key=config.GROQ_API_KEY,
            api_url=config.GROQ_API_URL,
            model=config.GROQ_MODEL,
            timeout=config.GROQ_TIMEOUT,
        )
    else:
        app.logger.warning("GROQ_API_KEY not set - /chat endpoint will be unavailable")
        llm_service = None

    # -------------------------------------------------------------------------
    # Register Handlers and Routes
    # -------------------------------------------------------------------------
    register_error_handlers(app)
    register_routes(app, config)

    return app


# =============================================================================
# ERROR HANDLERS
# =============================================================================

def register_error_handlers(app):
    """
    Register global error handlers for consistent error responses.
    
    All errors are returned as JSON with appropriate HTTP status codes.
    Error responses follow the format: {"error": "message", "field": "optional"}
    
    Args:
        app: Flask application instance
    """

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        Handle input validation errors (400 Bad Request).
        
        These occur when user input fails validation checks
        (missing fields, invalid format, suspicious content, etc.)
        """
        app.logger.warning("Validation error: %s", error.message)
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(LLMError)
    def handle_llm_error(error):
        """
        Handle LLM service errors (various status codes).
        
        These occur when the Groq API fails, times out, or returns errors.
        Status codes: 502 (connection), 504 (timeout), or API-specific codes.
        """
        app.logger.error("LLM error: %s", error.message)
        response = {"error": error.message}
        if error.details:
            response["details"] = error.details
        return jsonify(response), error.status_code

    @app.errorhandler(429)
    def handle_rate_limit(error):
        """
        Handle rate limit exceeded errors (429 Too Many Requests).
        
        Occurs when a client exceeds their allowed request quota.
        Response includes retry information.
        """
        app.logger.warning("Rate limit exceeded for %s", request.remote_addr)
        return jsonify({
            "error": "Rate limit exceeded. Please try again later.",
            "retry_after": error.description,
        }), 429

    @app.errorhandler(500)
    def handle_internal_error(error):
        """
        Handle unexpected internal errors (500 Internal Server Error).
        
        Catches any unhandled exceptions to prevent exposing internal details.
        Full stack trace is logged for debugging.
        """
        app.logger.exception("Internal server error: %s", error)
        return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# ROUTE REGISTRATION
# =============================================================================

def register_routes(app, config):
    """
    Register all API route handlers.
    
    Routes are organized by functionality:
    - Info routes: /, /health
    - Framework routes: /frameworks, /frameworks/<id>
    - Optimization routes: /optimize, /chat
    
    Args:
        app: Flask application instance
        config: Configuration object with settings
    """

    # -------------------------------------------------------------------------
    # Info Routes
    # -------------------------------------------------------------------------

    @app.route("/")
    def hello_world():
        """
        Root endpoint - Returns service information.
        
        Used for basic connectivity checks and service discovery.
        
        Returns:
            JSON: Service name, version, and status
        """
        return jsonify({
            "service": "CruxEn Prompt Optimization API",
            "version": "2.0",
            "status": "running",
        })

    @app.route("/health")
    def health_check():
        """
        Health check endpoint for monitoring and load balancers.
        
        Returns service health status and availability of optional features.
        Use this endpoint for:
        - Kubernetes/Docker health probes
        - Load balancer health checks
        - Monitoring dashboards
        
        Returns:
            JSON: Health status and feature availability
        """
        return jsonify({
            "status": "healthy",
            "llm_available": llm_service is not None,
        })

    # -------------------------------------------------------------------------
    # Framework Routes
    # -------------------------------------------------------------------------

    @app.route("/frameworks", methods=["GET"])
    def get_frameworks():
        """
        List all available prompt optimization frameworks.
        
        Returns comprehensive information about each framework including:
        - ID and name
        - Description and ideal use cases
        - Example inputs
        - Role personas
        
        Returns:
            JSON: Array of framework objects
        """
        try:
            frameworks = prompt_system.list_available_frameworks()
            return jsonify(frameworks)
        except Exception as e:
            app.logger.exception("Failed to fetch frameworks: %s", e)
            return jsonify({"error": "Failed to fetch frameworks"}), 500

    @app.route("/frameworks/<framework_id>", methods=["GET"])
    def get_framework_details(framework_id):
        """
        Get detailed information about a specific framework.
        
        Args:
            framework_id: Framework identifier (e.g., "coding_technical")
        
        Returns:
            JSON: Framework details or 404 if not found
        
        Example:
            GET /frameworks/coding_technical
        """
        try:
            # Validate and normalize the framework ID
            framework_id = validate_framework_id(framework_id)
            framework = prompt_system.get_framework_by_id(framework_id)
            
            if framework:
                return jsonify(framework)
            else:
                return jsonify({"error": f'Framework "{framework_id}" not found'}), 404
                
        except ValidationError:
            raise  # Let error handler deal with it
        except Exception as e:
            app.logger.exception("Failed to fetch framework details: %s", e)
            return jsonify({"error": "Failed to fetch framework details"}), 500

    # -------------------------------------------------------------------------
    # Optimization Routes
    # -------------------------------------------------------------------------

    @app.route("/optimize", methods=["POST"])
    @limiter.limit(config.RATE_LIMIT_OPTIMIZE)  # e.g., "60 per minute"
    def optimize_prompt():
        """
        Optimize a user prompt using framework-based detection.
        
        This endpoint analyzes the user's prompt, detects the most suitable
        framework, and returns an optimized version using that framework's
        structure and best practices.
        
        Request Body:
            {
                "prompt": "user prompt text",      # Required
                "framework": "coding_technical"   # Optional: force specific framework
            }
        
        Returns:
            JSON: Optimized prompt with framework info and quality metrics
        
        Rate Limit:
            60 requests per minute (configurable)
        
        Example:
            POST /optimize
            {"prompt": "write python code to sort a list"}
        """
        # Validate Content-Type header (must be application/json)
        validate_content_type()

        # Validate and extract input data
        data = request.get_json(silent=True)
        prompt, explicit_framework = validate_prompt_input(
            data,
            max_length=config.MAX_PROMPT_LENGTH,
            min_length=config.MIN_PROMPT_LENGTH,
        )

        try:
            # Process through the optimization system
            opt_result = prompt_system.process(prompt, explicit_framework=explicit_framework)
            return jsonify(opt_result)
            
        except ValueError as ve:
            # Convert ValueError to ValidationError for consistent handling
            raise ValidationError(str(ve))
        except Exception as e:
            app.logger.exception("Prompt optimization failed: %s", e)
            return jsonify({"error": "Prompt optimization failed"}), 500

    @app.route("/chat", methods=["POST"])
    @limiter.limit(config.RATE_LIMIT_CHAT)  # e.g., "30 per minute"
    def chat():
        """
        Enhanced prompt optimization with LLM integration.
        
        This endpoint combines framework-based optimization with LLM enhancement:
        1. Detects/applies the appropriate framework
        2. Sends to Groq LLM for intelligent rewriting
        3. Returns the LLM-optimized prompt
        
        Requires GROQ_API_KEY environment variable to be set.
        
        Request Body:
            {
                "prompt": "user prompt text",     # Required
                "framework": "creative_ideation", # Optional: force framework
                "include_meta": true              # Optional: include metadata
            }
        
        Returns:
            JSON: {
                "optimized_prompt": "...",
                "metadata": {...}  # If include_meta=true
            }
        
        Rate Limit:
            30 requests per minute (configurable, stricter due to LLM costs)
        
        Example:
            POST /chat
            {"prompt": "brainstorm startup ideas", "include_meta": true}
        """
        # Check if LLM service is available (requires API key)
        if llm_service is None:
            return jsonify({
                "error": "LLM service not configured. GROQ_API_KEY required."
            }), 503  # Service Unavailable

        # Validate Content-Type header
        validate_content_type()

        # Validate and extract input data
        data = request.get_json(silent=True)
        prompt, explicit_framework = validate_prompt_input(
            data,
            max_length=config.MAX_PROMPT_LENGTH,
            min_length=config.MIN_PROMPT_LENGTH,
        )
        include_meta = bool(data.get("include_meta", False))

        # Step 1: Framework-based optimization
        try:
            opt_result = prompt_system.process(prompt, explicit_framework=explicit_framework)
        except ValueError as ve:
            raise ValidationError(str(ve))
        except Exception as e:
            app.logger.exception("Prompt optimization failed: %s", e)
            return jsonify({"error": "Prompt optimization failed"}), 500

        # Step 2: LLM enhancement
        try:
            llm_response = llm_service.optimize_prompt(
                user_prompt=prompt,
                framework_name=opt_result["framework"]["name"],
                framework_desc=opt_result["framework"]["description"],
                role_template=opt_result["framework"]["role"],
                confidence=opt_result["confidence"],
            )

            # Build response
            response_body = {
                "optimized_prompt": llm_response.content,
            }

            # Include metadata if requested (useful for debugging/analysis)
            if include_meta:
                response_body["metadata"] = {
                    "framework": opt_result["framework"],
                    "confidence": opt_result["confidence"],
                    "reasoning": opt_result["reasoning"],
                    "quality_metrics": opt_result["quality_metrics"],
                    "llm_model": llm_response.model,
                    "usage": llm_response.usage,  # Token usage stats
                }

            return jsonify(response_body)

        except LLMError:
            raise  # Let error handler deal with it
        except Exception as e:
            app.logger.exception("LLM processing failed: %s", e)
            return jsonify({"error": "LLM processing failed"}), 500


# =============================================================================
# APPLICATION INSTANCE
# =============================================================================

# Create the default app instance for production use
# In production, this is imported by gunicorn: gunicorn app:app
app = create_app()

# Development server entry point
if __name__ == "__main__":
    # Run with debug mode for development
    # DO NOT use this in production - use gunicorn instead
    app.run(debug=True)
