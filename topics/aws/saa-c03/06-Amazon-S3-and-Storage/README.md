# Module 05 — Amazon S3 and Storage

## Objective

In this module, you will master storage architecture decisions on AWS, choosing services and storage classes based on cost, latency, durability, security, and retrieval requirements for both exam and production scenarios.

## Main AWS Services

- Amazon S3
- Amazon EFS
- Amazon FSx
- AWS Storage Gateway
- AWS DataSync

## Architecture and Trade-offs

## S3 Storage Classes

Amazon S3 offers a spectrum of classes that balance cost, durability, and access latency:

| Class | Availability | AZs | Latency | Min. Storage | Use Case |
|---|---|---|---|---|---|
| S3 Standard | 99.99% | >=3 | ms | None | Frequently accessed data |
| S3 Intelligent-Tiering | 99.9% | >=3 | ms | 30 days | Unpredictable access patterns |
| S3 Standard-IA | 99.9% | >=3 | ms | 30 days | Backups, DR accessed monthly |
| S3 One Zone-IA | 99.5% | 1 | ms | 30 days | Reproducible data, thumbnails |
| S3 Glacier Instant Retrieval | 99.9% | >=3 | ms | 90 days | Archives accessed 1x/quarter |
| S3 Glacier Flexible Retrieval | 99.99% | >=3 | minutes–hours | 90 days | Archives that can wait hours |
| S3 Glacier Deep Archive | 99.99% | >=3 | 12–48h | 180 days | Compliance, 7-10 year retention |

> **Durability:** All classes have 11 9s (99.999999999%) except One Zone-IA (99.5% availability, same durability but in 1 AZ).

### S3 Intelligent-Tiering
Automatically moves objects between tiers based on access:
- **Frequent Access** (default) → **Infrequent Access** (30 days without access) → **Archive Instant** (90 days) → **Archive Access** (90–730 days, optional) → **Deep Archive Access** (180–730 days, optional)
- Charges a monitoring fee per object (no retrieval fee on Frequent/Infrequent)

---

## Lifecycle Policies

Rules that automatically transition objects between classes or delete them:

```
Object created (Standard)
    ↓ 30 days → Standard-IA
    ↓ 90 days → Glacier Instant Retrieval
    ↓ 180 days → Glacier Deep Archive
    ↓ 365 days → DELETE (expiration)
```

Key points:
- Minimum transition between Standard and Standard-IA/One Zone-IA: **30 days**
- Lifecycle can apply to non-current versions (with versioning enabled)
- **Lifecycle does not apply to objects < 128 KB** (not cost-effective for Glacier)
- Can filter by prefix, tags, or object size

---

## Versioning and Replication

### Versioning
- Enabled at the bucket level — cannot be disabled once activated (only suspended)
- Each object version has a unique `VersionId`
- `DELETE` on a versioned object creates a **delete marker** — the object is not physically deleted
- To permanently delete: must specify the `VersionId`

### Replication
| Type | Description |
|---|---|
| **CRR** (Cross-Region Replication) | Source and destination in different regions. DR, compliance, reduced read latency |
| **SRR** (Same-Region Replication) | Same region. Log aggregation, production → staging, compliance |

Requirements:
- Versioning **enabled** on both buckets (source and destination)
- IAM Role with `s3:ReplicateObject` permission on the destination
- Replication is **prospective** — objects prior to activation are not replicated (use S3 Batch for existing objects)
- S3 Replication Time Control (RTC): guarantees 99.99% of objects replicated within 15 minutes (paid SLA)

---

## S3 Security

### Access Control
- **Bucket Policy** (resource-based): JSON, allows cross-account access, conditions (IP, VPC endpoint, MFA, etc.)
- **ACLs** (legacy): object or bucket level. AWS recommends disabling ACLs and using only bucket policies
- **Access Points**: simplify policies for multiple applications on a bucket — each access point has its own policy

### Pre-signed URLs
- Temporary URLs with the generator's credentials embedded
- Can be for GET or PUT
- Configurable expiration (max 7 days for SDK, 12h for `aws s3 presign`)
- Uses the permissions of whoever generated the URL at the time of access

### CORS
Cross-Origin Resource Sharing — required when a web application on `domain-a.com` makes a request to the bucket `domain-b.s3.amazonaws.com`. Configured via CORS rules on the bucket (AllowedOrigins, AllowedMethods, AllowedHeaders).

### Block Public Access
- **4 settings** that block: new ACLs, any ACL, new bucket policies with public access, any policy
- Enabled by default on new buckets
- Can be configured at the account level (AWS Organizations)

---

## S3 Encryption

| Type | Key Management | Where Encryption Occurs |
|---|---|---|
| **SSE-S3** | AWS (AES-256, key per object) | Server-side (default, no additional cost) |
| **SSE-KMS** | You (CMK or aws/s3) | Server-side, audited by CloudTrail, KMS API cost |
| **SSE-C** | You (key sent in request) | Server-side, AWS encrypts but does not store the key |
| **CSE** | You (encrypt before sending) | Client-side, S3 stores ciphertext |

As of 2023, SSE-S3 is the default for new buckets (unless configured otherwise).

**Bucket Key (SSE-KMS):** Reduces KMS API calls by up to 99% using a derived key per bucket, instead of calling KMS for each object. Enabled by default on new buckets with SSE-KMS.

---

## S3 Performance

- **Prefixes**: S3 scales to **3,500 PUTs/s and 5,500 GETs/s per prefix**. Distributing objects across multiple prefixes (e.g., name hash) maximizes throughput
- **Multipart Upload**: recommended for objects > 100 MB, **required** > 5 GB. Parallelizes uploads into parts
- **S3 Transfer Acceleration**: uses CloudFront Edge Locations for global upload acceleration via the AWS backbone network
- **S3 Byte-Range Fetches**: parallelizes downloads by dividing the object into ranges (similar to multipart but for reading)

---

## S3 Object Lock (WORM)

Prevents objects from being deleted or overwritten for a defined or indefinite period:

| Mode | Behavior |
|---|---|
| **Governance** | Only users with `s3:BypassGovernanceRetention` can overwrite or delete |
| **Compliance** | **No one** (including root) can delete or modify while active, nor change the mode |

- **Legal Hold**: WORM without expiration date, toggled by those with `s3:PutObjectLegalHold`
- Requires versioning enabled
- Ideal for regulatory compliance (SEC Rule 17a-4, FINRA, CFTC)

---

## S3 Event Notifications

Triggers notifications on object operations (`s3:ObjectCreated:*`, `s3:ObjectRemoved:*`, etc.):
- **Destinations**: SNS topic, SQS queue, Lambda function, **EventBridge**
- For events via EventBridge: all S3 operations are available with advanced filters and multiple destinations

---

## Amazon S3 Select and Glacier Select

- **S3 Select**: runs simple SQL queries (`SELECT * FROM S3Object WHERE...`) directly on S3, filtering data before transferring — reduces cost and latency
- **Supports**: CSV, JSON, Parquet (compressed with GZIP/BZIP2)

---

## Other Storage Services

### Amazon EFS (Elastic File System)
- **Managed NFS file system**, Linux-compatible (NFS v4.1)
- **Multi-AZ** by default (Standard) or Single-AZ for EC2 in the same AZ (lower cost)
- Classes: Standard and Standard-IA (like S3, lifecycle moves between them)
- **Performance modes**: General Purpose (default, low latency) and Max I/O (high concurrency)
- **Throughput modes**: Bursting (scales with storage), Provisioned (fixed), Elastic (recommended — auto-adjusts)
- Charged per GB stored (more expensive than EBS, but shared across instances)

### Amazon FSx
| Type | For | Protocol | Highlights |
|---|---|---|---|
| FSx for Windows File Server | Windows Apps / AD | SMB | Native AD, DFS Namespaces, NTFS |
| FSx for Lustre | HPC, ML, Media | POSIX | Sub-ms latency, integrates with S3, scratch vs persistent |
| FSx for NetApp ONTAP | On-prem migration | NFS/SMB/iSCSI | Deduplication, multi-protocol capability |
| FSx for OpenZFS | ZFS migration | NFS | Snapshots, clone, compression |

### AWS Storage Gateway
| Type | Protocol | Use Case |
|---|---|---|
| File Gateway | NFS/SMB | On-prem extension to S3 (files become objects) |
| Volume Gateway (Cached) | iSCSI | Primary data in S3, local cache; backups as EBS snapshots |
| Volume Gateway (Stored) | iSCSI | Primary data on-prem, async backup to S3 |
| Tape Gateway | iSCSI VTL | Replaces physical tape, backup goes to S3/Glacier |

### AWS DataSync
- **Incremental** and scheduled data transfer between on-prem and AWS (S3, EFS, FSx)
- Agent installed on-prem, compression and in-transit encryption
- Up to **10 Gbps** throughput, verifies data integrity

---

## Common Exam Pitfalls

- **S3 Standard by default** — always the safe answer when no cost requirements
- **One Zone-IA** only for **reproducible** data (thumbnails, transcodes) — do not use for critical backup
- **Glacier Instant** = ms access; **Glacier Flexible** = minutes/hours; **Deep Archive** = 12–48h
- **Object Lock Compliance** = nobody deletes, not even root — FINRA, SEC compliance
- **Pre-signed URL** uses the generator's permissions — if the role is revoked, the URL stops working
- **SSE-KMS with Bucket Key** reduces KMS calls by ~99% — better cost
- **CRR requires versioning on both buckets**
- FSx for Lustre: integrates with S3 as a data repository — HPC reads/writes directly to Lustre, syncs with S3
- EFS: charged for actual usage; EBS: charged for provisioned capacity

## Hands-on Lab

For guided practice, use the advanced S3 lab at [07-S3-Advanced-Labs/lab.md](../07-S3-Advanced-Labs/lab.md).
Cost notes: prioritize small files for lifecycle/replication tests, use few objects per step, and remove buckets, versions, and replication rules at the end.

## Practice Questions

- [questions.md](./questions.md)

## Quick Review / Cheatsheet

- [cheatsheet.md](./cheatsheet.md)
- [flashcards.md](./flashcards.md)

---
