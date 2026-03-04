"""JWT authentication utilities."""

import hashlib
import hmac
import json
import time
import base64
from config import Config
from exceptions import AuthenticationError, TokenExpiredError


def create_token(user_id: int, email: str) -> str:
    """Create a JWT-like token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": int(time.time()),
        "exp": int(time.time()) + Config.JWT_EXPIRY_HOURS * 3600,
    }

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    signing_input = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        Config.JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256
    ).hexdigest()

    return f"{header_b64}.{payload_b64}.{signature}"


def verify_token(token: str) -> dict:
    """Verify and decode a JWT-like token."""
    parts = token.split(".")
    if len(parts) != 3:
        raise AuthenticationError("Invalid token format")

    header_b64, payload_b64, signature = parts

    # Verify signature
    signing_input = f"{header_b64}.{payload_b64}"
    expected_sig = hmac.new(
        Config.JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        raise AuthenticationError("Invalid token signature")

    # Decode payload
    padding = 4 - len(payload_b64) % 4
    payload_b64 += "=" * padding
    payload = json.loads(base64.urlsafe_b64decode(payload_b64))

    # Check expiration
    if payload.get("exp", 0) < time.time():
        raise TokenExpiredError("Token has expired")

    return payload
