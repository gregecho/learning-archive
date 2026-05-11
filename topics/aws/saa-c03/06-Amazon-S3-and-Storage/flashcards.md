# Flashcards — Module 05: Amazon S3 and Storage

---

**Q:** What are the 7 S3 storage classes in descending order of storage cost?
**A:** Standard → Intelligent-Tiering → Standard-IA → One Zone-IA → Glacier Instant Retrieval → Glacier Flexible Retrieval → Glacier Deep Archive

---

**Q:** What is the minimum billable storage duration for S3 Standard-IA?
**A:** 30 days (below that, billed as if it were 30 days)

---

**Q:** What is the minimum storage duration for S3 Glacier Deep Archive?
**A:** 180 days

---

**Q:** How many copies does S3 Standard maintain and across how many AZs?
**A:** Minimum 3 copies across at least 3 AZs in the same region (durability 11 9s = 99.999999999%)

---

**Q:** Which S3 class stores in only 1 AZ? What is the risk?
**A:** S3 One Zone-IA. Risk: if the AZ is destroyed, data is lost. Availability 99.5% vs 99.9% of other classes

---

**Q:** What is S3 Intelligent-Tiering and when to use it?
**A:** Automatically moves objects between tiers (Frequent Access, Infrequent Access, Archive tiers) based on access. Ideal for unpredictable patterns. Charges a small monitoring fee but no retrieval fee

---

**Q:** What are the requirements to enable CRR or SRR?
**A:** Versioning must be enabled on BOTH buckets (source and destination). Existing objects are not automatically replicated (use S3 Batch Replication for those)

---

**Q:** What is the difference between SSE-S3, SSE-KMS, and SSE-C?
**A:** SSE-S3: AWS manages keys (AES-256). SSE-KMS: keys managed via AWS KMS (audit trail, fine-grained permissions). SSE-C: customer provides the key on each request; AWS encrypts/decrypts but does not store the key

---

**Q:** What is S3 Bucket Key and what is the benefit?
**A:** Reduces the number of KMS API calls by creating an envelope key per bucket (not per object). Reduces SSE-KMS cost by up to 99%

---

**Q:** What is the throughput per S3 prefix for PUT and GET?
**A:** 3,500 PUTs/COPY/POST/DELETE and 5,500 GET/HEAD per second **per prefix**. Distributing across multiple prefixes linearly increases total throughput

---

**Q:** When is Multipart Upload mandatory on S3?
**A:** Required for objects above **5 GB**. Recommended for objects above **100 MB**

---

**Q:** What is the difference between Object Lock Governance and Compliance?
**A:** Governance: users with `s3:BypassGovernanceRetention` permission can delete/modify. Compliance: NO ONE can delete (not even root/AWS) during the retention period. Compliance is irrevocable

---

**Q:** What is Legal Hold in S3 Object Lock?
**A:** Protects the object from deletion regardless of retention period. Can be applied/removed by any user with `s3:PutObjectLegalHold` permission. Does not expire automatically

---

**Q:** What is S3 Transfer Acceleration used for?
**A:** Uses CloudFront edge locations to accelerate client uploads to S3 (especially clients geographically distant from the S3 region). Traffic goes to the nearest CloudFront edge, then via AWS backbone to S3

---

**Q:** What is the difference between Gateway Endpoint and Interface Endpoint for S3?
**A:** Gateway Endpoint: free, added as a route in the route table, only within the VPC. Interface Endpoint (PrivateLink): has cost ($/hour + $/GB), creates ENI with private IP, accessible from on-prem via DX/VPN

---

**Q:** What is Amazon FSx for Lustre and what is its main use case?
**A:** High-performance file system based on Lustre (open-source HPC). Integrates natively with S3 (reads/writes directly). Use cases: ML training, HPC, video rendering, parallel data processing

---

**Q:** What are the 4 types of AWS Storage Gateway?
**A:** File Gateway (NFS/SMB → S3), Volume Gateway Cached (iSCSI, primary data in S3, local cache), Volume Gateway Stored (iSCSI, primary data local, S3 backup), Tape Gateway (VTL → S3/Glacier)

---

**Q:** What is S3 Select and what is the benefit?
**A:** Allows running simple SQL queries (SELECT) on S3 objects (CSV, JSON, Parquet) without downloading the entire file. Reduces transferred data and cost. Simple alternative to Athena for one-off queries

---

**Q:** How do S3 Event Notifications work?
**A:** Triggers events to SNS, SQS, or Lambda when actions occur on the bucket (s3:ObjectCreated, s3:ObjectRemoved, s3:ObjectRestore, etc.). Can filter by key prefix and suffix. Alternative: use EventBridge (more flexible)

---

**Q:** What is the difference between EFS and EBS?
**A:** EFS: managed NFS4, multi-AZ, concurrent access from multiple instances/AZs, scales automatically, Linux only. EBS: block storage, typically attached to 1 instance (except io2 Multi-Attach), single-AZ, Windows/Linux

---
