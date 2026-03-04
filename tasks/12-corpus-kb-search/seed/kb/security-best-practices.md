# Application Security Best Practices

## OWASP Top 10 Awareness
Stay current with the OWASP Top 10 vulnerabilities:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration

## Authentication
- Use bcrypt or Argon2 for password hashing
- Implement multi-factor authentication
- Rate limit login attempts
- Use secure session management

## Authorization
- Implement role-based access control (RBAC)
- Validate permissions server-side
- Use principle of least privilege
- Audit access patterns

## Data Protection
- Encrypt data at rest (AES-256)
- Use TLS 1.3 for data in transit
- Sanitize all user input
- Implement Content Security Policy (CSP)

## Dependency Management
- Scan dependencies for vulnerabilities (Snyk, Dependabot)
- Pin dependency versions
- Review transitive dependencies
- Keep dependencies up to date

## Secrets Management
- Never hardcode secrets in source code
- Use secret managers (Vault, AWS Secrets Manager)
- Rotate secrets regularly
- Use environment variables as a minimum
