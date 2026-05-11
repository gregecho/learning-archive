# Cheatsheet — Module 06: Databases

## RDS Multi-AZ vs Read Replica Comparison

| | Multi-AZ | Read Replica |
|---|---|---|
| Purpose | High availability / DR | Read scalability |
| Replication | Synchronous | Asynchronous |
| RPO | ~0 (no data loss) | Small lag possible |
| RTO | ~1-2 minutes (DNS flip) | Manual (promote to standalone) |
| Can receive reads? | NO (standby only) | YES (read only) |
| Cross-region? | No (same region) | Yes (up to 5 per DB) |
| Failover | Automatic | Manual |

## Aurora vs RDS

| | Aurora | RDS |
|---|---|---|
| Copies | 6 (across 3 AZs) | 2 (Multi-AZ: primary + standby) |
| Write quorum | 4/6 | 1 (primary synchronous to standby) |
| Read Replicas | Up to 15 | Up to 5 |
| RR Failover | ~30 seconds | Manual promote |
| Global Database | Yes (< 1s lag) | No (manual DX/VPN only) |
| Serverless | v2 (0.5-128 ACU) | No (except Aurora) |
| Performance | 3x MySQL / 5x PostgreSQL | Standard |

## DynamoDB — Key Values

| Parameter | Value |
|---|---|
| 1 RCU (Eventually Consistent) | 2 reads of 4 KB/s |
| 1 RCU (Strongly Consistent) | 1 read of 4 KB/s |
| 1 WCU | 1 write of 1 KB/s |
| DAX latency | Microseconds |
| TTL | Free; eventual deletion within 48h |
| Streams retention | 24 hours |
| Global Tables | Active multi-region replication |

## DynamoDB Indexes

| | LSI | GSI |
|---|---|---|
| When to create | Only at table creation | Any time |
| Partition Key | Same as table | Different |
| Sort Key | Different from table | Any attribute |
| Throughput | Shared with table | Independent |
| Consistency | Strong or Eventually | Eventually only |

## ElastiCache Redis vs Memcached

| | Redis | Memcached |
|---|---|---|
| Persistence | Yes (RDB, AOF) | No |
| Replication | Yes (Replica) | No |
| Multi-AZ | Yes | No |
| Cluster Mode | Yes (sharding) | Yes (multi-thread) |
| Data Structures | String, Hash, List, Set, Sorted Set, Geo, Streams | String only |
| Pub/Sub | Yes | No |
| Use case | Sessions, leaderboards, rich cache, queues | Simple cache, high-speed multi-thread |

## Caching Patterns

| Pattern | Cache Miss | Cache Hit | Pros | Cons |
|---|---|---|---|---|
| Lazy Loading | Fetch DB → write cache | Return cache | Only stores what's needed | 3 round-trips on miss; data may go stale |
| Write-Through | Write DB + cache | Return cache | Always fresh data | Write penalty; caches never-read data |
| Write-Behind | Write cache → async DB | Return cache | Lower write latency | Risk of loss if cache fails before persisting |

## Database Selection

| Need | Database |
|---|---|
| Relational OLTP (low latency) | RDS MySQL/PostgreSQL/Aurora |
| Relational OLTP (high performance) | Aurora |
| Relational OLAP / Data Warehouse | Redshift |
| NoSQL key-value / document | DynamoDB |
| In-memory cache | ElastiCache Redis |
| Graph | Amazon Neptune |
| Document (MongoDB) | Amazon DocumentDB |
| Time series (IoT, metrics) | Amazon Timestream |
| Immutable ledger | Amazon QLDB |
| Managed Cassandra | Amazon Keyspaces |

## Quick Exam Tips
- RDS Multi-AZ endpoint does not change after failover (same DNS CNAME)
- Aurora: 2 main endpoints — Cluster Endpoint (write) + Reader Endpoint (read LB)
- DynamoDB Global Tables require On-Demand or enable replication via replica write capacity
- Redshift Spectrum: query S3 data directly from Redshift without COPY
- RDS Proxy: mandatory when Lambda accesses RDS (connection pooling, IAM auth, Secrets Manager)
- ElastiCache Redis Cluster Mode: distributes keyspace across multiple shards → greater capacity and write throughput
- Aurora Serverless v2: scales in ~1 second (does not require restart like v1)
- PITR RDS retention: 1-35 days; Aurora: up to 35 days
