# Observability Guide

## Three Pillars
1. **Logs**: Structured event records
2. **Metrics**: Numeric measurements over time
3. **Traces**: Request flow across services

## Structured Logging
Use JSON format for logs. Include correlation IDs to trace requests across services.

## Metrics Collection
Key application metrics:
- Request rate (RED method: Rate, Errors, Duration)
- Resource utilization (USE method: Utilization, Saturation, Errors)
- Business metrics (signups, purchases, etc.)

## Distributed Tracing
OpenTelemetry is the recommended standard. Instrument your services to propagate trace context across HTTP calls and message queues.

## Alerting Strategy
- Alert on symptoms, not causes
- Use circuit breaker pattern in your alerting to prevent alert storms
- Set appropriate severity levels
- Include runbooks with every alert

## Dashboards
Create dashboards at three levels:
1. Business: KPIs, revenue, user activity
2. Service: Latency, error rates, throughput per service
3. Infrastructure: CPU, memory, disk, network
