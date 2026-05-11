# Cheatsheet — EC2 Compute

## EC2 Instance Families

| Family | Optimization | Examples | Use cases |
|---|---|---|---|
| M | General (balanced) | m5, m6i, m6a, m7g | Web servers, apps, dev environments |
| C | CPU (compute) | c5, c6i, c6g, c7g | HPC, batch, ML inference, encoding |
| R | Memory | r5, r6i, r6g, x1e | Redis, Elasticsearch, SAP HANA, in-memory DB |
| I | Local I/O (NVMe) | i3, i4i | NoSQL DB (Cassandra, MongoDB), high IOPS OLTP |
| D | Dense storage | d3 | Data warehousing, HDFS |
| P | GPU (NVIDIA) | p3, p4 | ML training, HPC with CUDA |
| G | General GPU | g4dn, g5 | ML inference, gaming, rendering |
| T | Burstable | t3, t3a, t4g | Dev environments, low-traffic sites, microservices |
| Inf | AWS Inferentia | inf1, inf2 | Custom chip ML inference |
| Hpc | HPC | hpc6a | High-performance HPC with EFA |

---

## EC2 Purchasing Options

| Option | Discount | Flexibility | Best for |
|---|---|---|---|
| On-Demand | None | Full | Irregular workloads, testing |
| Standard RI (1/3 years) | Up to 72% | Low (family/region/OS fixed) | Stable production PostgreSQL DB |
| Convertible RI (1/3 years) | Up to 54% | Medium (can change attributes) | Workloads that may change type |
| Compute Savings Plans | Up to 66% | High (any family/region) | Workloads that move between types |
| EC2 Instance Savings Plans | Up to 72% | Low (family+region fixed) | Similar to Standard RI |
| Spot | Up to 90% | High (but interruptible) | Batch, ML, rendering, fault-tolerant jobs |
| Dedicated Host | — | Low | Per-socket/core licensing (BYO-L) |
| Dedicated Instance | 10% surcharge | Low | Compliance (exclusive hardware) |
| Capacity Reservation | None | Full | Guarantee capacity without commitment |

---

## EBS — Volume Types

| Type | Category | IOPS | Throughput | Boot | Typical use |
|---|---|---|---|---|---|
| gp3 | General SSD | 3,000–16,000 | 125–1,000 MB/s | Yes | Boot, general apps, default |
| gp2 | General SSD | 100–16,000 (3/GB) | 128–250 MB/s | Yes | Legacy (prefer gp3) |
| io2 | IOPS SSD | Up to 64,000 (io2 BE: 256K) | 4,000 MB/s | Yes | Critical OLTP, Oracle, SQL |
| io1 | IOPS SSD | Up to 64,000 | 1,000 MB/s | Yes | Legacy io2 |
| st1 | Throughput HDD | N/A | 40–250 MB/s per TB (max 500) | No | Logs, Kafka, sequential data warehouse |
| sc1 | Cold HDD | N/A | 12–80 MB/s per TB | No | Rarely accessed data, backup |

> **Note:** io2 Block Express requires `io2 BE` type instances. Multi-attach available only on io1/io2 on Nitro instances.

---

## Placement Groups — Comparison

| Type | Topology | Limit | Latency | Use |
|---|---|---|---|---|
| Cluster | Same rack, same AZ | No practical limit | Lowest (<1ms, 10Gbps+) | HPC, MPI, high-speed analytics |
| Spread | Different rack per instance | 7 instances per AZ | High (distinct racks) | High availability, isolated failure |
| Partition | Instance groups per rack | 7 partitions per AZ | Moderate | HDFS, Cassandra, Kafka (partition-aware) |

---

## EC2 Lifecycle

```
Pending → Running ──┬─→ Stopping → Stopped → Terminated
                    │         (EBS preserved)
                    ├─→ [Hibernate] → Hibernating → Stopped (RAM saved to EBS)
                    │
                    └─→ Shutting-down → Terminated
                                        (EBS root deleted if deleteOnTermination=true)
```

| State | Instance billed | EBS billed | RAM preserved |
|---|---|---|---|
| Running | Yes | Yes | Yes |
| Stopped | No | Yes | No |
| Hibernated | No | Yes (RAM on root) | Yes |
| Terminated | No | No (generally) | No |

---

## IMDSv1 vs IMDSv2

| Feature | IMDSv1 | IMDSv2 |
|---|---|---|
| Authentication | None (direct GET) | Token (PUT → GET with header) |
| SSRF Protection | Vulnerable | Protected |
| Configuration | `HttpTokens: optional` | `HttpTokens: required` |
| Token TTL | N/A | 1s to 21600s (6h) |
| AWS Recommendation | Deprecated | Always use |

Important endpoints:
```
http://169.254.169.254/latest/meta-data/instance-id
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
http://169.254.169.254/latest/meta-data/placement/availability-zone
http://169.254.169.254/latest/user-data
```

---

## AMIs — Exam Tips

- Copy AMI to another region → specify destination CMK for encryption
- Share encrypted AMI → must also share the CMK
- Snapshot-based AMI → the snapshot stays in your account if you created the AMI
- Public AMI from AWS Marketplace → can use but cannot share the base snapshot
- HVM is the only virtualization type on modern instances (PV is legacy)

---

## Spot — Spot Fleet Strategies

| Strategy | Behavior | When to use |
|---|---|---|
| `lowestPrice` | Chooses lowest-priced pool | Cost-critical batch |
| `capacityOptimized` | Chooses pool with most available capacity | Reduce interruptions |
| `diversified` | Distributes across all defined pools | Maximum resilience |
| `priceCapacityOptimized` | Combines price and capacity | Recommended default |

---

## Exam Tips (EC2)

- **gp3** is the current default — cheaper and more flexible than gp2
- **io2 Block Express** for requirements > 64,000 IOPS
- **st1** for sequential throughput (logs) — NOT a boot option
- **Instance Store** lost on stop/terminate, but persisted on restart
- **Cluster PG** → same AZ, low latency. If one instance fails, all are exposed
- **Spread PG** → max 7 per AZ — choose for critical isolated instances
- IMDSv2 with `HttpTokens: required` blocks IMDSv1 — hardened security
- Spot Fleet `capacityOptimized` is preferred to reduce interruptions vs `lowestPrice`
- **Dedicated Host** is required for BYO-L (license mobility) — not Dedicated Instance
- Hibernate: RAM saved to EBS → requires encrypted EBS + size >= RAM

---
