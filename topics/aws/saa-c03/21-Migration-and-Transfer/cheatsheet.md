# Cheatsheet — Module 15: Migration and Transfer

## The 7 Rs — Migration Strategies

| Strategy | Name | Change | Example |
|---|---|---|---|
| **Retire** | Decommission | None | App no longer used |
| **Retain** | Keep on-premises | None | Compliance, latency |
| **Rehost** | Lift-and-shift | Minimal | EC2 = on-premises VM |
| **Relocate** | Move VMware | Minimal | VMware Cloud on AWS |
| **Replatform** | Lift-and-optimize | Targeted | RDS instead of self-managed MySQL |
| **Repurchase** | Switch to SaaS | Product change | Salesforce instead of custom CRM |
| **Refactor** | Rearchitect | Major | Microservices + Lambda + DynamoDB |

---

## Snow Family — Capacity and Usage

| Device | Storage | Compute | When to Use |
|---|---|---|---|
| **Snowcone Small** | 8 TB SSD | 2 vCPUs, 4 GB RAM | Remote locations, weight: 2.1 kg |
| **Snowcone Large** | 14 TB SSD | 4 vCPUs, 4 GB RAM | Higher capacity in the field |
| **Snowball Edge Storage** | 80 TB HDD | 40 vCPUs | Large-scale data migration |
| **Snowball Edge Compute** | 42 TB HDD | 52 vCPUs, optional GPU | Heavy edge computing |
| **Snowmobile** | 100 PB | N/A | Entire data center |

**Decision rule:** `data_size / available_bandwidth > 1 week` → use Snow Family.

---

## Comparison: AWS MGN vs DMS vs DataSync

| | MGN | DMS | DataSync |
|---|---|---|---|
| **Type** | Server rehost | Database migration | File transfer |
| **Source** | Any server (Win/Linux) | Database | NFS, SMB, S3, HDFS |
| **Target** | EC2 | RDS, Aurora, Redshift | S3, EFS, FSx |
| **Replication** | Continuous (block-level) | CDC (transactions) | Batch or scheduled |
| **Downtime** | Minutes (manual cutover) | Minimal (CDC) | N/A |
| **Prerequisite** | Agent on server | DMS task configured | DataSync Agent on-premises |

---

## DMS + SCT — When to Use Each

| Migration | DMS | SCT |
|---|---|---|
| MySQL → MySQL RDS | Yes | Not needed |
| Oracle → Oracle RDS | Yes | Not needed |
| Oracle → Aurora PostgreSQL | Yes (data) | Yes (schema conversion) |
| SQL Server → RDS PostgreSQL | Yes (data) | Yes (schema conversion) |
| Oracle → Redshift | Yes (data) | Yes (schema conversion) |

**Rule:** same engine (homogeneous) = DMS only. Different engines (heterogeneous) = SCT first + DMS.

---

## AWS DataSync — Use Cases

| Use Case | Configuration |
|---|---|
| On-premises NFS → S3 | DataSync Agent on-prem, Location NFS + S3 |
| S3 → EFS | No agent (AWS-to-AWS), Location S3 + EFS |
| HDFS on-prem → S3 | Agent on-prem, Location HDFS + S3 |
| SMB/Windows → S3 | Agent on-prem, Location SMB + S3 |
| S3 → FSx for Windows | No agent, Location S3 + FSx WFS |

**Preserves:** POSIX permissions, timestamps, ACLs. **Verifies:** integrity via end-to-end checksums.

---

## AWS Transfer Family — Protocols

| Protocol | Port | Encryption | Use Case |
|---|---|---|---|
| **SFTP** | 22 | TLS | Standard for secure file transfer |
| **FTPS** | 990/21 | TLS explicit/implicit | Legacy systems needing FTP + TLS |
| **FTP** | 21 | None | Internal networks (not recommended for internet) |
| **AS2** | 443 | TLS + S/MIME | B2B EDI (Electronic Data Interchange) |

Storage backend: **S3** or **EFS**.

---

## Migration Hub — Migration Phases

```
Phase 1: DISCOVER
   Application Discovery Service
   ↓ (inventory + dependencies)

Phase 2: ASSESS
   Migration Evaluator (TCO)
   Migration Hub (prioritization)
   ↓ (business case)

Phase 3: MIGRATE
   MGN (servers) / DMS (databases) / DataSync (files)
   ↓ (migration + replication)

Phase 4: CUTOVER
   Stop source → Validate target → Redirect traffic
   ↓

Phase 5: MODERNIZE
   Post-migration refactoring (optional)
```

---

## Exam Tips — Common Migration Patterns

| Clue in the Question | Likely Answer |
|---|---|
| "Move Windows server to EC2 with minimal downtime" | AWS MGN |
| "Migrate Oracle to Aurora PostgreSQL" | SCT (schema) + DMS (data + CDC) |
| "Terabytes of data, internet would be slow" | AWS Snowball Edge |
| "100 PB of data to AWS" | AWS Snowmobile |
| "Move NFS files to S3 preserving permissions" | AWS DataSync |
| "External partner needs SFTP" | AWS Transfer Family |
| "VMware VM migration with minimal change" | AWS MGN or Relocate (VMware Cloud) |
| "Discover on-prem app dependencies" | Application Discovery Service |
| "Calculate TCO before migrating" | AWS Migration Evaluator |
| "Track centralized migration progress" | AWS Migration Hub |
| "Continuous client access via FTP to S3" | AWS Transfer Family |
| "Replicate database changes in real time during migration" | DMS with CDC |
| "Edge sensor data without reliable connectivity" | Snowball Edge (Compute Optimized) |

---
