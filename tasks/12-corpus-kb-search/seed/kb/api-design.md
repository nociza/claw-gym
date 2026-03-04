# RESTful API Design Guide

## Principles
- Use nouns for resources, verbs for actions
- Use HTTP methods correctly (GET, POST, PUT, DELETE, PATCH)
- Return appropriate status codes
- Support pagination, filtering, and sorting

## Versioning
Prefer URL path versioning: `/api/v1/users`
Alternatives: header versioning, query parameter versioning

## Error Handling
Return consistent error responses:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{"field": "email", "reason": "required"}]
  }
}
```

## Rate Limiting
Implement rate limiting to protect your API:
- Use token bucket algorithm
- Return 429 Too Many Requests with Retry-After header
- Document rate limits in API docs

## Authentication
- Use OAuth 2.0 for third-party access
- Use API keys for server-to-server communication
- JWT tokens for session management

## Documentation
Use OpenAPI (Swagger) for API documentation. Generate interactive docs with tools like Redoc or Swagger UI.
