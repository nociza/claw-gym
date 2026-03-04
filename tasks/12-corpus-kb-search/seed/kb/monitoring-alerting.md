# Monitoring and Alerting Guide

## Monitoring Stack
Recommended stack:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **AlertManager**: Alert routing and silencing
- **PagerDuty/OpsGenie**: Incident management

## Key Metrics (Four Golden Signals)
1. **Latency**: Time to serve a request
2. **Traffic**: Request rate
3. **Errors**: Error rate
4. **Saturation**: Resource utilization

## Alert Design
- Alert on user-facing symptoms, not internal metrics
- Use multi-window alerting to reduce false positives
- Include runbook links in every alert
- Implement escalation policies

## SLO-Based Monitoring
Define Service Level Objectives:
- Availability: 99.9% uptime
- Latency: p99 < 500ms
- Error rate: < 0.1%
Use error budgets to balance reliability and feature velocity.

## Log Aggregation
Centralize logs with ELK stack (Elasticsearch, Logstash, Kibana) or Loki. Use structured logging (JSON) for searchability.

## Incident Response
1. Detect (automated monitoring)
2. Respond (on-call engineer)
3. Mitigate (restore service)
4. Resolve (fix root cause)
5. Learn (post-mortem)
