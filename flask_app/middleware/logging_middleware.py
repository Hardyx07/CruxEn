"""
Logging Middleware Module
=========================

This module provides structured logging capabilities for the Flask application,
including request tracking with unique IDs and timing information.

Features:
---------
- Unique request IDs for tracing requests through logs
- Request timing (how long each request takes)
- Structured log format with timestamps
- Request ID propagation via X-Request-ID header
- Response timing header (X-Response-Time)

Log Format:
-----------
    [2024-01-15 10:30:45] [INFO] [abc12345] Request started: POST /optimize
    [2024-01-15 10:30:45] [INFO] [abc12345] Request completed: POST /optimize - 200 (125.5ms)

Classes:
--------
- RequestIdFilter: Adds request_id to log records
- RequestLoggingMiddleware: Registers before/after request hooks

Functions:
----------
- setup_logging(): Configure structured logging for the app
- log_endpoint(): Decorator for additional endpoint logging

Usage:
------
    from middleware.logging_middleware import setup_logging, RequestLoggingMiddleware
    
    app = Flask(__name__)
    setup_logging(app, level=logging.INFO)
    RequestLoggingMiddleware(app)
"""

import logging
import time
import uuid
from functools import wraps
from typing import Callable

from flask import Flask, g, request


# =============================================================================
# LOGGING FILTER
# =============================================================================

class RequestIdFilter(logging.Filter):
    """
    Logging filter that adds request_id to log records.
    
    This filter ensures every log message includes a request ID,
    making it easy to trace all logs related to a single request.
    
    The request ID is retrieved from Flask's 'g' object, which stores
    request-local data. If called outside a request context, it falls
    back to placeholder values.
    
    Attributes Added to LogRecord:
        request_id (str): Unique identifier for the current request
    
    Example log output:
        [2024-01-15 10:30:45] [INFO] [abc12345] Some log message
    """

    def filter(self, record):
        """
        Add request_id attribute to the log record.
        
        Args:
            record: The LogRecord to process
        
        Returns:
            bool: Always True (never filters out records)
        """
        try:
            # Try to get request_id from Flask's g object
            record.request_id = getattr(g, "request_id", "no-request")
        except RuntimeError:
            # Outside of application/request context (e.g., during startup or tests)
            record.request_id = "no-context"
        return True


# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(app: Flask, level: int = logging.INFO) -> None:
    """
    Configure structured logging for the Flask application.
    
    This function sets up logging with:
    - Custom format including timestamp, level, and request ID
    - Request ID filter for traceability
    - Configurable log level
    
    The logging is configured for both:
    - Flask's app.logger (for application logs)
    - Root logger (for library/service logs)
    
    Args:
        app: Flask application instance
        level: Logging level (default: logging.INFO)
            Use logging.DEBUG for development
            Use logging.INFO for production
    
    Log Format:
        [YYYY-MM-DD HH:MM:SS] [LEVEL] [request_id] message
    
    Example:
        app = Flask(__name__)
        setup_logging(app, level=logging.DEBUG)
        app.logger.info("Server started")
        # Output: [2024-01-15 10:30:45] [INFO] [no-context] Server started
    """
    # -------------------------------------------------------------------------
    # Clear existing handlers to prevent duplicate logs
    # -------------------------------------------------------------------------
    app.logger.handlers = []

    # -------------------------------------------------------------------------
    # Create and configure stream handler (console output)
    # -------------------------------------------------------------------------
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Define log format with request_id placeholder
    # Format: [timestamp] [level] [request_id] message
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(request_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    
    # Add filter to inject request_id into log records
    handler.addFilter(RequestIdFilter())

    # Apply to Flask's app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(level)

    # -------------------------------------------------------------------------
    # Configure root logger for service modules
    # -------------------------------------------------------------------------
    # This ensures logs from services (like LLMService) also get formatted
    root_logger = logging.getLogger()
    root_logger.handlers = []  # Clear existing handlers
    
    # Create separate handler for root logger
    root_handler = logging.StreamHandler()
    root_handler.setFormatter(formatter)
    root_handler.addFilter(RequestIdFilter())
    
    root_logger.addHandler(root_handler)
    root_logger.setLevel(level)


# =============================================================================
# REQUEST LOGGING MIDDLEWARE
# =============================================================================

class RequestLoggingMiddleware:
    """
    Middleware for automatic request logging with timing and request IDs.
    
    This middleware:
    1. Assigns a unique ID to each request (or uses provided X-Request-ID)
    2. Logs when requests start and complete
    3. Tracks request duration
    4. Adds timing headers to responses
    
    Response Headers Added:
        X-Request-ID: The unique request identifier
        X-Response-Time: How long the request took (e.g., "125.5ms")
    
    Usage:
        app = Flask(__name__)
        RequestLoggingMiddleware(app)
    
    Example logs:
        [2024-01-15 10:30:45] [INFO] [abc12345] Request started: POST /optimize
        [2024-01-15 10:30:45] [INFO] [abc12345] Request completed: POST /optimize - 200 (125.5ms)
    """

    def __init__(self, app: Flask) -> None:
        """
        Initialize middleware and register hooks.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        self._register_hooks()

    def _register_hooks(self) -> None:
        """
        Register before_request and after_request hooks.
        
        These hooks intercept every request to:
        - Set up request context (before)
        - Log completion and add headers (after)
        """

        @self.app.before_request
        def before_request():
            """
            Set up request context before processing.
            
            This hook runs before every request and:
            1. Generates or extracts request ID
            2. Records start time for duration calculation
            3. Logs the request start
            
            Request ID Sources (in order of preference):
            1. X-Request-ID header (if provided by client/proxy)
            2. Auto-generated UUID (truncated to 8 chars for readability)
            """
            # Get or generate request ID
            # Using first 8 chars of UUID for readability in logs
            g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
            
            # Record start time for duration calculation
            g.start_time = time.time()

            # Log request start
            self.app.logger.info(
                "Request started: %s %s",
                request.method,
                request.path,
            )

        @self.app.after_request
        def after_request(response):
            """
            Log completion and add headers after processing.
            
            This hook runs after every request and:
            1. Calculates request duration
            2. Logs completion with status and timing
            3. Adds tracking headers to response
            
            Args:
                response: Flask Response object
            
            Returns:
                Response: Modified response with added headers
            """
            # Calculate request duration
            duration = time.time() - getattr(g, "start_time", time.time())
            duration_ms = round(duration * 1000, 2)  # Convert to milliseconds

            # Log request completion
            self.app.logger.info(
                "Request completed: %s %s - %s (%sms)",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )

            # Add tracking headers to response
            # These are useful for debugging and client-side tracking
            response.headers["X-Request-ID"] = getattr(g, "request_id", "unknown")
            response.headers["X-Response-Time"] = f"{duration_ms}ms"

            return response


# =============================================================================
# OPTIONAL ENDPOINT DECORATOR
# =============================================================================

def log_endpoint(func: Callable) -> Callable:
    """
    Decorator for additional endpoint-specific logging.
    
    This decorator adds entry/exit logging for individual endpoints,
    useful for debugging specific routes or tracking function-level
    execution.
    
    Args:
        func: The endpoint function to wrap
    
    Returns:
        Callable: Wrapped function with logging
    
    Usage:
        @app.route('/api/process')
        @log_endpoint
        def process_data():
            # ... handler code ...
            return jsonify(result)
    
    Example logs:
        [INFO] Entering endpoint: process_data
        [INFO] Endpoint process_data completed successfully
        
        Or on error:
        [ERROR] Endpoint process_data failed: ValueError: ...
    """

    @wraps(func)  # Preserve original function metadata
    def wrapper(*args, **kwargs):
        logging.info("Entering endpoint: %s", func.__name__)
        try:
            result = func(*args, **kwargs)
            logging.info("Endpoint %s completed successfully", func.__name__)
            return result
        except Exception as e:
            # Log the exception with full stack trace
            logging.exception("Endpoint %s failed: %s", func.__name__, str(e))
            raise  # Re-raise to let Flask's error handlers deal with it

    return wrapper
