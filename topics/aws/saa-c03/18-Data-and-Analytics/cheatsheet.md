# Cheatsheet — Module 12: Data and Analytics

## Quick Comparison of Analytics Services

| Service | Type | Model | Best For |
|---|---|---|---|
| **Athena** | Interactive query | Serverless, pay-per-TB | SQL ad-hoc on S3 |
| **Glue** | ETL | Serverless | ETL transformations, Catalog |
| **EMR** | Big Data Cluster | Managed EC2 | Custom Spark/Hive/Presto |
| **Redshift** | Data Warehouse | Cluster or Serverless | OLAP, BI, analytical SQL |
| **OpenSearch** | Search/Analytics | Cluster | Full-text search, logs, dashboards |
| **MSK** | Managed Kafka | Cluster | Native Kafka streaming |
| **Kinesis Data Streams** | Streaming | Shards | Customizable real-time streaming |
| **Kinesis Firehose** | Delivery streaming | Serverless | Automatic delivery to S3/Redshift |
| **QuickSight** | BI/Visualization | SaaS | Dashboards, SPICE |

---

## Athena — Cost and Performance Optimizations

| Technique | Impact | Implementation |
|---|---|---|
| **Columnar format** (Parquet/ORC) | Reduces up to 90% data scanned | Convert CSV → Parquet with Glue |
| **Compression** (Snappy, GZIP) | Reduces file size | Configure in ETL job |
| **Partitioning** | Scans only relevant partitions | `year=2024/month=01/day=15/` |
| **Bucketing** | Reduces data shuffle on join | `CLUSTERED BY (user_id) INTO 64 BUCKETS` |
| **CTAS** (Create Table As Select) | Transforms in-place to Parquet | `CREATE TABLE ... WITH (format='PARQUET')` |

**Price:** $5.00 per TB scanned. Free: DDL queries, failed queries, queries with partitions (except scanned data).

---

## Kinesis Data Streams vs Kinesis Firehose

| Characteristic | KDS | KDF |
|---|---|---|
| Latency | Milliseconds (real-time) | Near real-time (60s-900s buffer) |
| Consumers | Custom (Lambda, App, KDA) | Automatic (S3, Redshift, OpenSearch) |
| Data retention | 1-365 days | None (delivers and discards) |
| Reprocessing | Yes (multiple consumer cursors) | No |
| Throughput | 1 MB/s per shard (write), 2 MB/s (read) | Automatic |
| Code needed | Yes (consumer code) | No (configuration) |
| Transformation | Not native | Optional Lambda |

---

## Glue — Components

| Component | Function |
|---|---|
| **Data Catalog** | Central repository of schemas/metadata |
| **Crawler** | Discovers schemas and populates the Catalog automatically |
| **ETL Job** | Spark code (Python/Scala) for transformation |
| **DataBrew** | Visual transformation interface without code |
| **Studio** | Visual IDE for Glue jobs |
| **Workflow** | Orchestration of crawlers + jobs + events |
| **Streaming ETL** | Continuous ETL from Kinesis/Kafka |

---

## Redshift — Distribution and Sort Keys

| Type | When to Use |
|---|---|
| DISTKEY: join field | Co-locates related rows on the same nodes |
| DISTKEY: ALL | Replicates the entire table on each node (small dimension tables) |
| DISTKEY: EVEN | Round-robin distribution (no frequent join) |
| SORTKEY: filter/range field | Physically organizes rows — more efficient range scan |

---

## Redshift Serverless vs Provisioned

| | Serverless | Provisioned |
|---|---|---|
| **Management** | Zero | Manage cluster, resize |
| **Scalability** | Automatic | Manual or Elastic Resize |
| **Cost** | RPU-hours (pay-per-use) | Node hour (regardless of usage) |
| **Best for** | Intermittent, dev/test | Predictable and continuous workloads |
| **Concurrency Scaling** | N/A | Automatic transient clusters |

---

## EMR — Node Types and Recommended Instances

| Node | Function | Recommended Instance | Spot OK? |
|---|---|---|---|
| **Master** | Coordinates cluster (YARN RM, HDFS NN) | On-Demand or Reserved | No (SPOF) |
| **Core** | Processes + stores HDFS | On-Demand or Reserved | No (lose HDFS data) |
| **Task** | Only processes (no HDFS) | **Spot** (ideal) | **Yes** — can be interrupted without data loss |

---

## Lake Formation — Access Controls

| Level | Example |
|---|---|
| **Database** | List/describe tables |
| **Table** | Select from all columns |
| **Column** | Select only from authorized columns |
| **Row** | Row-level filters |
| **Cell** | Combination of column + row |

Fine-Grained Access Control (FGAC) replaces S3 bucket policy management for data lakes.

---

## Exam Tips — Common Patterns

| Clue in the Question | Likely Answer |
|---|---|
| "SQL ad-hoc on S3" | Athena |
| "Reduce Athena cost" | Parquet + Partitioning |
| "Visual ETL without code" | AWS Glue DataBrew |
| "Automatic schema discovery" | Glue Crawler → Glue Data Catalog |
| "Migrate Kafka to AWS" | Amazon MSK |
| "Automatic stream delivery to S3" | Kinesis Data Firehose |
| "Real-time with custom consumer" | Kinesis Data Streams |
| "Self-service BI for non-technical users" | QuickSight (SPICE) |
| "Full-text search + Kibana dashboards" | OpenSearch Service |
| "Historical data in S3 + SQL query" | Redshift Spectrum or Athena |
| "Column-level granular security in data lake" | Lake Formation FGAC |
| "Stream processing with Apache Flink" | MSF (Managed Apache Flink) |
| "Oracle → Aurora heterogeneously" | SCT (schema) + DMS (data) |

---
