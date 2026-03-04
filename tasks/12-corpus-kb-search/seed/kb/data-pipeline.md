# Data Pipeline Architecture

## ETL vs ELT
- **ETL**: Extract, Transform, Load - transform before loading to warehouse
- **ELT**: Extract, Load, Transform - load raw data, transform in warehouse
- Modern trend favors ELT with powerful warehouses (BigQuery, Snowflake)

## Batch Processing
- Use Apache Spark for large-scale batch processing
- Schedule with Airflow or Dagster
- Design for idempotency and retry

## Stream Processing
- Apache Kafka Streams for event processing
- Apache Flink for complex event processing
- Use windowing for time-based aggregations

## Data Quality
- Validate schema at ingestion
- Implement data quality checks at each stage
- Use Great Expectations or dbt tests
- Monitor for data drift

## Data Catalog
Maintain a data catalog for discoverability:
- Document data sources, schemas, owners
- Track data lineage
- Enable self-service analytics

## Performance Tips
- Partition data by date for time-series workloads
- Use columnar formats (Parquet, ORC) for analytics
- Compress data at rest
- Optimize serialization (Avro, Protocol Buffers)
