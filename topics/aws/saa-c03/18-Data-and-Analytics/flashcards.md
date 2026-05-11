# Flashcards — Module 12: Data and Analytics

> **Format:** Q = Question | A = Answer
> **Total:** 25 flashcards

---

**Q:** What is Amazon Athena and what is its pricing model?
**A:** Serverless interactive query service using standard SQL directly on S3 files. Model: **pay-per-query** — $5 per TB of data scanned. Optimizations to reduce cost: use columnar format (Parquet/ORC) and partitioning (scans less data).

---

**Q:** Why does Parquet reduce query costs in Athena?
**A:** Parquet is **columnar**: Athena reads only the columns needed for the query, ignoring the others. It also has native compression (Snappy, Gzip). Result: scans less data → lower costs ($5/TB scanned). CSV is row-based — scans the entire row even if the query only needs 2 columns.

---

**Q:** What is the AWS Glue Data Catalog?
**A:** Central metadata repository (schemas, tables, partitions) for data in S3, RDS, Redshift, etc. Functions as a metastore for Athena and EMR. Glue Crawlers automatically populate the Catalog. Each data source has a "database" with "tables" in the Catalog.

---

**Q:** What is the difference between Glue ETL Jobs and AWS Glue DataBrew?
**A:** **Glue ETL Jobs:** Python/Scala code (Spark) for complex custom transformations. **AWS Glue DataBrew:** visual data preparation interface without code. Over 250 built-in transformations (deduplicate, filter, format). For data analysts without programming skills.

---

**Q:** What are the 3 node types in an Amazon EMR cluster?
**A:** **Master Node:** coordinates the cluster (YARN ResourceManager, HDFS NameNode). **Core Node:** processes tasks + stores HDFS data (YARN NodeManager). **Task Node:** only processes tasks, without HDFS storage — ideal for Spot Instances (losing Task Nodes does not affect data).

---

**Q:** When to use Amazon MSK instead of Amazon Kinesis?
**A:** **MSK:** when you already use Apache Kafka on-premises and want to migrate without changing producers/consumers (fully managed Kafka); when you need native Kafka protocol. **Kinesis:** proprietary AWS service, more integrated; no broker operations; better integration with Lambda, Firehose, etc. MSK = lift-and-shift Kafka; Kinesis = AWS-native.

---

**Q:** What is the difference between Redshift Multi-AZ and Redshift Cross-Region Snapshot?
**A:** **Multi-AZ:** Redshift cluster with replicas in multiple AZs — HA for automatic failover (available on RA3). **Cross-Region Snapshot:** cluster backup copied to another region for DR. Snapshots: automatic (1-35 days). For migration/restore in another region.

---

**Q:** What is Redshift Concurrency Scaling?
**A:** Feature that automatically adds transient clusters when concurrency demand exceeds the main cluster capacity. Queries routed to scaling clusters. Free credits: 1 hour per day of active main cluster. Additional cost beyond credits.

---

**Q:** What is SPICE in Amazon QuickSight?
**A:** Super-fast Parallel In-memory Calculation Engine: in-memory cache of imported data in QuickSight. Dashboards become ultra-fast because they don't need to query the database on every interaction. Quota per user (GB). Scheduled or on-demand refresh to update data.

---

**Q:** What are the use cases for Amazon Kinesis Data Firehose?
**A:** Delivery of streaming data to **destinations**: S3, Redshift (via S3 staging), OpenSearch, Splunk, custom HTTP endpoints. Characteristics: near-real-time (buffering of 60s to 900s or 1-128 MB), optional transformation with Lambda, format conversion (JSON→Parquet), compression. Does not require a consumer — automatic delivery.

---

**Q:** What is AWS Lake Formation and what problem does it solve?
**A:** Simplifies building secure **Data Lakes** on S3. Problem: granular security in data lakes is complex. Solution: Fine-Grained Access Control (FGAC) — control by column, row-level filters, cell-level security. Centralizes permissions instead of individual policies per bucket/folder.

---

**Q:** What is the difference between OpenSearch Service and Amazon Kendra?
**A:** **OpenSearch:** search and analytics engine for logs, metrics, full-text search, visualizations (Kibana/OpenSearch Dashboards). **Kendra:** AI-powered search engine for corporate documents — understands natural language ("what are the vacation policies?"), searches PDFs, Word, SharePoint. OpenSearch = technical/analytics; Kendra = intelligent document search.

---

**Q:** What is Redshift Spectrum?
**A:** Redshift extension that allows querying data directly in **S3** without loading into Redshift. Uses independent scalability nodes (Spectrum layer). Accesses the Glue Data Catalog for metadata. Ideal for: historical/cold data in S3 + hot data in Redshift in a single SQL query.

---

**Q:** How does partitioning work in Athena and why is it important?
**A:** Partitioning: organizing data in S3 into hierarchical folders by high-cardinality field (e.g., `s3://bucket/year=2024/month=01/day=15/`). In the query: `WHERE year=2024 AND month=01` → Athena scans only those partitions. Drastically reduces data scanned → lower cost and better performance.

---

**Q:** What are the differences between Kinesis Data Streams and Kinesis Data Firehose?
**A:** **KDS:** real-time streaming, custom consumers (Lambda, apps, Kinesis Analytics), retention 1-365 days, configurable shards. Requires consumer code. **KDF:** managed delivery to destinations (S3, Redshift, OpenSearch), near-real-time (buffer), no consumer code, automatic compression/transformation. KDS = flexibility; KDF = delivery simplicity.

---

**Q:** What is AWS Glue Streaming ETL?
**A:** Glue extension to process **streaming** data from Kinesis Data Streams, Kafka/MSK, or SQS. Continuously processes micro-batches (streaming ETL). Uses Apache Spark Structured Streaming. Managed alternative to Apache Flink for streaming transformations.

---

**Q:** How does Amazon EMR Serverless work?
**A:** Runs Spark/Hive workloads without managing clusters. Submit a job → AWS automatically provisions the necessary resources → executes → deallocates. No nodes to manage. Pay-per-vCPU-second and GB-second. Ideal for intermittent or unpredictable workloads. No cold start from manual cluster provisioning.

---

**Q:** What are Amazon OpenSearch UltraWarm and Cold Tiers?
**A:** Cost-effective storage tiers for historical data in OpenSearch: **UltraWarm:** less accessed data in S3 (warm tier), cheaper than hot instances, still queryable in seconds. **Cold:** even cheaper, archived data, higher access latency. Migration: indices moved between hot → warm → cold as they age.

---

**Q:** What is AWS Glue Workflow?
**A:** Orchestration of ETL pipelines in Glue. Allows creating execution graphs with triggers, crawlers, and jobs. Trigger types: on-demand, schedule (cron), event-based (completion of another job). Graphical visualization in the console. For complex multi-step ETL pipelines without Step Functions.

---

**Q:** When to use Amazon EMR vs AWS Glue for ETL?
**A:** **Glue:** simple-to-medium ETL, no infrastructure to manage, native integration with Catalog/S3/Redshift, ideal for non-Spark engineers. **EMR:** complex Spark/Hive/Presto workloads, full control over cluster configuration, multiple frameworks (local HDFS), HPC workloads, greater flexibility and performance for big data.

---

**Q:** What is Amazon Kinesis Data Analytics (now Amazon Managed Service for Apache Flink)?
**A:** Managed service for Apache Flink applications — processes streams in real-time with SQL or Java/Python/Scala. Input: KDS or MSK. Output: S3, KDS, KDF, Lambda, etc. Use cases: real-time anomaly detection, windowed aggregations (sliding/tumbling windows), joins of multiple streams.

---

**Q:** What is the billing model for Amazon Athena?
**A:** $5.00 per TB of data **scanned** (not per query time). No charge for failed queries. To reduce cost: (1) Compression — smaller data = fewer TB; (2) Columnar (Parquet/ORC) — scans only necessary columns; (3) Partitioning — scans only relevant partitions.

---

**Q:** What is Amazon QuickSight Q?
**A:** QuickSight's NLP (Natural Language Processing) engine: allows asking questions in natural language about dashboards. Ex: "what was the revenue in January?" → QuickSight interprets and generates visualization automatically. Requires topic training with the data.

---

**Q:** What is DMS (Database Migration Service) and when to use SCT?
**A:** **DMS:** database migration with minimal downtime (ongoing replication CDC). Supports homogeneous and heterogeneous. **SCT (Schema Conversion Tool):** converts schema + code (stored procedures, views) between different engines (Oracle → PostgreSQL, SQL Server → Aurora). DMS = migrates data; SCT = converts incompatible schema. Homogeneous (MySQL→MySQL): DMS without SCT. Heterogeneous: DMS + SCT.

---

**Q:** What is Amazon Redshift Serverless?
**A:** Redshift without needing to provision or manage clusters. AWS automatically provisions and scales capacity based on workload. Pay-per-use (RPU-hours — Redshift Processing Units). Ideal for: intermittent workloads, dev/test environments, sporadic analytics. Vs cluster: no management, but cost may be higher for constant workloads.

---
