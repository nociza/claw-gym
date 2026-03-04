# Resilience Patterns for Distributed Systems

## Circuit Breaker
The circuit breaker pattern monitors for failures and prevents calls to a failing service. States:
- **Closed**: Normal operation, calls pass through
- **Open**: Failures exceeded threshold, return fallback
- **Half-Open**: Allow limited calls to test recovery

Implementation: Use Resilience4j (Java), Polly (.NET), or custom middleware.

## Retry with Backoff
Retry failed operations with exponential backoff and jitter:
- First retry: 100ms + random(0-50ms)
- Second retry: 200ms + random(0-100ms)
- Third retry: 400ms + random(0-200ms)
- Maximum: 5 retries

## Timeout
Set appropriate timeouts for all external calls. Use separate timeouts for connection and read operations.

## Bulkhead
Isolate resources to prevent cascade failures. Implement via:
- Thread pool isolation
- Semaphore isolation
- Separate connection pools per dependency

## Fallback
Provide degraded functionality when a dependency fails:
- Return cached data
- Use default values
- Switch to alternative service

## Health Checks
Implement deep health checks that verify:
- Database connectivity
- External service availability
- Disk space and memory
- Message queue connectivity
