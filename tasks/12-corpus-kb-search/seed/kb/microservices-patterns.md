# Microservices Design Patterns

## Overview
This article covers essential design patterns for microservices architecture.

## Circuit Breaker Pattern
The circuit breaker pattern prevents cascading failures in distributed systems. When a service becomes unresponsive, the circuit breaker trips and returns a fallback response instead of waiting for timeout. Libraries like Hystrix and Resilience4j implement this pattern.

## Service Discovery
Services register themselves with a registry (e.g., Consul, Eureka) and discover other services dynamically. This eliminates hardcoded endpoints and supports horizontal scaling.

## API Gateway
An API gateway acts as a single entry point for all client requests. It handles routing, authentication, rate limiting, and response aggregation.

## Saga Pattern
For distributed transactions, the saga pattern coordinates local transactions across services. Each service executes its transaction and publishes events for the next step.

## Bulkhead Pattern
The bulkhead pattern isolates different service calls into separate thread pools, preventing one slow service from consuming all resources.
