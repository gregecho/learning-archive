# Exam Questions — Module 06: Databases

<!-- SAA-C03 Domain: Design Resilient Architectures / High-Performing Architectures -->

---

**1.** An e-commerce web application needs a relational database with automatic failover within the same region without data loss. Which RDS configuration should be used?

- A) RDS with Read Replica in another AZ
- B) RDS Multi-AZ Deployment
- C) RDS with automated backup enabled
- D) Aurora with Multi-Master

<details>
<summary>Answer</summary>
**B — RDS Multi-AZ Deployment**
Multi-AZ maintains a **synchronous** standby replica in another AZ with automatic failover (1-2 minutes). Read Replicas are **asynchronous** and serve reads, not automatic failover without intervention. Automated backup does not provide failover.
</details>

---

**2.** What is the critical difference between Multi-AZ and Read Replicas in RDS?

- A) Multi-AZ uses synchronous replication; Read Replicas use asynchronous replication
- B) Multi-AZ is for reads and writes; Read Replicas are only for writes
- C) Read Replicas guarantee zero RPO; Multi-AZ has RPO of minutes
- D) Multi-AZ can be cross-region; Read Replicas are only in the same AZ

<details>
<summary>Answer</summary>
**A — Correct**
Multi-AZ: synchronous → zero RPO, automatic failover, standby does not receive read traffic. Read Replicas: asynchronous → may have lag (small RPO), for read offloading, can be promoted to standalone DB. Read Replicas can be cross-region! Multi-AZ is only within the same region.
</details>

---

**3.** A startup uses RDS MySQL with Aurora and notices a latency spike when Lambda functions scale from 0 to 1,000 concurrent instances, exhausting RDS connections. What is the solution?

- A) Increase max_connections in the parameter group
- B) Use RDS Proxy between Lambda functions and the database
- C) Vertically scale to db.r6g.16xlarge
- D) Enable Enhanced Monitoring on RDS

<details>
<summary>Answer</summary>
**B — RDS Proxy**
RDS Proxy manages a connection pool between the application (Lambda, ECS, etc.) and RDS/Aurora, reusing connections and preventing each Lambda from opening its own connection. It is the architectural solution for "connection exhaustion" with Lambda. Increasing max_connections is a workaround with limits.
</details>

---

**4.** Regarding Amazon Aurora, which statement is CORRECT?

- A) Aurora stores 2 copies of data across 2 AZs (2 total copies)
- B) Write quorum requires 4 of 6 copies; read quorum requires 3 of 6
- C) Aurora Failover to Read Replica takes ~30 minutes
- D) Aurora Serverless v2 does not support automatic capacity scaling

<details>
<summary>Answer</summary>
**B — Correct**
Aurora maintains **6 copies across 3 AZs** (2 per AZ). Write quorum: 4/6 copies confirmed. Read quorum: 3/6. Failover to Aurora Read Replica is automatic and takes ~30 seconds (not 30 minutes). Aurora Serverless v2 scales from 0.5 to 128 ACUs automatically.
</details>

---

**5.** A company needs a NoSQL database that responds in microseconds for a product catalog with millions of items. Which solution?

- A) DynamoDB with DAX
- B) ElastiCache Redis with RDS PostgreSQL
- C) Aurora with Read Replicas
- D) DynamoDB with Strong Consistency enabled

<details>
<summary>Answer</summary>
**A — DynamoDB with DAX**
DynamoDB has millisecond latency. DAX (DynamoDB Accelerator) is a managed in-memory cache that reduces latency to **microseconds**. ElastiCache with RDS adds operational complexity. Strong Consistency on DynamoDB increases latency (does not reduce it).
</details>

---

**6.** Which DynamoDB capacity mode charges only for what is actually consumed without capacity planning?

- A) Provisioned Capacity Mode with Auto Scaling
- B) On-Demand Capacity Mode
- C) Reserved Capacity
- D) Provisioned with burst capacity

<details>
<summary>Answer</summary>
**B — On-Demand Capacity Mode**
On-Demand charges for each read/write request actually made. Ideal for unpredictable workloads, new workloads, or sporadic use. Costs more per request than Provisioned, but zero planning. Provisioned + Auto Scaling still requires min/max configuration; may have throttling if scaling cannot keep up with sudden spikes.
</details>

---

**7.** A web application needs user sessions stored in cache with a 30-minute TTL, shared across multiple EC2 instances. Which service?

- A) DynamoDB with TTL
- B) ElastiCache Redis
- C) ElastiCache Memcached
- D) RDS with index on session_id

<details>
<summary>Answer</summary>
**B — ElastiCache Redis**
Redis supports rich data structures, persistence, replication, Multi-AZ, and Pub/Sub. For user sessions with TTL, Redis is ideal. Memcached is simpler, with no persistence, no replication. DynamoDB works but has millisecond latency vs microsecond Redis latency and is not strictly "in-memory".
</details>

---

**8.** A company needs to run analytical SQL queries over 100 TB of historical sales data with performance in minutes, not hours. Which AWS database to use?

- A) RDS PostgreSQL with indexes
- B) Aurora Serverless v2
- C) Amazon Redshift
- D) DynamoDB with GSI

<details>
<summary>Answer</summary>
**C — Amazon Redshift**
Redshift is OLAP (Online Analytical Processing) with MPP (Massively Parallel Processing) architecture for analytical queries over petabytes of data. RDS/Aurora are OLTP (transactions). DynamoDB + GSI is NoSQL, not suitable for ad-hoc analytical SQL on 100 TB.
</details>

---

**9.** What is the difference between LSI and GSI in DynamoDB?

- A) LSI can have a different partition key; GSI keeps the same partition key
- B) LSI must be created at table creation; GSI can be created at any time
- C) GSI uses separate RCU/WCU; LSI shares the base table's RCU/WCU
- D) B and C are correct

<details>
<summary>Answer</summary>
**D — B and C are correct**
LSI: created **only at table creation** (not possible afterwards); same partition key, different sort key; shares the table's throughput. GSI: created at any time after creation; distinct partition key and sort key; has its own throughput (independent WCU/RCU). Both allow queries on non-key attributes.
</details>

---

**10.** A company wants to use Aurora and guarantee RPO close to zero in case of total failure of an AWS Region. Which feature?

- A) Aurora Multi-AZ with 6 copies
- B) Aurora Global Database
- C) Aurora with CRR (Cross-Region Read Replica)
- D) RDS Multi-Region

<details>
<summary>Answer</summary>
**B — Aurora Global Database**
Aurora Global Database replicates with < 1 second lag to up to 5 secondary regions. In case of primary region failure, can promote a secondary region in < 1 minute (RTO < 1min, RPO < 1 second). Regular RDS/Aurora CRR has higher lag and slower manual failover.
</details>

---

**11.** A legacy Java application uses JDBC to connect to an on-premises Oracle database. The company wants to migrate to AWS without rewriting the application. Which database to choose?

- A) DynamoDB (NoSQL as a substitute)
- B) RDS for Oracle
- C) Aurora PostgreSQL with schema conversion
- D) Amazon Keyspaces

<details>
<summary>Answer</summary>
**B — RDS for Oracle**
For lift-and-shift migration of Oracle without rewriting, RDS for Oracle maintains full Oracle compatibility. Aurora PostgreSQL + AWS SCT (Schema Conversion Tool) is an option for heterogeneous migration but requires conversion effort. DynamoDB and Keyspaces are NoSQL — not compatible with Oracle JDBC without rewriting.
</details>

---

**12.** A Redshift analysis needs to cross data warehouse data with fresh data in S3, without loading it into the DW. Which feature to use?

- A) Redshift COPY command
- B) Redshift Spectrum
- C) AWS Glue ETL
- D) Amazon Athena

<details>
<summary>Answer</summary>
**B — Redshift Spectrum**
Redshift Spectrum allows running SQL queries directly on S3 data (Parquet, CSV, JSON, etc.) as if they were external Redshift tables, without loading the data. Athena also queries S3 but is independent of Redshift — Spectrum unites both worlds in a single query.
</details>

---

**13.** Which AWS database is most suitable for graph data such as social networks (friendships, connections)?

- A) DynamoDB with adjacency list pattern
- B) Amazon Neptune
- C) Amazon DocumentDB
- D) Amazon QLDB

<details>
<summary>Answer</summary>
**B — Amazon Neptune**
Neptune is a managed graph database, with support for Property Graph (Gremlin, openCypher) and RDF (SPARQL). Ideal for social networks, knowledge graphs, fraud detection, recommendations. DocumentDB is a document store (MongoDB-compatible). QLDB is an immutable ledger. DynamoDB adjacency list works but is suboptimal for complex traversals.
</details>

---

**14.** An application stores user sessions in DynamoDB. Sessions expire after 24 hours and need to be automatically removed. Which feature to use?

- A) Lambda with CloudWatch Events removing items daily
- B) DynamoDB Streams with cleanup Lambda
- C) TTL (Time To Live) in DynamoDB
- D) S3 Lifecycle Policy integrated with DynamoDB

<details>
<summary>Answer</summary>
**C — TTL (Time To Live)**
DynamoDB TTL allows associating a timestamp attribute with an item; when the timestamp expires, DynamoDB automatically removes the item at no WCU cost. Removal occurs within a 48h window after expiration (not immediate, but efficient and free). Lambda + CloudWatch is overengineering.
</details>

---

**15.** What is the typical RTO of an RDS Multi-AZ failover?

- A) Instant (0 seconds) — automatically redirects DNS
- B) 1 to 2 minutes — flips DNS to standby
- C) 5 to 10 minutes — standby needs to re-sync logs
- D) 15 to 30 minutes — new DB instance is provisioned

<details>
<summary>Answer</summary>
**B — 1 to 2 minutes**
RDS Multi-AZ failover flips the DNS CNAME to point to the standby in ~60-120 seconds. The application reconnects to the same DNS endpoint. Standby is already synchronized (synchronous), so there is no re-synchronization. Zero data loss with RPO approximately equal to 0. Applications should use JDBC connection retry to absorb the brief downtime.
</details>
