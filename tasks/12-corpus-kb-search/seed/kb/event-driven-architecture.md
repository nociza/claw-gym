# Event-Driven Architecture

## Overview
Event-driven architecture (EDA) uses events to trigger and communicate between decoupled services.

## Event Types
- **Domain events**: Business-meaningful occurrences (OrderPlaced, UserRegistered)
- **Integration events**: Cross-service communication
- **Notification events**: Inform subscribers of state changes

## Message Brokers
- **Apache Kafka**: High-throughput, durable, ordered event streaming
- **RabbitMQ**: Traditional message queue, flexible routing
- **AWS SQS/SNS**: Managed message queue and pub/sub

## Patterns
### Event Sourcing
Store state changes as a sequence of events. Rebuild current state by replaying events. Provides complete audit trail.

### CQRS
Command Query Responsibility Segregation: separate read and write models. Often combined with event sourcing.

### Choreography vs Orchestration
- Choreography: Services react to events independently
- Orchestration: Central coordinator directs the workflow

## Idempotency
Design event handlers to be idempotent. Duplicate events should produce the same result as processing once.

## Considerations
- Event ordering guarantees vary by broker
- Schema evolution requires careful versioning
- Eventual consistency is inherent in EDA
