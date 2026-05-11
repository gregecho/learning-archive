# Exam Questions — Module 05: Amazon S3 and Storage

<!-- SAA-C03 Domain: Design Resilient Architectures / Cost-Optimized Architectures -->

---

**1.** A company stores access logs with an unpredictable access pattern for an indeterminate period. They need the lowest possible cost without manually managing tiers. Which S3 class is most appropriate?

- A) S3 Standard-IA
- B) S3 Glacier Flexible Retrieval
- C) S3 Intelligent-Tiering
- D) S3 One Zone-IA

<details>
<summary>Answer</summary>
**C — S3 Intelligent-Tiering**
Automatically moves objects between tiers (Frequent, Infrequent, Archive Instant, Archive) based on access patterns. Ideal when the pattern is unpredictable. One Zone-IA would be good if the data can tolerate loss; Standard-IA incurs retrieval cost on frequent access.
</details>

---

**2.** An S3 bucket needs to be publicly accessible to host a static website. The administrator enabled "Block Public Access" on the account but wants to release only this bucket. What should they do?

- A) Not possible — account-level Block Public Access is irrevocable
- B) Disable Block Public Access on the account, then apply a public bucket policy
- C) Enable "requester pays" on the bucket to allow public access
- D) Create an S3 endpoint and access via CloudFront without making the bucket public

<details>
<summary>Answer</summary>
**D — Use CloudFront with OAC (recommended)**
The best practice is NOT to make the bucket public. Use CloudFront with Origin Access Control (OAC). But if the question requires a public bucket: the correct answer is B — disable Block Public Access on the account and apply a bucket policy. Option D is architecturally superior and is what AWS recommends.
</details>

---

**3.** A company wants to replicate S3 objects from us-east-1 to ap-southeast-1 to reduce latency for users in Asia. Which feature should be enabled?

- A) S3 Transfer Acceleration
- B) Cross-Region Replication (CRR)
- C) Same-Region Replication (SRR)
- D) S3 Multi-Region Access Points

<details>
<summary>Answer</summary>
**B — Cross-Region Replication (CRR)**
CRR asynchronously replicates objects between buckets in different regions. Requires versioning enabled on both. SRR is for the same region. Transfer Acceleration speeds up client uploads to S3, it does not replicate objects. Multi-Region Access Points route to the nearest bucket but do not replicate on their own.
</details>

---

**4.** Which type of S3 encryption allows the customer to manage the keys but AWS performs the encryption/decryption?

- A) SSE-S3 (AES-256)
- B) SSE-KMS
- C) SSE-C
- D) Client-Side Encryption (CSE)

<details>
<summary>Answer</summary>
**C — SSE-C**
SSE-C: the customer provides the key on each HTTP request; AWS encrypts/decrypts but never stores the key. SSE-S3: AWS manages everything. SSE-KMS: AWS manages via KMS (keys can be customer CMKs). CSE: the customer encrypts before sending, AWS sees only encrypted bytes.
</details>

---

**5.** An S3 object needs to be accessed by an external user without AWS credentials for 1 hour. Which mechanism should be used?

- A) Public ACL on the object
- B) Pre-signed URL
- C) Bucket policy with aws:SourceIp condition
- D) VPC Endpoint with open policy

<details>
<summary>Answer</summary>
**B — Presigned URL**
Presigned URLs grant temporary access (configurable duration) to a specific object, using the credentials of whoever generated the URL. They expire after the TTL. Public ACL would expose the object indefinitely. SourceIp restricts by IP, not by time.
</details>

---

**6.** A company has S3 objects that cannot be deleted for 7 years due to financial regulation. Which feature ensures that not even administrators can delete them?

- A) MFA Delete
- B) Versioning with lifecycle policy
- C) S3 Object Lock in Compliance mode
- D) S3 Object Lock in Governance mode

<details>
<summary>Answer</summary>
**C — S3 Object Lock Compliance mode**
In Compliance mode, NO user (including root) can delete or modify the object before the retention period expires. In Governance mode, users with `s3:BypassGovernanceRetention` permission can bypass it. MFA Delete protects bucket deletion, does not guarantee minimum retention.
</details>

---

**7.** An application uploads 1 TB files to S3. What is needed to ensure reliability and efficiency in the upload?

- A) Use S3 Transfer Acceleration exclusively
- B) Use Multipart Upload (required above 5 GB)
- C) Use S3 Batch Operations
- D) Upload to a regional bucket and then replicate with CRR

<details>
<summary>Answer</summary>
**B — Multipart Upload**
Multipart Upload is **required** for objects above **5 GB** and recommended for objects above 100 MB. It divides the file into parallel parts, increasing speed and resilience (failed parts are resent individually). Transfer Acceleration is for reducing geographic latency, not for upload reliability.
</details>

---

**8.** A web client needs to upload files directly from the browser to an S3 bucket on a different domain. What should be enabled on the bucket?

- A) Transfer Acceleration
- B) CORS (Cross-Origin Resource Sharing)
- C) Bucket Policy with public s3:GetObject
- D) ACL with AllUsers permission

<details>
<summary>Answer</summary>
**B — CORS**
CORS controls which origins (external domains) can make requests to the S3 bucket directly from the browser. Without CORS configured, the browser will block cross-origin requests for security. This is required for direct browser uploads (direct-to-S3).
</details>

---

**9.** A company wants to minimize costs by storing audit logs that are rarely accessed but, when needed, must be available in less than 5 minutes. Which S3 class?

- A) S3 Glacier Deep Archive
- B) S3 Glacier Flexible Retrieval
- C) S3 Glacier Instant Retrieval
- D) S3 Standard-IA

<details>
<summary>Answer</summary>
**C — S3 Glacier Instant Retrieval**
Glacier Instant Retrieval offers retrieval in **milliseconds**, at a lower cost than Standard-IA. Ideal for data rarely accessed but needing immediate access when requested. Glacier Flexible Retrieval takes minutes to hours. Deep Archive takes hours.
</details>

---

**10.** A file system needs to be shared simultaneously among 100 Linux EC2 instances across multiple AZs. Which AWS service should be used?

- A) Amazon S3
- B) Amazon EBS (gp3)
- C) Amazon EFS
- D) Amazon FSx for Windows File Server

<details>
<summary>Answer</summary>
**C — Amazon EFS**
EFS is managed NFS for Linux, multi-AZ, allows concurrent access from multiple instances/AZs. EBS is block storage attached to a single instance (except io2 Multi-Attach, limited to 16 instances in the same AZ). FSx for Windows is for Windows environments. S3 has different semantics (object storage).
</details>

---

**11.** A data center company needs to migrate 10 TB of weekly backup data to AWS S3. The internet connection is limited. Which service should be used without AWS SnowFamily?

- A) AWS DataSync via internet
- B) AWS Storage Gateway — Tape Gateway
- C) AWS DataSync via Direct Connect
- D) S3 Transfer Acceleration

<details>
<summary>Answer</summary>
**C — AWS DataSync via Direct Connect**
DataSync is the data migration/synchronization service. With Direct Connect, data travels over a dedicated private link, avoiding the internet. Storage Gateway Tape replaces physical tapes but does not optimize bulk transfer. Transfer Acceleration uses the internet (CloudFront edge).
</details>

---

**12.** A company needs an on-premises server to access files stored in S3 using the NFS/SMB protocol with local cache for low latency. Which service?

- A) AWS DataSync
- B) Amazon EFS with VPN
- C) AWS Storage Gateway — File Gateway
- D) AWS Storage Gateway — Volume Gateway (Stored mode)

<details>
<summary>Answer</summary>
**C — File Gateway**
File Gateway exposes S3 buckets as NFS/SMB file shares for on-premises applications. Local cache keeps recent files for low latency. Data is stored in S3 as objects. DataSync is for batch migration, not continuous access. Volume Gateway works with block storage (iSCSI).
</details>

---

**13.** Which statement about S3 Lifecycle Policies is TRUE?

- A) Objects can transition from S3 Standard directly to S3 Glacier Deep Archive without going through other tiers
- B) Objects can only transition to cheaper tiers (cannot return to Standard)
- C) To transition to Standard-IA or One Zone-IA, objects must be at least 180 days old
- D) S3 Intelligent-Tiering cannot be a destination of a Lifecycle Policy

<details>
<summary>Answer</summary>
**A — Correct**
Lifecycle Policies allow direct transitions between any classes (e.g., Standard → Deep Archive directly). B is true (lifecycle only transitions to cheaper tiers; restoring is manual). C is wrong — the minimum for IA tiers is **30 days**. D is wrong — Intelligent-Tiering can be a destination.
</details>

---

**14.** An S3 bucket receives 100,000 PUTs per second distributed across 10 different prefixes. What is the expected throughput per prefix?

- A) 100 PUT/s per prefix
- B) 3,500 PUT/s per prefix
- C) 5,500 GET/s per prefix
- D) 10,000 PUT/s per prefix (auto-scaling)

<details>
<summary>Answer</summary>
**B — 3,500 PUT/s per prefix**
S3 supports **3,500 PUT/COPY/POST/DELETE** and **5,500 GET/HEAD** per second **per prefix**. Distributing load across 10 different prefixes gives you 35,000 PUTs/s total. This is linear — more prefixes = more throughput.
</details>

---

**15.** A company wants to receive an immediate notification when a specific file is uploaded to S3. Which configuration should be used?

- A) S3 Inventory with daily report
- B) CloudTrail with S3 event filter
- C) S3 Event Notifications → SNS or Lambda
- D) EventBridge Scheduler with bucket polling

<details>
<summary>Answer</summary>
**C — S3 Event Notifications**
S3 Event Notifications trigger events in real time to SNS, SQS, or Lambda when objects are created, deleted, restored, etc. This is the most direct and lowest latency approach. CloudTrail logs API calls but is not for "immediate notification." EventBridge can also be used (S3 integrates with EventBridge) but the most direct way is S3 Event Notifications → Lambda.
</details>

---
