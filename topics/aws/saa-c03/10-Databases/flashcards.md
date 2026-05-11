# Flashcards — Module 06: Databases

---

**Q:** What is the replication difference between RDS Multi-AZ and Read Replica?
**A:** Multi-AZ: **synchronous** replication → zero RPO, automatic failover (~1-2 min). Read Replica: **asynchronous** replication → small lag, for read offloading, manual failover (promote to standalone DB)

---

**Q:** How many copies does Aurora data maintain and how?
**A:** 6 copies across 3 AZs (2 per AZ). Write quorum: 4/6. Read quorum: 3/6. Supports loss of 1 AZ without read impact; loss of 2 AZs without write impact

---

**Q:** What is the RTO/RPO of Aurora Global Database in case of regional failure?
**A:** RPO < 1 second (replication with ~1s lag). RTO < 1 minute (promote secondary region manually or automatically via managed failover)

---

**Q:** What is RDS Proxy and when to use it?
**A:** Managed proxy that provides connection pooling between applications and RDS/Aurora. Reuses connections, avoids connection exhaustion. Critical for Lambda (stateless, opens new connection on each invoke) and ECS (many tasks)

---

**Q:** How far back does RDS PITR (Point-In-Time Recovery) allow restore?
**A:** Up to the last 35 days (configurable from 1 to 35 days). Restore to any second within that window using backups + transaction logs

---

**Q:** What are the 2 DynamoDB capacity modes and when to use each?
**A:** Provisioned: you set RCUs and WCUs + Auto Scaling. Use for predictable/consistent workloads (cheaper). On-Demand: charged per request. Use for unpredictable workloads, new workloads, sudden spikes

---

**Q:** What is 1 RCU and 1 WCU in DynamoDB?
**A:** 1 RCU = 1 strongly consistent read of up to 4 KB (or 2 eventually consistent reads). 1 WCU = 1 write of up to 1 KB per second

---

**Q:** What is the latency of DAX vs direct DynamoDB?
**A:** DynamoDB: milliseconds latency. DAX (DynamoDB Accelerator): **microseconds** (managed in-memory cache, compatible with DynamoDB API)

---

**Q:** What is the difference between LSI and GSI in DynamoDB?
**A:** LSI: same partition key, different sort key, created ONLY at table creation, uses table throughput. GSI: different partition key, created at any time, independent throughput

---

**Q:** How long does DynamoDB Streams retain data?
**A:** 24 hours. Streams capture item-level changes (INSERT, MODIFY, REMOVE) with before and/or after image. Integrates with Lambda (trigger) and DynamoDB Global Tables (multi-region replication)

---

**Q:** What is the "Lazy Loading" read pattern in ElastiCache?
**A:** Cache Miss: fetch from database → write to cache. Cache Hit: return from cache. Pros: only stores requested data. Cons: cache miss = 3 trips (cache, DB, cache) + risk of stale data

---

**Q:** What is the main difference between Redis and Memcached in ElastiCache?
**A:** Redis: persistence, replication, Multi-AZ, Pub/Sub, Sorted Sets, Geospatial, Cluster Mode (sharding). Memcached: multi-threading, no persistence, no replication, simple, pure cache. For HA and complex data structures: Redis

---

**Q:** What is Redshift Enhanced VPC Routing?
**A:** Forces Redshift COPY and UNLOAD traffic to use the VPC (instead of public internet/public S3 endpoints). Allows control via VPC Flow Logs, SG, NACLs. Recommended for security and compliance

---

**Q:** When to use Amazon Neptune?
**A:** For graph data and queries: social networks (friendships), fraud detection (suspicious connections), knowledge graphs, recommendation engines. Supports Property Graph (Gremlin, openCypher) and RDF (SPARQL)

---

**Q:** When to use Amazon QLDB?
**A:** Ledger database with immutable and cryptographically verifiable history. For: financial records, supply chain tracking, audit logs where no data can be deleted or retroactively modified

---

**Q:** For which workload is Aurora Serverless v2 ideal?
**A:** Workloads with highly variable traffic (e.g., dev/test, applications with nightly or seasonal peaks). Scales from 0.5 to 128 ACUs in 0.5 ACU increments in ~1 second. Zero downtime during scaling

---

**Q:** What are the read endpoint and write endpoint of an Aurora Cluster?
**A:** Cluster Endpoint (write): points to the primary writer instance. Reader Endpoint: load balancer across all Read Replicas. Applications should use the correct endpoint to separate reads from writes

---

**Q:** What is ElastiCache Cluster Mode (sharding in Redis)?
**A:** Distributes key slots (keyspace partitions) across multiple node groups (shards). Enables higher total throughput (parallel writes across shards) and greater data capacity than a single node. Each shard has replicas for HA

---

**Q:** What is Amazon Keyspaces?
**A:** Apache Cassandra compatible and fully managed on AWS. For lift-and-shift migration of Cassandra workloads without managing clusters. CQL (Cassandra Query Language) compatible

---

**Q:** What is the use of Amazon Timestream?
**A:** Serverless time series database. For IoT data, DevOps metrics, application performance telemetry. Stores and analyzes trillions of events per day. Queries with built-in temporal analysis functions
