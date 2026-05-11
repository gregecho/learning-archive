# Questions — Module 27: Real-World Use Cases

> **SAA-C03 Domain**: All domains (multi-service)  
> **Difficulty**: High

---

**1.** A video streaming company needs an architecture that supports 1 million concurrent users, serves videos with low latency globally, and scales automatically. Which AWS services make up the ideal architecture?

- A) EC2 + ELB + RDS
- B) CloudFront + S3 (static content) + ALB + Auto Scaling Group + Aurora (metadata)
- C) API Gateway + Lambda + DynamoDB
- D) Global Accelerator + EC2 + RDS Multi-AZ

<details><summary>Answer</summary>

**B** — CloudFront caches videos at edge locations globally (low latency, reduces origin load). S3 stores video files (unlimited scale, low cost). ALB + ASG scales the application layer (metadata, authentication, playlists). Aurora for transactional data with Read Replicas for high read throughput.

</details>

---

**2.** An e-commerce platform needs to process payments ensuring each transaction is processed exactly once, even in case of retry. Which architecture guarantees this?

- A) API Gateway → Lambda → SQS Standard → processing Lambda
- B) API Gateway → Lambda → SQS FIFO → processing Lambda with idempotency key
- C) API Gateway → Lambda → DynamoDB → SNS
- D) API Gateway → direct Lambda (explicit retry on client)

<details><summary>Answer</summary>

**B** — SQS FIFO with MessageDeduplicationId = exactly-once delivery. In the processor, use the transaction ID as an Idempotency Key in DynamoDB (conditional put: only write if it does not exist) to guarantee exactly-once processing even if the message is re-delivered. Double protection: SQS FIFO (dedup) + DynamoDB conditional write.

</details>

---

**3.** A fintech startup needs an architecture that detects fraud in real-time transactions (latency < 100ms), processes 10,000 transactions per second, and maintains full audit trail. Which architecture implements this?

- A) S3 + Athena for batch fraud analysis (review after the day)
- B) API GW → Lambda → SageMaker endpoint (real-time ML models) → DynamoDB (result) + Kinesis → S3 + Athena (audit)
- C) RDS Aurora with fraud detection stored procedures
- D) EC2 with fraud detection application running 24/7

<details><summary>Answer</summary>

**B** — For real-time with ML: SageMaker real-time endpoint returns prediction in <100ms. The transaction also goes to Kinesis Firehose → S3 for audit in Athena. DynamoDB stores prevention results. Lambda orchestrates everything, scaling automatically to 10,000 TPS.

</details>

---

**4.** A multi-tenant SaaS company needs to isolate each client's (tenant) data in S3, ensuring that one tenant never accesses another's data. Which mechanism implements this?

- A) A single S3 bucket with prefixes per tenant and generic bucket policy
- B) One S3 bucket per tenant with bucket policy + Cognito Identity Pool with assume role per tenant
- C) Shared S3 with per-object ACLs for each tenant
- D) S3 Object Ownership with ACLs enabled per object

<details><summary>Answer</summary>

**B** — Strong isolation: bucket per tenant + Cognito Identity Pool (federates users to tenant-specific IAM roles). The tenant-bucket policy allows access only from the tenant's role. No cross-tenant access is possible. Alternative (A) with prefixes is easier to implement but less secure (one misconfiguration can expose all tenants).

</details>

---

**5.** A company wants to migrate from a monolithic architecture to microservices without downtime, using the Strangler Fig pattern. How to implement this on AWS?

- A) Create all microservices first and do full cutover on a weekend
- B) ALB with path-based routing: new routes go to microservices, legacy routes go to the monolith; migrate gradually
- C) Route 53 with weighted routing splitting traffic between monolith and microservices
- D) B is the correct Strangler Fig pattern; traffic is migrated incrementally by domain

<details><summary>Answer</summary>

**D** — Strangler Fig: ALB as facade. New features and migrated routes go to microservices (ECS/Lambda); legacy features still go to the monolith. Gradually, all routes are migrated and the monolith is "strangled" (decommissioned). Route 53 weighted would be more for blue/green of the entire monolith, not incremental migration.

</details>

---

**6.** An IoT company has 100,000 devices sending telemetry every 10 seconds. The data needs to be processed in real time for alerts and stored for historical analytics. Which architecture to use?

- A) IoT Core → Lambda (per message) → DynamoDB + S3
- B) IoT Core → Kinesis Data Streams → Lambda (real-time alerts) + Kinesis Firehose → S3 (storage) + Athena (analytics)
- C) MQTT broker EC2 → SQS → Lambda
- D) API Gateway → Lambda → DynamoDB Streams → Analytics

<details><summary>Answer</summary>

**B** — IoT Core: managed MQTT/HTTPS for 100k devices. Kinesis Data Streams absorbs 100k × 10s = 10k messages/second. Lambda processes stream for real-time alerts. Kinesis Firehose in parallel delivers to S3 in Parquet. Athena does historical analytics. Serverless, managed, and scalable solution.

</details>

---

**7.** A marketplace company needs to notify 5 different teams (email, mobile push, audit, analytics, CRM) when an order is created. What is the most appropriate pattern?

- A) REST API that calls the 5 systems sequentially
- B) SNS topic (order created) → 5 SQS queues (one per system) → each system consumes its own queue (fan-out pattern)
- C) EventBridge with 5 rules pointing to each system
- D) B and C are valid; SNS fan-out is simpler; EventBridge is better for complex conditional rules

<details><summary>Answer</summary>

**D** — SNS Fan-out: SNS → multiple SQS (or Lambda directly) in parallel. Simple and direct. EventBridge: better when different events need different filters/rules (e.g., only notify analytics for orders > $500). For the simple case described, SNS fan-out is sufficient.

</details>

---

**8.** A company needs a product search system that supports full-text search, filters by category/price, and autocompletion. The database has 10 million products. Which AWS service to use?

- A) DynamoDB with GSI for category filters
- B) Amazon OpenSearch Service with product indexes
- C) Amazon Aurora with Full-Text Search
- D) Amazon Kendra

<details><summary>Answer</summary>

**B** — OpenSearch: full-text search engine, compound filters, autocompletion (completion suggester), fuzzy matching, relevance scoring. 10 million documents is viable in a properly sized OpenSearch cluster. DynamoDB does not have full-text search. Kendra is for enterprise document search, not product catalogs.

</details>

---

**9.** A company wants to build a serverless data lake where data engineers can do ETL in Python, analysts can run SQL queries, and data scientists can train ML models, all on the same S3 data. Which architecture?

- A) Permanent EMR for all workloads
- B) S3 + Glue Data Catalog + Glue Studio (ETL) + Athena (SQL) + SageMaker (ML)
- C) Redshift as central data repository for everything
- D) Aurora + QuickSight for all use cases

<details><summary>Answer</summary>

**B** — S3 as universal storage (raw and processed data). Glue Data Catalog: shared metastore. Glue Studio: serverless Python/Spark ETL. Athena: SQL over S3 (serverless). SageMaker: ML on S3 data. Each persona uses the ideal tool, all access the same data on S3 via Glue Catalog.

</details>

---

**10.** A web application needs to authenticate users with Google, Facebook, and email/password, and then access DynamoDB and S3 directly from the browser (client-side) without going through the backend. Which service implements this?

- A) IAM Users for each application user
- B) Amazon Cognito: User Pools (auth) + Identity Pools (temporary AWS credentials for client-side access)
- C) API Gateway with Lambda Authorizer to validate OAuth tokens
- D) AWS SSO for web application users

<details><summary>Answer</summary>

**B** — Cognito User Pool: signup/login with email/password + federation with Google, Facebook (social). Identity Pool: exchanges the Cognito token (or social) for temporary AWS credentials (STS assume role). The browser can then access S3 and DynamoDB directly with temporary credentials, without exposing permanent credentials.

</details>

---

**11.** A media company needs to process user-uploaded videos (transcoding to multiple formats and resolutions). Processing is heavy (30-60 minutes per video) and volume is unpredictable. Which architecture?

- A) Lambda for transcoding (max timeout 15 min — insufficient)
- B) S3 event → SQS → ECS Fargate tasks (scale based on queue depth) for transcoding
- C) EC2 On-Demand with Auto Scaling
- D) AWS Elemental MediaConvert (managed service specific for transcoding)

<details><summary>Answer</summary>

**D** — AWS Elemental MediaConvert: managed service specific for video transcoding. Supports multiple input/output formats, resolution presets, DRM, subtitles. S3 → MediaConvert → S3. Serverless, pay per minute of transcoded output. Alternative: S3 → SQS → Fargate tasks with FFmpeg (B) — more flexible but more complex.

</details>

---

**12.** A company needs a cloud development environment where developers write, run, and debug code directly from the browser, without setting up local environments. Which AWS service?

- A) AWS Cloud9 (browser-based IDE with EC2 in background)
- B) AWS CloudShell
- C) Amazon WorkSpaces
- D) AWS CodeStar

<details><summary>Answer</summary>

**A** — AWS Cloud9: complete browser-based IDE with code editor, integrated terminal, debugger, and Lambda development support. Runs on EC2 (or SSM for existing instances). Real-time collaboration. CloudShell (B) is terminal only without IDE. WorkSpaces (C) is a full virtual desktop.

</details>

---

**13.** A blog platform has predictable traffic spikes (article launches) that last 2 hours. Most content is static. What is the most cost-effective architecture?

- A) Auto Scaling Group with CPU-based scaling
- B) CloudFront caching static content (articles, images) → origin ALB + small ASG (for dynamic content only)
- C) Lambda for all content (including dynamic HTML generation)
- D) EC2 with high memory for local memory cache

<details><summary>Answer</summary>

**B** — CloudFront absorbs most traffic for static content without reaching the origin. Only non-cacheable requests (search, comments, user-specific) reach the backend. The ASG can be minimal. During spikes, CloudFront scales automatically (global infrastructure). Cost-effective because it eliminates most backend load.

</details>

---

**14.** A company needs to ensure it can restore its application in a new region in less than 1 hour after a regional failure. Which combination of strategies should it implement?

- A) Daily EBS snapshots + AMIs copied to second region
- B) Multi-region AMIs + Aurora Global DB + S3 CRR + Route 53 health check failover + IaC (CloudFormation)
- C) Only S3 CRR for data backup
- D) AWS Backup with cross-region backup for all resources

<details><summary>Answer</summary>

**B** — For RTO < 1 hour: pre-copied AMIs (EC2 ready to launch), Aurora Global DB (replicated DB with RPO < 1s), S3 CRR (replicated data), Route 53 automatic failover, and CloudFormation to quickly provision infrastructure. AWS Backup (D) is good for backups but does not coordinate orchestrated failover.

</details>

---

**15.** A healthcare company needs to store medical records with strict controls: only authorized doctors access their patients' records, audit of all access, encryption with customer-managed keys, and HIPAA compliance. Which architecture?

- A) RDS MySQL with per-doctor users
- B) S3 with AES256 + per-doctor IAM policies
- C) DynamoDB (data) + KMS CMK (encryption) + IAM with resource-based conditions + CloudTrail Data Events (audit) + AWS Artifact (HIPAA certification)
- D) Aurora with SSL + Cognito User Pools

<details><summary>Answer</summary>

**C** — Full HIPAA compliance: DynamoDB with KMS CMK (customer-managed key = full encryption control); IAM with conditions (`dynamodb:LeadingKeys` to restrict by doctor-patient patient_id); CloudTrail Data Events: records all DynamoDB reads; AWS Artifact: obtains BAA (Business Associate Agreement) documents required for HIPAA.

</details>
