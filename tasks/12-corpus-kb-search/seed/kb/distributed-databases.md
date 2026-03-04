# Distributed Database Guide

## CAP Theorem
The CAP theorem states that a distributed system can provide at most two of three guarantees: Consistency, Availability, and Partition tolerance. Understanding CAP is fundamental to choosing the right database.

- **CP systems**: MongoDB (with majority write concern), HBase
- **AP systems**: Cassandra, DynamoDB, CouchDB
- **CA systems**: Traditional RDBMS (single node, no partition tolerance)

## Consistency Models
- Strong consistency: All reads return the most recent write
- Eventual consistency: Reads may return stale data temporarily
- Causal consistency: Maintains cause-effect ordering

## Replication Strategies
- Synchronous: Guarantees consistency, higher latency
- Asynchronous: Lower latency, risk of data loss
- Semi-synchronous: Compromise approach

## Sharding
Distribute data across nodes using:
- Hash-based sharding
- Range-based sharding
- Geographic sharding

## Recommended Patterns
For most web applications, we recommend starting with PostgreSQL and adding read replicas before moving to a distributed database.
