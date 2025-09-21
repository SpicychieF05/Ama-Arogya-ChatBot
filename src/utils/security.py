"""
Security utilities for the health chatbot API.
Provides security middleware, validation, rate limiting, and monitoring functionality.
"""

import logging
import time
import asyncio
import hashlib
import re
import ipaddress
from typing import Dict, List, Set, Any, Optional, Callable
from functools import wraps
from collections import defaultdict, deque

from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Configure security logger
security_logger = logging.getLogger("security")

# Global storage for banned IPs and rate limiting
banned_ips: Set[str] = set()
rate_limit_storage: Dict[str, deque] = defaultdict(deque)
security_events: deque = deque(maxlen=1000)

# Security configuration
RATE_LIMIT_REQUESTS = 100  # requests per minute
RATE_LIMIT_WINDOW = 60     # seconds
MAX_MESSAGE_LENGTH = 1000
MAX_SENDER_ID_LENGTH = 100
SUSPICIOUS_PATTERNS = [
    r'<script[^>]*>.*?</script>',
    r'javascript:',
    r'on\w+\s*=',
    r'<iframe[^>]*>',
    r'eval\s*\(',
    r'document\.',
    r'window\.',
]


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware to handle IP filtering, basic attack prevention,
    and request validation.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process each request through security checks."""
        start_time = time.time()

        # Get client IP
        client_ip = self._get_client_ip(request)

        # Check if IP is banned
        if client_ip in banned_ips:
            log_security_event(
                'blocked_request',
                {'ip': client_ip, 'reason': 'banned_ip'},
                request
            )
            return JSONResponse(
                status_code=403,
                content={"detail": "Access denied"}
            )

        # Check rate limiting
        if not check_rate_limit(client_ip):
            log_security_event(
                'rate_limit_exceeded',
                {'ip': client_ip},
                request
            )
            # Ban IP temporarily for excessive requests
            banned_ips.add(client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        # Process request
        try:
            response = await call_next(request)

            # Log successful request
            processing_time = time.time() - start_time
            if processing_time > 5.0:  # Log slow requests
                log_security_event(
                    'slow_request',
                    {
                        'ip': client_ip,
                        'path': str(request.url.path),
                        'processing_time': processing_time
                    },
                    request
                )

            return response

        except Exception as e:
            log_security_event(
                'middleware_error',
                {'ip': client_ip, 'error': str(e)},
                request
            )
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers."""
        # Check for forwarded headers first (for reverse proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"


class ContentSecurityValidator:
    """
    Validates and sanitizes content for security threats.
    """

    @staticmethod
    def validate_chat_message(message: str, language: str) -> Dict[str, Any]:
        """
        Validate chat message content for security issues.

        Args:
            message: The chat message to validate
            language: The language code

        Returns:
            Dict containing validated message and language

        Raises:
            HTTPException: If validation fails
        """
        if not message or not isinstance(message, str):
            raise HTTPException(
                status_code=400,
                detail="Message is required and must be a string"
            )

        if len(message) > MAX_MESSAGE_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Message too long. Maximum {MAX_MESSAGE_LENGTH} characters allowed"
            )

        # Check for suspicious patterns
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Message contains potentially harmful content"
                )

        # Validate language
        if not language or not isinstance(language, str):
            language = "en"  # Default to English

        if len(language) > 10:
            raise HTTPException(
                status_code=400,
                detail="Invalid language code"
            )

        # Clean the language code
        language = re.sub(r'[^a-zA-Z-]', '', language).lower()

        return {
            'message': sanitize_input(message),
            'language': language
        }


def check_rate_limit(identifier: str) -> bool:
    """
    Check if the identifier (usually IP) is within rate limits.

    Args:
        identifier: The identifier to check (IP address, user ID, etc.)

    Returns:
        True if within limits, False if rate limit exceeded
    """
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW

    # Get the request times for this identifier
    requests = rate_limit_storage[identifier]

    # Remove old requests outside the window
    while requests and requests[0] < window_start:
        requests.popleft()

    # Check if we're within the limit
    if len(requests) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    requests.append(current_time)

    return True


def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent XSS and injection attacks.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)

    # Remove or escape potentially dangerous characters
    # Replace HTML entities
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    text = text.replace('/', '&#x2F;')

    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

    # Remove or escape script-related content
    for pattern in SUSPICIOUS_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Limit length to prevent memory issues
    if len(text) > MAX_MESSAGE_LENGTH:
        text = text[:MAX_MESSAGE_LENGTH]

    return text.strip()


def log_security_event(event_type: str, details: Dict[str, Any], request: Optional[Request] = None):
    """
    Log security events for monitoring and analysis.

    Args:
        event_type: Type of security event
        details: Additional details about the event
        request: Optional request object for additional context
    """
    event = {
        'timestamp': time.time(),
        'event_type': event_type,
        'details': details
    }

    if request:
        event['request_info'] = {
            'method': request.method,
            'url': str(request.url),
            'user_agent': request.headers.get('User-Agent', 'unknown'),
            'client_ip': _get_client_ip_from_request(request)
        }

    # Add to security events log
    security_events.append(event)

    # Log to security logger
    security_logger.warning(f"Security event: {event_type} - {details}")


def secure_endpoint(func: Callable) -> Callable:
    """
    Decorator for adding additional security checks to endpoints.

    Args:
        func: The endpoint function to secure

    Returns:
        Decorated function with security checks
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Find the request object in the arguments
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break

        # Also check keyword arguments
        if not request:
            for value in kwargs.values():
                if isinstance(value, Request):
                    request = value
                    break

        if request:
            client_ip = _get_client_ip_from_request(request)

            # Additional security checks can be added here
            # For now, just log the access
            log_security_event(
                'endpoint_access',
                {
                    'endpoint': func.__name__,
                    'ip': client_ip
                },
                request
            )

        # Call the original function
        return await func(*args, **kwargs)

    return wrapper


def _get_client_ip_from_request(request: Request) -> str:
    """Helper function to extract client IP from request."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    return request.client.host if request.client else "unknown"


def clear_banned_ips():
    """Clear banned IPs (useful for scheduled cleanup)."""
    global banned_ips
    banned_ips.clear()


def get_security_stats() -> Dict[str, Any]:
    """
    Get current security statistics.

    Returns:
        Dictionary with security statistics
    """
    return {
        'banned_ips_count': len(banned_ips),
        'active_rate_limits': len(rate_limit_storage),
        'recent_events': len(security_events),
        'banned_ips': list(banned_ips) if len(banned_ips) < 50 else f"{len(banned_ips)} IPs"
    }
