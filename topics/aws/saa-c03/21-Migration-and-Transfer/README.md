# Module 15 — Migration and Data Transfer

## The 7 Migration Strategies (7 Rs)

| Strategy | Name | Description | Effort |
|---|---|---|---|
| **Retire** | Retire | Discontinue application: no business value | None |
| **Retain** | Retain | Keep on-premises for now (compliance, technical debt, revisit later) | None |
| **Rehost** | Lift & Shift | Move to EC2 without changes (e.g., MGN) | Low |
| **Relocate** | Relocate | Move to AWS without changes (VMware Cloud on AWS, Kubernetes) | Low |
| **Replatform** | Lift & Reshape | Small optimizations without core refactoring (e.g., move to RDS instead of Oracle on EC2) | Medium |
| **Repurchase** | Replace | Migrate to SaaS (e.g., CRM → Salesforce, email → Microsoft 365) | Medium |
| **Refactor / Re-architect** | Refactor | Rewrite leveraging cloud-native (e.g., monolith → microservices + Lambda + containers) | High |

---

## AWS Migration Hub

Central migration tracking dashboard:
- Visualizes progress of all servers being migrated
- Integrates with **Application Discovery Service**, **MGN**, **DMS**
- **Migration Hub Orchestrator**: coordinates and automates migration sequences

---

## AWS Application Discovery Service

Collects data from the on-premises environment for migration planning:

| Mode | How it works |
|---|---|
| **Agentless Discovery** (Connector) | VM appliance on VMware vCenter; discovers VMs, CPU, memory, storage without installing agent |
| **Agent-based Discovery** | Installs ADS Agent on each server; collects more detailed data (running processes, network connections) |

Data exported to Migration Hub or S3 for analysis with Athena.

---

## AWS Application Migration Service (MGN/SMS)

**AWS MGN** (successor to SMS - Server Migration Service):
- Automated **Rehost (lift-and-shift)** to EC2
- Installs replication agent on source server → continuously replicates disk blocks to AWS
- **Cutover**: testing in staging → maintenance window → final cutover

```
On-prem Server
  │
  ├── MGN Replication Agent installed
  │     └── Continuous replication → S3/EBS on AWS
  │
  ├── Launch Template (instance type, VPC, SG)
  │
  └── Test → Cutover → EC2 in production
           └── Very low RTO/RPO (minutes)
```

---

## AWS Database Migration Service (DMS)

Database migration:

| Type | Sources/Destinations | SCT |
|---|---|---|
| **Homogeneous** | Oracle→Oracle, MySQL→RDS MySQL, PostgreSQL→Aurora | Not needed |
| **Heterogeneous** | Oracle→Aurora, SQL Server→PostgreSQL | **SCT required** |

**Schema Conversion Tool (SCT)**: converts schema + stored procedures to the target database dialect

**CDC (Change Data Capture)**: replicates ongoing changes after initial migration (supports ongoing replication with zero downtime)

**DMS Replication Instance**: EC2 that runs the replication job; needs connectivity with source and target

**Supported Sources**: Oracle, SQL Server, MySQL, PostgreSQL, MongoDB, SAP, IBM DB2, S3
**Supported Targets**: all above + DynamoDB, Redshift, Kafka, OpenSearch, DocumentDB

---

## AWS Snow Family

Physical data transfer (edge computing and massive migration):

| Product | Capacity | Edge Computing | Typical Use |
|---|---|---|---|
| **Snowcone** | 8-14 TB | Yes (2 vCPU, 4 GB) | Small physical environments, IoT |
| **Snowball Edge Storage Optimized** | 80 TB HDD + 1 TB SSD | Yes (40 vCPU, 80 GB) | Large-scale data migration |
| **Snowball Edge Compute Optimized** | 42 TB + 28 TB SSD | Yes (52 vCPU, 208 GB, optional GPU) | Local analytics, ML at the edge |
| **Snowmobile** | **100 PB** (exabyte-scale) | No | Entire data center migration |

**Rule of thumb**: if upload would take more than 1 week via internet → use Snow Family

Process:
1. AWS ships the device
2. You load data locally
3. Ship back to AWS
4. AWS loads data into S3

For **Snowball after S3**: lifecycle policy to Glacier if needed.

---

## AWS DataSync

AUTOMATED and scheduled data transfer:

| From → To | Protocol | Speed |
|---|---|---|
| On-prem → S3/EFS/FSx | NFS, SMB | Up to 10 Gbps per agent |
| S3 → S3 (cross-region/account) | S3 API | High |
| EFS → EFS | NFS | High |

- **Installation**: DataSync Agent (VM appliance) on-prem; connects via Direct Connect/VPN or internet
- **Preserves metadata**: timestamps, Unix permissions
- **Integrity verification**: verifies checksums on both sides
- **Scheduled**: creates tasks with scheduling (incremental after first full transfer)

**DataSync vs Storage Gateway vs Snow Family:**
```
DataSync: scheduled/automated transfer (migration + sync)
Storage Gateway: continuous hybrid access (not a migration tool)
Snow Family: when the network is insufficient or too slow
```

---

## AWS Transfer Family

Managed transfer protocols for S3 and EFS:

| Protocol | Port |
|---|---|
| SFTP (SSH FTP) | 22 |
| FTPS (FTP over TLS) | 990 |
| FTP (unencrypted) | 21 |
| AS2 (Applicability Statement 2) | 8080/HTTPS |

- Maintains existing endpoints (no need to change clients)
- Auth via IAM, Cognito, custom Lambda (for existing LDAP/AD)
- Ideal for: B2B partners using SFTP; migrations of legacy SFTP servers to S3

---

## Other Migration Services

| Service | Function |
|---|---|
| **AWS Mainframe Modernization** | Migrates and modernizes IBM/Micro Focus mainframes to AWS |
| **CloudEndure Disaster Recovery** | Continuous replication for DR (replaced by MGN for migration) |
| **Migration Hub Refactor Spaces** | Incremental migration from monolith to microservices |

---

## Exam Tips

- **7 Rs**: identifying the correct strategy per scenario is a frequent question
  - "No change, move to EC2" = Rehost (MGN)
  - "MySQL on EC2 → RDS" = Replatform
  - "No value, shut down" = Retire
- **DMS**: for DB migration; SCT = heterogeneous schema conversion
- **DataSync** vs **Snow Family**: DataSync = network available + automation; Snow = no good network
- **Snowmobile** = only for **exabyte** scale (>100 PB); Snowball Edge = 80 TB per device
- Transfer Family: clients **do not need to change anything** → AWS receives transfers and stores in S3/EFS
- **MGN** includes **continuous replication** → very low RTO at cutover time
- Application Discovery Service: agentless (VMware VMs via connector) vs agent-based (any OS, more detailed)
- DMS with CDC = **zero-downtime migration**: replicates ongoing changes while testing
- DataSync preserves metadata (timestamps, permissions); Snow Family does not necessarily
- **SCT** (Schema Conversion Tool) is separate from DMS — desktop tool for converting DDL and procedures

---
