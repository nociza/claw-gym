# Database Optimization Techniques

## Query Optimization
- Use EXPLAIN ANALYZE to understand query plans
- Add indexes for frequently queried columns
- Avoid SELECT * in production queries
- Use parameterized queries to benefit from query plan caching

## Indexing Strategy
- B-tree indexes for equality and range queries
- GIN indexes for full-text search and JSONB in PostgreSQL
- Partial indexes for filtered queries
- Composite indexes for multi-column queries (order matters!)

## Connection Pooling
Use connection poolers like PgBouncer or HikariCP. Configure pool size based on: connections = (core_count * 2) + effective_spindle_count.

## Read Replicas
Offload read traffic to replicas. Be aware of replication lag affecting consistency. The CAP theorem applies here - you trade consistency for availability.

## Partitioning
- Range partitioning for time-series data
- List partitioning for categorical data
- Hash partitioning for even distribution

## Monitoring
Track these metrics:
- Query response time (p95, p99)
- Connection pool utilization
- Replication lag
- Table bloat and vacuum statistics
