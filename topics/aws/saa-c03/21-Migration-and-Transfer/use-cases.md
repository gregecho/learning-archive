# Real Use Cases — Migration and Transfer (Module 15)

## Case 1 — Lift-and-Shift of a Corporate Data Center

**Context:** Manufacturing company with 200 on-premises servers (Windows Server + SQL Server, Linux + Oracle) needs to migrate to AWS in 12 months. Wants minimum initial rework (lift-and-shift) with later modernization.

**Requirements:**
- Cutover window < 2 hours per server
- Zero data loss during migration
- Continuous replication before cutover
- Rollback plan in case of failure

**Migration Architecture with MGN:**
```
PHASE 1 — DISCOVERY (weeks 1-4):
AWS Application Discovery Service (discovery agent on servers)
├── Maps dependencies between apps (which servers communicate)
├── Collects: CPU, memory, disk, network traffic
└── Migration Hub → groups into migration waves

PHASE 2 — REPLICATION (weeks 5-20):
On-premises → AWS MGN (Application Migration Service)
        AWS Replication Agent installed on each server
                │ Continuous replication over TCP 1500
                ▼
        AWS Staging Area (replication server instances)
                │
                ▼
        EBS Volumes (copy of on-premises disks)

PHASE 3 — TEST CUTOVER (weeks 21-23):
MGN → Launch Test Instance (launch template configured)
├── Validate app works on AWS
├── Test connectivity with other services
└── Check performance (same or better)

PHASE 4 — PRODUCTION CUTOVER:
├── Freeze on-premises traffic (30min maintenance)
├── MGN finalizes replication (delta sync)
├── Launch production instances
├── Update DNS (Route 53 → new IPs)
└── Monitor 48h before decommissioning on-premises
```

**Rollback Plan:**
- MGN keeps staging instances for 90 days after cutover
- DNS can be reverted in < 5 minutes (Route 53 low TTL)
- On-premises is not decommissioned until full validation

---

## Case 2 — PostgreSQL Database Migration to Aurora with DMS

**Context:** FinTech with on-premises PostgreSQL database (500 GB, 100 transactions/second) needs to migrate to Amazon Aurora PostgreSQL without interrupting operations. System processes payments 24/7.

**Requirements:**
- Zero downtime during migration
- Cutover window < 10 minutes
- Validate data integrity after migration
- Rollback capability in 15 minutes

**Architecture with DMS (Change Data Capture):**
```
PHASE 1 — FULL LOAD:
PostgreSQL On-Prem ──── DMS Replication Instance ──── Aurora PostgreSQL
   (source endpoint)          (r5.xlarge)              (target endpoint)
                         Full Load Task
                         ├── Copies all tables
                         ├── Disables FK constraints (temporary)
                         └── Creates indexes after load (faster)

Estimated duration: 4-6 hours (500GB)

PHASE 2 — CDC REPLICATION (while Full Load is still running):
DMS → Change Data Capture (captures INSERT/UPDATE/DELETE)
     └── Applies changes to Aurora in real time
     └── Replication latency: < 1 second

CUTOVER (when replication lag ≈ 0):
1. Application: read-only mode (or maintenance page 5min)
2. DMS: verify lag = 0 (no pending data)
3. Change app connection string → Aurora endpoint
4. AWS SCT validated: same structure + matching checksums
5. Resume normal operation
6. Monitor 24h = rollback available (DMS still active in reverse direction)

ROLLBACK:
DMS reverse task (Aurora → PostgreSQL on-prem) pre-configured
Connection string change back in < 5 minutes
```

**Full Load vs CDC Difference:**
| Mode | What it does | When to use |
|------|-----------|-------------|
| Full Load | Single complete copy | Traffic can be interrupted |
| CDC | Replicates incremental changes | Zero-downtime migration |
| Full Load + CDC | Copy + tracks changes | **Recommended standard** |

---

## Case 3 — 500 TB Transfer with AWS Snowball Edge

**Context:** Oil company with remote base (no fiber, 100 Mbps satellite link) needs to transfer 500 TB of historical seismic data to S3 and then process it with EMR.

**Requirements:**
- Transfer in < 30 days
- Encrypted data during transport
- No dependency on internet link (slow link)
- Processing of data subset at the edge before sending

**Feasibility Calculation:**
```
500 TB via internet (100 Mbps):
  500 TB = 500 x 1024 x 8 Gbits = 4,096,000 Gbits
  @ 100 Mbps = 0.1 Gbps
  Time = 4,096,000 / 0.1 / 3600 / 24 = ~474 days

Snowball Edge Storage Optimized (80 TB usable):
  500 TB / 80 TB = 7 devices
  Packaging + shipping + ingestion: ~3 weeks
  ✓ MUCH FASTER
```

**Process:**
```
AWS Console → Order 7 Snowball Edge Storage Optimized
                    │ Delivery in 2-5 business days
                    ▼
Remote Base:
  ├── Connect Snowball to local network (10 GbE)
  ├── Snowball Client → transfer data to device
  ├── (optional) Snowball Edge compute: local Lambda for pre-processing
  └── Automatic encryption (AES-256, key in KMS)

Ship to AWS (carrier)
                    │
                    ▼
AWS Data Center → Automatic ingestion into S3
                    │
                    ▼
S3 (seismic data) → EMR (Spark processing)
                  → Athena (ad hoc analysis)

Notification: SNS email when ingestion complete
Verification: MD5 checksum automatic by the service
```

---

## Case 4 — Heterogeneous Migration Oracle → Aurora PostgreSQL

**Context:** HR company wants to eliminate Oracle license ($500K/year) by migrating to Aurora PostgreSQL. Database has 2 TB with stored procedures, PL/SQL packages, and Oracle-specific functions.

**Requirements:**
- Convert PL/SQL code to PL/pgSQL (natively incompatible)
- Identify incompatibilities before starting
- Migrate data with minimal downtime
- Document all conversions for auditing

**Process with SCT + DMS:**
```
PHASE 1 — ASSESSMENT:
AWS SCT (Schema Conversion Tool)
├── Connects to on-premises Oracle
├── Generates compatibility report:
│   ├── 70% code automatically converted ✓
│   ├── 20% requires manual adjustment (Oracle-specific logic)
│   └── 10% needs to be rewritten (features without equivalent)
└── Priority: fix the 30% manual before continuing

PHASE 2 — CONVERSION:
SCT automatically converts:
├── Tables, indexes, views → CREATE TABLE/INDEX/VIEW
├── Basic PL/SQL → PL/pgSQL
└── Sequences → PostgreSQL Sequences

DBA team manually fixes:
├── CONNECT BY (hierarchy) → Recursive CTE
├── ROWNUM → ROW_NUMBER() OVER()
├── Oracle packages → PostgreSQL schemas + functions
└── Implicit cursors → Explicit PgSQL cursors

PHASE 3 — DATA MIGRATION:
DMS Full Load + CDC (same as case 2, but Oracle source → Aurora PG)
Difference: SCT must be applied before DMS

PHASE 4 — VALIDATION:
AmazonDMS data validation (table hashes automatically compared)
Regression tests (critical query suite must return same results)
```

---

## Case 5 — Transfer Family for B2B Integration with Partners

**Context:** Logistics company needs to receive files from 50 partners via SFTP (industry legacy standard) and process them automatically. Currently maintains 2 on-premises SFTP servers.

**Requirements:**
- Maintain SFTP protocol (partners do not change)
- Process files automatically upon arrival
- Each partner sees only their folder
- High availability (no server maintenance)

**Architecture:**
```
Partners (50 companies)
    │ SFTP (port 22)
    ▼
AWS Transfer Family (managed SFTP endpoint)
├── Custom DNS: sftp.company.com (Route 53)
├── Authentication: AWS Secrets Manager (SSH key per partner)
└── Storage: S3 (bucket per partner or prefix per partner)

S3 Structure:
  s3://logistics-partners/
    partner-A/incoming/   (partner A only accesses this prefix)
    partner-B/incoming/   (partner B only accesses this prefix)

Access Control:
IAM Policy per partner:
  s3:PutObject only in /{partner}/{userid}/*
  s3:GetObject only in /{partner}/{userid}/*

AUTOMATIC PROCESSING:
S3 Event (s3:ObjectCreated) → Lambda (process-file)
├── Validates file format (CSV, EDI)
├── Moves to /processed/ after validation
├── Inserts records into DynamoDB
└── SNS → internal system updates delivery status

MONITORING:
CloudWatch Logs (each SFTP connection logged)
CloudTrail (who uploaded which file, when)
CloudWatch Alarm (file not received from critical partner in 24h)
```

**Benefits vs on-premises SFTP:**
| Item | On-premises | Transfer Family |
|------|------------|----------------|
| HA | Manual (2 VMs) | Native Multi-AZ |
| Scalability | Limited | Automatic |
| Maintenance | Manual patches | Zero |
| Cost | Servers + licenses | Per hour + per GB |
| Auditing | Manual logs | Native CloudTrail |

---
