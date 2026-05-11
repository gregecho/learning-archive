# Questions — Module 12: Data and Analytics

> **SAA-C03 Domain**: Design High-Performance Architectures
> **Difficulty**: Medium

---

**1.** A company has raw data in S3 in JSON format (10 TB). Analysts run frequent queries on only 3 of the 50 available columns. Which change would have the biggest impact on Athena query cost and performance?

- A) Move the data to Redshift
- B) Convert JSON files to Parquet format and partition by date
- C) Use S3 Intelligent-Tiering to reduce storage cost
- D) Enable S3 Transfer Acceleration

<details><summary>Answer</summary>

**B** — Parquet is columnar: Athena reads only the 3 needed columns (vs all 50 in JSON). Partitioning avoids full table scans. Combined: 80-95% reduction in cost and query time. Lower cost per TB scanned + much faster queries.

</details>

---

**2.** A Data Science team needs to perform ETL on 100 GB of daily data in S3, transforming JSONs into Parquet and applying data cleaning. Which AWS service is most suitable for this without managing servers?

- A) AWS Glue (serverless ETL jobs with managed Spark)
- B) Amazon EMR with a permanent cluster
- C) Lambda for file-by-file processing
- D) AWS Batch with containers

<details><summary>Answer</summary>

**A** — Glue ETL jobs: serverless Spark, auto-scales, pays per DPU-hour only while the job runs. EMR requires cluster management. Lambda has a 15-minute limit and 10 GB memory (insufficient for 100 GB of data). Glue is the standard for serverless ETL on AWS.

</details>

---

**3.** An analytics team wants to create a centralized catalog of datasets stored in S3, making them queryable via Athena without manually configuring each table. Which service solves this automatically?

- A) Amazon Macie
- B) AWS Glue Crawlers + Glue Data Catalog
- C) AWS Lake Formation
- D) Amazon OpenSearch

<details><summary>Answer</summary>

**B** — Glue Crawlers: scan S3, automatically infer schemas, and create/update tables in the Glue Data Catalog. Athena uses the Glue Data Catalog as its metastore. Within minutes, all S3 datasets become queryable via Athena.

</details>

---

**4.** A company operates an on-premises Kafka cluster and wants to migrate to AWS without rewriting producers and consumers. Which AWS service should be used?

- A) Amazon Kinesis Data Streams
- B) Amazon SQS FIFO
- C) Amazon MSK (Managed Streaming for Apache Kafka)
- D) Amazon EventBridge

<details><summary>Answer</summary>

**C** — MSK is managed Kafka: compatible with native Kafka APIs. Existing producers and consumers continue to work without modification. Kinesis has its own APIs (incompatible with Kafka).

</details>

---

**5.** A company has a Redshift cluster and analyst queries are degrading the performance of other users. Which Redshift feature solves this with minimal configuration?

- A) Increase cluster size to ra3.16xlarge
- B) Enable Concurrency Scaling to automatically add capacity during query peaks
- C) Migrate to Redshift Serverless
- D) Create Redshift read replicas

<details><summary>Answer</summary>

**B** — Concurrency Scaling: when multiple users submit simultaneous queries and the queue grows, Redshift automatically provisions additional clusters to process extra queries. The first 60 minutes per day of scaling are free. There are no read replicas in Redshift (unlike RDS).

</details>

---

**6.** An architect needs to create a pipeline that delivers clickstream events from a web app to S3 in Parquet format for later analysis with Athena. What is the simplest architecture?

- A) Kinesis Data Streams → Lambda → S3 (converting to Parquet in Lambda)
- B) Kinesis Data Firehose with format transformation to Parquet (via Glue Data Catalog) → S3
- C) API Gateway → Lambda → Glue Job → S3
- D) MSK → Glue Streaming → S3

<details><summary>Answer</summary>

**B** — Kinesis Firehose supports native format conversion to Parquet/ORC using the Glue Data Catalog (defines the schema). Code-free configuration, auto-scales, automatic compression, and delivery to S3 with buffering. Simplest and most managed solution.

</details>

---

**7.** A company needs business analysts to build interactive dashboards on S3 data without moving data to another system. What is the best solution?

- A) Redshift + QuickSight
- B) Athena + QuickSight (with SPICE for interactive dashboards)
- C) OpenSearch + Kibana
- D) EMR + Jupyter Notebooks

<details><summary>Answer</summary>

**B** — Athena queries S3 directly (without moving data); QuickSight connects to Athena and can import results into SPICE (in-memory cache) for ultra-fast dashboards. No infrastructure to manage. Redshift (A) would require moving the data.

</details>

---

**8.** A company has a self-managed Elasticsearch cluster running on EC2 for log analytics. They want to migrate to a managed service while keeping the existing APIs and Kibana dashboards. Which service should they use?

- A) Amazon Kinesis Data Analytics
- B) Amazon OpenSearch Service (with support for OpenSearch Dashboards/Kibana)
- C) Amazon Athena
- D) AWS Glue

<details><summary>Answer</summary>

**B** — Amazon OpenSearch Service is the managed successor to the Elasticsearch Service. Compatible with Elasticsearch APIs and Kibana (via OpenSearch Dashboards). Migration from self-managed Elasticsearch clusters to OpenSearch Service is supported.

</details>

---

**9.** A data team needs to control which users can access which tables and columns in the data lake (S3 + Glue Catalog). Which service implements column-level permissions?

- A) S3 Bucket Policies
- B) Glue Data Catalog with IAM policies
- C) AWS Lake Formation with column-level security
- D) Amazon Macie

<details><summary>Answer</summary>

**C** — Lake Formation: manages data lake permissions with database/table/column/row (Cell-Level Security) granularity. Integrates with Athena, Redshift Spectrum, and EMR. S3 Bucket Policies and IAM policies do not operate at the column level of a table.

</details>

---

**10.** A company stores historical data in S3 but needs to run ad-hoc SQL queries on that data combined with "hot" data in a Redshift cluster. Which Redshift feature should be used?

- A) Redshift Data Sharing
- B) Redshift Spectrum to query S3 data as external tables
- C) Migrate all historical data to Redshift
- D) Use Athena for all data and abandon Redshift

<details><summary>Answer</summary>

**B** — Redshift Spectrum: creates external tables in Redshift pointing to S3 data (via Glue Catalog). Queries referencing external tables are distributed across thousands of Spectrum nodes on S3 — without moving data. Combines hot data (Redshift) and cold data (S3) in a single SQL.

</details>

---

**11.** An ML team needs to store computed features for use in both training (batch) and real-time inference (online) without inconsistencies. Which AWS service offers this?

- A) S3 to store feature CSVs
- B) SageMaker Feature Store with offline store (S3) and online store (low latency)
- C) DynamoDB for online features and S3 for offline features separately
- D) ElastiCache Redis for all features

<details><summary>Answer</summary>

**B** — SageMaker Feature Store: maintains offline store (S3, for training) and online store (low latency, for real-time inference) in sync. Ensures consistency: the same feature definition is used in training and production, avoiding training/serving skew.

</details>

---

**12.** A company processes large volumes of data with Apache Spark on EMR. To reduce costs, they want to use Spot Instances for processing nodes. Which type of node should use Spot?

- A) Master node
- B) Core nodes
- C) Task nodes
- D) B and C

<details><summary>Answer</summary>

**C** — Task nodes are ideal for Spot: they process data but do not store HDFS data. If interrupted, the job can redistribute the work. Core nodes store HDFS data — if lost (Spot interruption), data is lost. Master node = never Spot (coordinates the entire cluster).

</details>

---

**13.** A company wants to query data from a DynamoDB table and an S3 bucket in a single SQL query using Athena. Which feature should be used?

- A) DynamoDB Streams exported to S3 before queries
- B) Athena Federated Query with Lambda Data Source Connector for DynamoDB
- C) Glue ETL to move DynamoDB data to S3 before queries
- D) AWS Glue DataBrew to unify the sources

<details><summary>Answer</summary>

**B** — Athena Federated Query: uses Lambda connectors to query non-S3 sources (DynamoDB, RDS, Redshift, CloudWatch, etc.) directly in SQL. The DynamoDB connector translates Athena queries to DynamoDB API. Queries across S3 and DynamoDB in a single SQL.

</details>

---

**14.** The analytics team needs to detect anomalies in sales metrics in real time (e.g., sudden drop in conversion). Which combination of services implements this?

- A) Kinesis Data Streams → Kinesis Data Analytics (Apache Flink) → SNS for alerts
- B) S3 + Athena with scheduled Lambda queries → SNS
- C) CloudWatch Metrics with Anomaly Detection → CloudWatch Alarm → SNS
- D) A and C are valid depending on the data source

<details><summary>Answer</summary>

**D** — Kinesis Analytics (A): for data already in streaming (clickstream, apps). CloudWatch Anomaly Detection (C): for application and infrastructure metrics. The choice depends on the source: if sales data comes from a stream, use Kinesis Analytics. If they are system metrics, use CloudWatch.

</details>

---

**15.** A company needs to migrate its on-premises Oracle data warehouse to Amazon Redshift. The Oracle schema uses stored procedures and has a different table structure than Redshift. What is the correct process?

- A) DMS directly from Oracle to Redshift (natively supported)
- B) SCT (Schema Conversion Tool) to convert schema + procedures, then DMS to migrate data
- C) Export CSV from Oracle → S3 → Redshift COPY command
- D) EMR to transform data before loading into Redshift

<details><summary>Answer</summary>

**B** — Heterogeneous migration Oracle → Redshift: SCT first to convert DDL, stored procedures, and proprietary Oracle code to Redshift-compatible SQL (also identifies what cannot be automatically converted). Then DMS to move the data (with support for full load and CDC for zero-downtime).

</details>

---
