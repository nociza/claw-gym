# Testing Strategy Guide

## Test Pyramid
- **Unit tests** (base): Fast, isolated, test individual functions
- **Integration tests** (middle): Test component interactions
- **End-to-end tests** (top): Test complete user workflows

## Unit Testing
- Aim for 80%+ code coverage
- Test edge cases and error paths
- Use mocking for external dependencies
- Keep tests fast (< 1 second each)

## Integration Testing
- Test database interactions with real databases (Testcontainers)
- Test API contracts between services
- Use consumer-driven contract testing (Pact)

## Load Testing
Use k6 for load testing (see load-testing article for details). Establish performance baselines and test against them in CI.

## Property-Based Testing
Use Hypothesis (Python) or fast-check (JavaScript) to generate test cases automatically. Effective for finding edge cases.

## Testing in Production
- Feature flags for gradual rollout
- Synthetic monitoring (scheduled test transactions)
- Chaos engineering (Netflix Simian Army, Gremlin)

## Best Practices
- Write tests before or alongside code (TDD/BDD)
- Keep tests independent and repeatable
- Use descriptive test names
- Clean up test data after each test
