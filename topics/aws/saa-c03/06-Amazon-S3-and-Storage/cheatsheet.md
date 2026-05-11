# Cheatsheet — Module 05: Amazon S3 and Storage

## S3 Storage Classes

| Class | Availability | AZs | Retrieval Fee | Min. Duration | Main Use |
|---|---|---|---|---|---|
| S3 Standard | 99.99% | >= 3 | None | None | Frequently accessed data |
| S3 Intelligent-Tiering | 99.9% | >= 3 | None | None | Unpredictable access patterns |
| S3 Standard-IA | 99.9% | >= 3 | Per GB | 30 days | Infrequent access, fast retrieval |
| S3 One Zone-IA | 99.5% | 1 | Per GB | 30 days | Reproducible data, low cost |
| S3 Glacier Instant | 99.9% | >= 3 | Per GB | 90 days | Rarely accessed archives, ms retrieval |
| S3 Glacier Flexible | 99.99% | >= 3 | Per GB | 90 days | Archives, minutes/hours retrieval |
| S3 Glacier Deep Archive | 99.99% | >= 3 | Per GB | 180 days | Long-term backup, hours retrieval |

## S3 Encryption Types

| Type | Key Management | Encryption Management | Cases |
|---|---|---|---|
| SSE-S3 | AWS | AWS | Lowest operational overhead |
| SSE-KMS | AWS KMS (optional CMK) | AWS | Audit trail, key access control |
| SSE-C | Customer | AWS | Customer wants full key control |
| CSE | Customer | Customer | Compliance requiring client-side encryption |

## S3 Replication

| | CRR | SRR |
|---|---|---|
| Regions | Different regions | Same region |
| Requirement | Versioning on BOTH | Versioning on BOTH |
| Existing objects | Not replicated (use S3 Batch) | Not replicated |
| Delete replicated | Optional with delete marker sync | Optional |

## Performance Per Prefix
- **3,500 PUT/COPY/POST/DELETE** per second per prefix
- **5,500 GET/HEAD** per second per prefix
- Multipart Upload: required > **5 GB**, recommended > **100 MB**
- S3 Transfer Acceleration: uses CloudFront edge → AWS backbone → S3

## Object Lock
| Mode | Who can remove | Period |
|---|---|---|
| Governance | Users with `s3:BypassGovernanceRetention` | Configurable |
| Compliance | NO ONE (not even root) | Configurable, irrevocable |
| Legal Hold | Anyone with `s3:PutObjectLegalHold` | No expiration date |

## Other Storage Services

| Service | Protocol | Multi-AZ | OS | Use Case |
|---|---|---|---|---|
| EBS | Block (iSCSI) | No (zonal) | Win/Linux | Single volume for EC2 |
| EFS | NFS v4 | Yes | Linux | Shared across N EC2s |
| FSx for Windows | SMB/NTFS | Yes | Windows | AD, DFS |
| FSx for Lustre | Lustre | Yes | Linux | HPC, ML, big data |
| FSx for ONTAP | NFS/SMB/iSCSI | Yes | Win/Linux | NetApp migration |
| FSx for OpenZFS | NFS | Yes | Linux | ZFS/POSIX migration |

## Storage Gateway

| Type | Protocol | Where it persists |
|---|---|---|
| File Gateway | NFS/SMB | S3 (with local cache) |
| Volume Cached | iSCSI | S3 (with local cache) |
| Volume Stored | iSCSI | On-premises (async backup to S3) |
| Tape Gateway | iSCSI VTL | S3 / S3 Glacier |

## Quick Exam Tips
- Versioning = **prerequisite** for CRR, SRR, and Object Lock
- Bucket Policy vs ACL: prefer Bucket Policy (ACL is legacy)
- Block Public Access: 4 independent settings; applies at account AND bucket level
- CORS: required for browser JavaScript to make cross-origin requests to S3
- Pre-signed URL: generated with creator's credentials, expires at configurable time
- S3 Inventory: list bucket objects asynchronously (daily/weekly) — alternative to LIST API
- S3 Select: simple SQL over S3 objects (up to 50% less data transferred)
- DataSync: data migration on-prem → AWS or between AWS services (supports NFS, SMB, HDFS, S3, EFS, FSx)

---
