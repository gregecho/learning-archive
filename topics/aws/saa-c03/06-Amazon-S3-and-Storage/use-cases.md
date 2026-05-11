# Use Cases — Module 05: Amazon S3 and Storage

## Case 1: Static Website Hosting with CloudFront and Security

**Scenario:** A company wants to host a static website (React SPA) with low global latency, a private S3 bucket, and HTTPS.

**Architecture:**
```
User (Global)
  └── Route 53 (Alias → CloudFront)
        └── CloudFront Distribution
              └── S3 Bucket (PRIVATE - Block Public Access ON)
                    └── Origin Access Control (OAC) → Bucket Policy
```

**Key settings:**
- S3: Block Public Access = ON; Versioning = ON for rollback
- CloudFront: OAC enabled; Viewer Protocol Policy = HTTPS Only
- Bucket Policy: `Allow cloudfront.amazonaws.com with condition aws:SourceArn = distribution ARN`
- ACM Certificate: us-east-1 (required for CloudFront)
- Route 53: Alias record `www.company.com` → CloudFront distribution

**Why this design?** Private S3 + OAC prevents direct bucket access; CloudFront is the only access path. CloudFront provides global caching → lower latency. HTTPS enforced at all layers.

---

## Case 2: Automated Backup with Lifecycle and Glacier

**Scenario:** A financial company stores monthly reports for 7 years. Access in the first 90 days is frequent; afterward, rarely accessed.

**Lifecycle Policy:**
```
S3 Standard → (90 days) → S3 Standard-IA → (180 days) → S3 Glacier Instant Retrieval
           → (365 days) → S3 Glacier Deep Archive → (7 years) → Expire
```

**Object Lock configured:**
- Compliance mode with 2,555 days retention (7 years)
- Additional Legal Hold for documents under audit

**Why this design?** Lifecycle progressively reduces cost as data "ages." Object Lock Compliance ensures regulatory compliance without the possibility of premature deletion.

---

## Case 3: Multi-Region Data Lake with Replication

**Scenario:** A global company needs data available in us-east-1 (processing) and ap-southeast-1 (Asia data compliance).

**Architecture:**
```
Production (us-east-1)             Read/Compliance (ap-southeast-1)
  └── S3 Bucket [Primary]   →CRR→  S3 Bucket [Replica]
        ├── S3 Event Notification       └── S3 Inventory (compliance)
        │     └── SQS → Lambda (ETL)
        └── S3 Inventory (daily CSV)
```

**Settings:**
- Versioning: ON in both buckets
- CRR: replication of all objects (or by prefix `data/raw/`)
- Encryption: SSE-KMS with different CMKs per region
- Access Points: one per data team with prefix isolation

---

## Case 4: Direct Browser Upload with Pre-signed URL

**Scenario:** A photo platform allows users to upload images directly to S3 without going through the application server.

**Flow:**
```
1. Browser → API Gateway → Lambda
              └── Lambda generates pre-signed URL (PutObject, TTL 15min)
2. Browser → PUT directly to S3 using pre-signed URL
3. S3 Event Notification → SQS → Lambda (image processing)
4. Lambda → writes thumbnail to another bucket
```

**Settings:**
- CORS on S3 bucket: AllowedOrigins = `https://app.company.com`, AllowedMethods = PUT
- Bucket Policy: allows only requests with the presigned URL signature
- CloudFront in front to serve processed images (GET)

---

## Case 5: Migration to AWS with Storage Gateway and DataSync

**Scenario:** Corporate data center with Windows servers accessing file shares. The company wants to migrate to S3 gradually.

**Migration Phases:**
```
PHASE 1 (Coexistence):
  Windows Servers → File Gateway (NFS/SMB) → S3 Bucket
  [File Gateway on-prem; primary data in S3; local cache]

PHASE 2 (Bulk Migration):
  DataSync Agent (on-prem) → AWS DataSync → S3 Bucket
  [Historical data migration with integrity verification]

PHASE 3 (Post-migration):
  Windows Servers → Amazon FSx for Windows (AWS) via Direct Connect
  [Managed file system on AWS with AD integration]
```

**Why Storage Gateway first?** Allows gradual coexistence while teams adapt, without a big-bang cutover. DataSync for bulk migration of existing data.

---
