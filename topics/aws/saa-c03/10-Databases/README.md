# Module 06 — Databases

## Objective

In this module, you will choose the correct database service for each scenario, balancing consistency, scale, latency, availability, and cost in typical SAA-C03 decisions.

## Key AWS Services

- Amazon RDS
- Amazon Aurora
- Amazon DynamoDB
- Amazon ElastiCache
- Amazon Redshift

## Architecture and Trade-offs

## Amazon RDS

Managed service for relational databases. Supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora.

### Multi-AZ
- Passive **standby** in another AZ — receives synchronous replication via storage-level replication
- Automatic failover in 1–2 minutes (DNS updates to standby)
- The standby **cannot be read** — it is not a read replica
- Backups are taken from the standby (no impact on primary)
- Multi-AZ is for **availability** (HA), not read scalability

### Read Replicas
- **Asynchronous** replication from primary — may have lag
- Up to 15 read replicas (Aurora), 5 (standard RDS)
- Can be in another region (**Cross-Region Read Replica**)
- Can be promoted to an independent database (breaks replication)
- **Used for:** scaling reads, analytics without primary impact, migration

### Backups and Snapshots
| Type | Retention | When it occurs | Restoration |
|---|---|---|---|
| Automated Backup | 1–35 days | Maintenance window | Point in time (PITR) |
| Manual Snapshot | Indefinite | You trigger | To specific snapshot |

- PITR (Point-in-Time Recovery): restores to any second within the retention period
- Automated Backup enabled by default; default retention = 7 days
- Snapshots copyable across regions for DR

### RDS Proxy
- Connection pool between application and database — reduces open/close overhead
- Ideal for Lambda (functions create/destroy connections quickly)
- Supports faster Multi-AZ failover (fewer connections to renegotiate)
- Must be in the same VPC

---

## Amazon Aurora

Relational database compatible with MySQL/PostgreSQL, performance up to **5x MySQL and 3x PostgreSQL** of equivalent RDS.

### Cluster Architecture
```
Writer Endpoint        Reader Endpoint
      │                      │
      ▼                      ▼
  Primary Instance    ← Replica 1
                      ← Replica 2 (all replicas share the same storage)
                      ← Replica N (up to 15)

Storage Layer (Shared):
  6 data copies → 3 AZs (2 copies per AZ)
  Quorum: 4/6 for writes, 3/6 for reads
  Auto-healing: auto-detects and repairs corrupted bits
  Auto-scaling storage: 10 GB increments, up to 128 TB
```

### Aurora vs RDS Multi-AZ
| Aurora | RDS Multi-AZ |
|---|---|
| Read replicas (up to 15) in the same cluster | Passive standby (not readable) |
| Failover in <30 seconds | Failover in 1–2 minutes |
| Shared storage across instances | Separate storage replication |
| Aurora Serverless v2 available | No serverless |

### Aurora Global Database
- **Cross-region replication** in < 1 second (median)
- Up to 5 secondary regions, each with up to 16 read replicas
- Secondary region promotion to primary in < 1 minute (DR)
- Useful for global read latency and cross-region recovery

### Aurora Serverless v2
- Scales from 0.5 to 128 ACUs (Aurora Capacity Units) in fine 0.5 ACU increments
- Ideal for variable, intermittent, test/dev workloads
- Charged per ACU-hour every second

---

## Amazon DynamoDB

Fully managed NoSQL key-value and document store. Scales horizontally to any throughput.

### Data Model
- **Partition Key** (required): determines physical partition — must have high cardinality
- **Sort Key** (optional): allows multiple items per partition key, enables range queries
- **Items**: up to 400 KB each
- **Attributes**: typed (String, Number, Binary, Boolean, Null, List, Map, Set)

### Secondary Indexes
| Type | Partition Key | Sort Key | Size | Consistency |
|---|---|---|---|---|
| **LSI (Local Secondary Index)** | Same as table | Different | Up to 10 GB per partition key | Eventual or Strong |
| **GSI (Global Secondary Index)** | Different | Any | Unlimited | Eventual only |

- LSI: created only during table creation, cannot be added later
- GSI: can be added at any time, has its own RCU/WCU

### Capacity Modes
| Mode | How you pay | When to use |
|---|---|---|
| **Provisioned** | Pre-defined RCU + WCU | Predictable traffic, lower cost |
| **On-Demand** | Per read/write operation | Unpredictable traffic, pay per use |

- 1 RCU = 1 strongly consistent read of 4 KB / 2 eventually consistent reads of 4 KB
- 1 WCU = 1 write of up to 1 KB

### DAX (DynamoDB Accelerator)
- Fully managed in-memory cache for DynamoDB
- **Microsecond** latency (vs millisecond direct DynamoDB)
- Drop-in replacement for DynamoDB API (same endpoint, no code changes)
- Ideal for read-intensive applications with hot keys

### DynamoDB Streams
- Captures changes (insert, update, delete) in chronological order per item
- Retention: 24 hours
- Use cases: trigger Lambda on changes, custom cross-region replication, auditing, derived computation

### DynamoDB TTL
- Timestamp attribute (Unix epoch) on each item
- DynamoDB auto-deletes expired items (eventually, at no WCU cost)
- Useful for: sessions, shopping carts, temporary tokens, telemetry data

---

## Amazon ElastiCache

Managed in-memory cache. Two engines:

### Redis vs Memcached
| Characteristic | Redis | Memcached |
|---|---|---|
| Data structures | Strings, Lists, Sets, Sorted Sets, Hashes, HLL | Strings only |
| Multi-threading | Single-thread (by default, Redis 6+ has I/O threads) | Multi-thread |
| Persistence | RDB snapshots + AOF | None |
| Replication | Read replicas (cluster mode off/on) | No |
| Automatic failover | Yes (Redis Sentinel/Cluster) | No |
| Pub/Sub | Yes | No |
| Lua scripting | Yes | No |
| **Multi-AZ** | Yes | No |
| Use for | Sessions, leaderboards, pub/sub, light queues, ML features | Simple multi-threaded cache |

### Redis Cluster Mode
- **Cluster Mode Off**: 1 shard, up to 5 read replicas, Multi-AZ possible, simple
- **Cluster Mode On**: up to 500 shards, auto-distributes data (sharding), scales to PiB of data

### Caching Patterns
| Pattern | Description |
|---|---|
| **Lazy Loading** | Cache miss → fetch DB → store in cache. Data may go stale |
| **Write-Through** | Write to cache and DB together. Cache always current, but higher write latency |
| **Cache Aside** | App manages cache manually |

---

## Amazon Redshift

Column-oriented data warehouse (MPP — Massively Parallel Processing) for large-scale analytics.

- **Cluster**: Leader node (query planning) + Compute nodes (store and process)
- **Redshift Spectrum**: runs SQL queries on S3 data without loading it into the cluster
- **Columnar storage**: excellent compression, optimized for aggregations
- **Enhanced VPC Routing**: forces COPY/UNLOAD traffic through the VPC (not internet)
- **Snapshots**: automatic (retention 1–35 days) or manual; cross-region possible
- **Redshift Serverless**: auto-scaling without managing cluster, pays per RPU-second

---

## Specialized Databases

| Service | Type | Use Case |
|---|---|---|
| **Amazon DocumentDB** | Document (MongoDB compatible) | Catalogs, CMS, user profiles |
| **Amazon Neptune** | Graph | Social networks, fraud detection, knowledge graphs |
| **Amazon Keyspaces** | Wide column (Cassandra compatible) | IoT, telemetry, large-scale time-series |
| **Amazon QLDB** | Ledger (immutable, auditable) | Financial records, supply chain, transaction history |
| **Amazon Timestream** | Time-series | IoT, DevOps metrics, time-series telemetry |

---

## How to Choose the Right Database (Exam)

```
Relational data + fixed schema + ACID?
  ├── High availability + MySQL/PostgreSQL compatibility → Aurora
  └── Oracle/SQL Server (specific license) → RDS

Semi-structured data (JSON), flexible, massive scale?
  └── DynamoDB (key-value/document)

Analytics, BI, data warehouse?
  └── Redshift

High-speed cache?
  ├── Session, leaderboard, pub/sub → ElastiCache Redis
  └── Simple multi-threaded cache → ElastiCache Memcached

Graphs (friends of friends, fraud detection)?
  └── Neptune

Immutable auditing (cannot alter history)?
  └── QLDB

IoT / high-ingestion time-series?
  └── Timestream

Migrated MongoDB workload?
  └── DocumentDB
```

---

## Common Exam Pitfalls

- **RDS Multi-AZ != Read Replica**: Multi-AZ is synchronous HA (standby does not read); Read Replica is asynchronous scale (readable)
- **Aurora stores 6 copies across 3 AZs**, quorum 4/6 for writes
- **Aurora Global Database** < 1s cross-region replication — perfect for low global RPO
- **DynamoDB Partition Key** must have high cardinality for uniform distribution (hot partition = throttling)
- **GSI** = can create at any time; **LSI** = only at table creation
- **DAX** = us latency; only for DynamoDB; does not help for writes (write-through)
- **ElastiCache Redis** has Multi-AZ, persistence, replication — use when these features matter
- **Redshift Spectrum** = query S3 without loading into cluster (serverless query on data lake)
- **QLDB** = immutable ledger — questions about financial history auditing
- **RDS Proxy** = connection pool — ideal for Lambda + RDS

## Hands-on Lab

For relational database and modeling practice, use [11-RDS-and-Relational-Databases-Labs/lab.md](../11-RDS-and-Relational-Databases-Labs/lab.md) and [12-DynamoDB/lab.md](../12-DynamoDB/lab.md).
Cost notes: use small instance classes, keep minimum backup retention for the lab, and remove instances, snapshots, and test tables when done.

## Practice Questions

- [questions.md](./questions.md)

## Quick Review / Cheatsheet

- [cheatsheet.md](./cheatsheet.md)
- [flashcards.md](./flashcards.md)
