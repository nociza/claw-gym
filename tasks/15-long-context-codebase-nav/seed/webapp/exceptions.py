"""Custom exception classes."""


class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(AppError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppError):
    """Raised when user lacks permission."""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, identifier: str = ""):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} '{identifier}' not found"
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, message: str = "Validation failed", errors: list = None):
        super().__init__(message, status_code=400)
        self.errors = errors or []


class ConflictError(AppError):
    """Raised when a resource conflict occurs."""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status_code=409)


class TokenExpiredError(AuthenticationError):
    """Raised when a JWT token has expired."""
    def __init__(self, message: str = "Token expired"):
        super().__init__(message)
