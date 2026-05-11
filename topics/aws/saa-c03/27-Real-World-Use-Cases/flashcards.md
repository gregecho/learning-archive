# Flashcards — Module 27: Real-World Use Cases

> **Format:** Q = Question | A = Answer  
> **Total:** 25 flashcards

---

**Q:** What is the "Strangler Fig" pattern and how to implement it on AWS?  
**A:** Gradual migration pattern from monolith to microservices. New functionalities are built as microservices; old functionalities are migrated incrementally. On AWS: use API Gateway or Application Load Balancer to route traffic — `/new-feature` → Lambda/ECS, `/legacy/*` → EC2 monolith. Gradual, no big-bang rewrite.

---

**Q:** How to architect a highly available e-commerce application on AWS?  
**A:** Frontend: CloudFront + S3 (SPA). Backend: ALB + ECS/EC2 in 2+ AZs with Auto Scaling. Database: RDS Aurora Multi-AZ (write) + Read Replicas (read). Cache: ElastiCache (sessions, popular products). Cart/inventory: DynamoDB (high scale). Payments: SQS (exactly-once via deduplicationId). Images: S3 + CloudFront.

---

**Q:** What is the fan-out pattern and when to use it on AWS?  
**A:** Fan-out: one event triggers multiple consumers in parallel. Implementation: SNS Topic → multiple SQS Queues (or Lambda). Each subscriber processes independently. Use when: one event needs to trigger multiple actions (order_placed → SQS_email + SQS_fulfillment + SQS_analytics + SQS_audit). Decouples publisher from multiple consumers.

---

**Q:** How to implement exactly-once processing for payments on AWS?  
**A:** SQS FIFO Queue with **MessageDeduplicationId** (hash of transactionId). If the same transaction is sent twice with the same DeduplicationId within the 5-minute window, only one is delivered. In processing: idempotency check in the database (check if transactionId has already been processed before debiting).

---

**Q:** What architecture for an IoT pipeline with 100,000 devices?  
**A:** Devices → IoT Core (MQTT) → Rules Engine → multiple destinations: Kinesis Data Streams (streaming analytics), DynamoDB (latest readings), S3 (via Kinesis Firehose, historical data). For real-time alerts: Lambda Consumer on KDS. For historical analysis: Athena on S3. Visualization: QuickSight or Grafana.

---

**Q:** How to use the CQRS (Command Query Responsibility Segregation) pattern on AWS?  
**A:** Separate write and read into different models/stores. Write path (Command): API Gateway → Lambda → DynamoDB (source of truth). Read path (Query): denormalized data in ElastiCache or OpenSearch for fast reading. Sync: DynamoDB Streams → Lambda → updates read model. Write optimized for consistency; read optimized for performance.

---

**Q:** How to architect a serverless Data Lake on AWS?  
**A:** Ingestion: Kinesis Firehose (streaming) + DataSync (batch). Storage: S3 with date partitioning. Catalog: Glue Crawler → Glue Data Catalog. Transform: Glue ETL Jobs (raw → curated → analytics zones). Query: Athena (SQL). Security: Lake Formation (FGA by column/row). Visualization: QuickSight. Orchestration: Step Functions or MWAA.

---

**Q:** What is Event Sourcing and how to implement it on AWS?  
**A:** Instead of saving current state, save all events that led to the state: `order_created`, `payment_processed`, `shipped`. Current state is rebuilt by replaying events. AWS: DynamoDB Streams or Kinesis as event log. EventBridge to publish events. Advantage: full audit, temporal queries (state at any point in time), debugging.

---

**Q:** How to implement authentication with Cognito in an SPA + S3?  
**A:** (1) Cognito User Pool for authentication (username/password, OAuth social). (2) Cognito Identity Pool to exchange User Pool token for temporary AWS credentials (assumed IAM Role). (3) Frontend uses temporary credentials to call API Gateway (authenticated via Cognito Authorizer) or access S3 directly. No authentication backend to manage.

---

**Q:** What architecture for a video streaming platform (Netflix-like)?  
**A:** Upload: S3 + pre-signed URL. Transcoding: S3 Event → SQS → EC2/ECS with MediaConvert or Elemental. CDN: CloudFront with S3 origins (processed video). DRM: CloudFront Signed URLs or Signed Cookies. Metadata: DynamoDB or Aurora. Recommendations: SageMaker Personalize. Analytics: Kinesis → Redshift/Athena.

---

**Q:** How to implement multi-tenant with tenant isolation on AWS?  
**A:** Strategies: **(1) Silo model:** AWS account per tenant (maximum isolation, high administrative cost). **(2) VPC per tenant:** shared account, separate VPCs. **(3) S3 prefixes:** `s3://bucket/tenant-id/data/` with IAM conditions `Condition: {"StringLike": {"s3:prefix": "${aws:PrincipalTag/TenantId}/*"}}`. **(4) DynamoDB partition key** = tenantId. Choice depends on isolation requirements.

---

**Q:** What is the typical serverless architecture pattern in the SAA-C03 exam?  
**A:** API GW → Lambda → DynamoDB (simple CRUD). Variations: + S3 pre-signed URLs for direct upload. + Cognito for auth. + SQS to decouple Lambda from heavy processing. + EventBridge for scheduling. + Step Functions for multi-step workflows. + Lambda@Edge for CDN customization. + RDS Proxy for Lambda connecting to RDS (connection pooling).

---

**Q:** How to detect fraud in real time with ML on AWS?  
**A:** Transactions → API GW → Lambda → Amazon Fraud Detector (or SageMaker endpoint) → result in <100ms. For historical transactions: Kinesis Data Streams → Lambda (calls FM endpoint). Store decisions: DynamoDB. Re-train models periodically: Kinesis → S3 → SageMaker Training Job → update endpoint. Audit trail: CloudTrail + DynamoDB.

---

**Q:** What is the "Cache-Aside" pattern and how to implement it with ElastiCache?  
**A:** Application manages the cache manually. Read: check ElastiCache → hit: return data. Miss: fetch from RDS → save in ElastiCache → return. Write: update RDS → **invalidate** cache (delete key). Opposite of Write-Through (cache always updated on write). Cache-Aside: lazy loading, less memory used, eventually consistent.

---

**Q:** How to implement Blue/Green Deployment with zero downtime on AWS?  
**A:** Option 1: **ELB + ASG** — create new Target Group (green) with new version, gradually shift traffic on the ALB Listener Rule. Option 2: **CodeDeploy Blue/Green** — automates process + automatic rollback. Option 3: **Lambda aliases + weighted routing** (10% v2 → 100% v2). Option 4: **Elastic Beanstalk** — swap environment URLs. Rollback: redirect traffic back.

---

**Q:** How to architect product search in e-commerce with high performance?  
**A:** DynamoDB as source of truth → DynamoDB Streams → Lambda → OpenSearch Service (indexing). Frontend searches in OpenSearch (full-text, filters, autocomplete, facets). Benefit: OpenSearch returns in <10ms for complex queries. DynamoDB does not natively support full-text search. Data mapped with analyzed (tokenized) fields in OpenSearch.

---

**Q:** What are the main integration patterns between AWS services?  
**A:** **(1) Sync:** API Gateway → Lambda (client waits). **(2) Async:** API GW → Lambda → SQS → another Lambda (fire-and-forget). **(3) Fan-out:** SNS → multiple SQS. **(4) Streaming:** KDS → Lambda/KDA. **(5) Schedule:** EventBridge Scheduler → Lambda. **(6) Workflow:** Step Functions → multiple orchestrated services. Each pattern for a use case.

---

**Q:** How to ensure HIPAA compliance in AWS architecture?  
**A:** (1) Use HIPAA-eligible services (EC2, RDS, S3, Lambda, etc. — check BAA). (2) Sign Business Associate Agreement (BAA) with AWS. (3) Encryption: KMS CMKs, encryption at rest and in transit. (4) Audit logging: CloudTrail + CloudWatch Logs. (5) Access control: IAM with least-privilege principle. (6) Network: private VPC + VPN/DX for access. (7) Encrypted data backups.

---

**Q:** How to implement DLQ (Dead Letter Queue) in a serverless architecture?  
**A:** **Async** invocation (SNS, S3 Events): DLQ configured directly on the Lambda function (SNS retries 2x, Lambda retries 2x). Failed messages go to SQS DLQ. **Event Source Mapping** (SQS): DLQ is configured on the SQS (not on Lambda). SQS will try for maxReceiveCount, then move to SQS DLQ. Preferred: use Lambda Destinations for async invocations (more flexible).

---

**Q:** What architecture for backend application with low RTO (<5 min) and RPO (<1 min) multi-region?  
**A:** Active-Active: Route 53 with health checks + Latency/Failover Routing. Stateless API in both regions (ECS/Lambda). Database: Aurora Global Database (replication <1s, automatic failover in ~1 min). Cache: ElastiCache Global Datastore (cross-region replica). S3 CRR for assets. Sessions: DynamoDB Global Tables. CloudFront with origins in multiple regions.

---

**Q:** What is the Saga pattern and when to use it on AWS?  
**A:** Manage distributed transactions in microservices. Each service performs a local transaction and publishes an event. If a subsequent phase fails: compensating transactions undo previous steps. AWS: Step Functions (orchestration — knows global state) or Choreography via SNS/EventBridge (each service reacts to events). Use when: eventual consistency is needed in multi-service transactions.

---

**Q:** How to use SSM Parameter Store for application configuration?  
**A:** Parameter hierarchy: `/app/prod/database/password` (SecureString with KMS). Lambda/ECS fetches parameters at initialization via SDK. Advantages over env vars: (1) versioning; (2) encrypted secrets; (3) auditable (CloudTrail); (4) change without redeploy (Lambda can read on cold start). For automatic rotation: Secrets Manager.

---

**Q:** How to implement serverless image processing on AWS?  
**A:** Upload: pre-signed S3 URL (directly from browser to S3, bypassing backend). Upload trigger: S3 Event → Lambda. Lambda processes: Pillow/Sharp → resize/thumbnail → saves result to S3. CDN: CloudFront distributes processed images. For heavy processing: S3 Event → SQS → Lambda (throttled) or EC2 Spot via ASG. Metadata: DynamoDB.

---

**Q:** What is the typical architecture for a real-time notification system?  
**A:** Backend → EventBridge (or SNS) → multiple channels: (1) Email: SES. (2) SMS: SNS → SMS. (3) Push notifications: SNS → GCM/APNs. (4) In-app real-time: API GW WebSocket API + Lambda + DynamoDB (connection tracking). (5) Slack: Lambda → Slack API. Fan-out pattern for multiple simultaneous channels without coupling the backend.

---

**Q:** How does the exam test knowledge of multi-tier (3-tier) architectures?  
**A:** **Presentation:** CloudFront + S3 (SPA) or ALB. **Application:** EC2 ASG or ECS in private subnets (no direct internet access). **Data:** RDS in private data subnet (only accepts connections from the application tier's SG). The exam tests: correct SG flow, that databases are in private subnets, that ALB is in public subnet, that application EC2 doesn't need a public IP.
