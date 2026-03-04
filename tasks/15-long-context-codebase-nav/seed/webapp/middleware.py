"""Request middleware pipeline."""

import time
import logging
from functools import wraps
from flask import Flask, request, g, jsonify
from auth import verify_token
from exceptions import AuthenticationError, AppError

logger = logging.getLogger(__name__)


def setup_middleware(app: Flask) -> None:
    """Register all middleware in order."""
    app.before_request(request_logger)
    app.before_request(request_timer)
    app.before_request(authenticate)
    app.after_request(add_security_headers)
    app.errorhandler(Exception)(error_handler)
    app.errorhandler(404)(not_found_handler)


def request_logger():
    """Log incoming requests."""
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")


def request_timer():
    """Track request duration."""
    g.start_time = time.monotonic()


def authenticate():
    """Authenticate requests using JWT tokens."""
    # Skip auth for public endpoints
    public_paths = ["/api/auth/login", "/api/auth/register", "/health"]
    if request.path in public_paths:
        return None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid Authorization header")

    token = auth_header[7:]
    try:
        payload = verify_token(token)
        g.current_user = payload
    except Exception as exc:
        raise AuthenticationError(f"Invalid token: {exc}")


def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Request-Duration"] = str(
        time.monotonic() - g.get("start_time", time.monotonic())
    )
    return response


def error_handler(error):
    """Handle all unhandled exceptions."""
    if isinstance(error, AppError):
        return format_error_response(error.message, error.status_code)

    # BUG: This catches all exceptions but logs the wrong variable name
    # It references 'exc' instead of 'error', which would cause a NameError
    # if a non-AppError exception occurs
    logger.error(f"Unhandled exception: {exc}")
    return format_error_response("Internal server error", 500)


def not_found_handler(error):
    """Handle 404 errors."""
    return format_error_response(f"Not found: {request.path}", 404)


def format_error_response(message: str, status_code: int):
    """Generate standardized JSON error response."""
    return jsonify({
        "error": {
            "message": message,
            "status": status_code,
            "path": request.path,
        }
    }), status_code
