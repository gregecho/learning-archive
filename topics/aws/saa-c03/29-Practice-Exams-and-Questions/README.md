# Module 29 — Practice Exams and Questions

## Where Each Content Lives

- This file (`README.md`) contains the **Full Practice Exam 1** with 65 questions in SAA-C03 style.
- The file `questions.md` contains **complementary exam strategy questions** (meta-questions about approach and exam format).

## Strategy for the SAA-C03 Exam

### Exam Format
- **65 questions** (multiple choice/multiple select)
- **130 minutes** (2h10min)
- **Minimum score**: 720/1000 (scoring scale of 100-1000)
- **Covered domains:**
  - Design Resilient Architectures: 26%
  - Design High-Performing Architectures: 24%
  - Design Secure Applications: 30%
  - Design Cost-Optimized Architectures: 20%

### Response Strategy
1. Read the **main requirement** highlighted in the question (usually in bold or explicitly stated)
2. Eliminate obvious **distractors** (wrong services for the context)
3. Choose the **most managed** answer that satisfies **all** requirements
4. For multiple-select questions: identify how many answers are requested (2 or 3)
5. Time per question: **~2 minutes**; mark difficult questions for review

---

## Full Practice Exam 1 — 65 Questions

### Section A — Resilient Architectures (Questions 1-17)

**1.** A company needs to run a MySQL database with automatic failover between Availability Zones that supports high read loads. Which service combination solves this?
- A) RDS MySQL Single-AZ with Read Replicas
- B) Amazon Aurora MySQL Multi-AZ with Aurora Read Replicas
- C) Amazon RDS MySQL Multi-AZ with Read Replicas
- D) Amazon DynamoDB with DAX

<details><summary>Answer</summary>

**B** — Aurora MySQL Multi-AZ has automatic failover in ~30s (much faster than RDS Multi-AZ) AND supports up to 15 low-latency Read Replicas. Aurora Read Replicas are part of the cluster and promote automatically in case of failover.

</details>

---

**2.** A critical EC2 application needs RTO < 15 minutes and RPO < 1 hour. Which DR strategy on AWS is most economical for these requirements?
- A) Multi-Site Active-Active in two regions
- B) Backup & Restore with automatic snapshots to S3
- C) Warm Standby with reduced capacity in a second region
- D) Pilot Light with minimum components in a second region

<details><summary>Answer</summary>

**D** — Pilot Light: keeps only essential components (replicated DB, ready AMIs) running in the second region at minimal state. RTO of 10-15 min (provision the rest) at much lower cost than Warm Standby. RPO depends on replication frequency; with Aurora Global DB or DMS CDC, RPO < 1h is feasible.

</details>

---

**3.** A company has a critical endpoint. When the primary region becomes unavailable, traffic must be automatically routed to a second region. Which service implements this?
- A) AWS Global Accelerator with endpoint groups
- B) Amazon Route 53 with Failover routing
- C) Amazon CloudFront with origin failover
- D) A and B are both valid

<details><summary>Answer</summary>

**D** — Route 53 Failover routing monitors health checks and automatically switches DNS to the secondary endpoint. Global Accelerator also does automatic failover between regions via anycast. Both are valid; Route 53 acts at DNS level, Global Accelerator acts at network level (lower failover latency).

</details>

---

**4.** An SQS queue is receiving high-priority messages mixed with low-priority messages. High-priority messages need to be processed immediately. What should be done?
- A) Configure message attributes and filter at the consumer
- B) Create two separate SQS queues and route messages by priority
- C) Use SQS FIFO to ensure processing order
- D) Use SNS Message Filtering to separate messages

<details><summary>Answer</summary>

**B** — SQS has no native message priority support. The solution is to create separate queues (high and low priority) and have workers that check the high-priority queue first. SQS FIFO guarantees order but not priority between messages.

</details>

---

**5.** A company needs a system that guarantees each message is processed exactly once, even with consumer restarts. Which AWS queue to use?
- A) Amazon SQS Standard
- B) Amazon SQS FIFO with deduplication ID
- C) Amazon SNS FIFO
- D) Amazon Kinesis Data Streams

<details><summary>Answer</summary>

**B** — SQS FIFO with Message Deduplication ID guarantees exactly-once delivery (exactly-once processing). SQS Standard guarantees at-least-once delivery (duplicates possible). Kinesis can have at-least-once delivery depending on consumer configuration.

</details>

---

**6.** A web application uses ALB + Auto Scaling Group + RDS Aurora. During peaks, the database becomes overloaded with reads. The most cost-effective solution to scale reads is:
- A) Increase the primary RDS instance class
- B) Add Aurora Read Replicas and configure the application connection string to the Reader endpoint
- C) Implement ElastiCache Redis as session cache
- D) Migrate to DynamoDB with DAX

<details><summary>Answer</summary>

**B** — Aurora Read Replicas scale reads horizontally with minimal latency; the Reader Endpoint distributes automatically across replicas. It is more economical and direct than other options for existing SQL read workloads.

</details>

---

**7.** A company wants to ensure its critical Lambda functions always have available capacity without cold start. Which configuration implements this?
- A) Reserved Concurrency with a high value
- B) Provisioned Concurrency on a Lambda version or alias
- C) Increase allocated Lambda memory to 10 GB
- D) Configure Lambda in VPC to reduce cold starts

<details><summary>Answer</summary>

**B** — Provisioned Concurrency pre-warms N execution environments, completely eliminating cold start for those N concurrents. Reserved Concurrency guarantees capacity but does not eliminate cold start. VPC does not help with cold start (Hyperplane ENI since 2019 minimized this effect).

</details>

---

**8.** An EC2 instance fails and needs to be automatically replaced with the same private IP address and data storage. Which solution implements this?
- A) Auto Scaling Group with min/max/desired = 1
- B) EC2 Instance Recovery via CloudWatch Alarm
- C) Automatic AMI + CloudFormation
- D) EC2 Instance with Placement Group

<details><summary>Answer</summary>

**B** — EC2 Instance Recovery (alarm action "Recover Instance") moves the instance to new hardware keeping the same private IP, Elastic IP, instance ID, and EBS data. ASG creates a new instance with new IPs.

</details>

---

**9.** A company must ensure that critical S3 objects are automatically replicated to another region, and that metadata and versions are also replicated. What should be configured?
- A) S3 Transfer Acceleration
- B) S3 Cross-Region Replication (CRR) with versioning enabled on both buckets
- C) S3 Same-Region Replication (SRR) with Lambda
- D) S3 Event → Lambda → CopyObject to another bucket

<details><summary>Answer</summary>

**B** — CRR requires versioning enabled on both buckets (source and destination). It automatically replicates new objects and versions to the destination region. SRR is within the same region.

</details>

---

**10.** An application uses DynamoDB and starts receiving `ProvisionedThroughputExceededException` errors. The company wants to scale automatically without manually managing RCU/WCU. What should be implemented?
- A) Manually increase provisioned RCU/WCU
- B) Migrate to DynamoDB On-Demand mode
- C) Add DAX in front of DynamoDB
- D) Migrate to RDS to support more capacity

<details><summary>Answer</summary>

**B** — On-Demand mode scales automatically based on traffic; there is no throttling due to provisioned capacity. DynamoDB Auto Scaling (with provisioned mode) also works but has response delay. On-Demand has per-request cost (more expensive for high predictable load, ideal for variable/unpredictable load).

</details>

---

**11.** A company has an S3 bucket with sensitive data and needs to ensure that no object is accidentally deleted for 7 years. Which configuration implements this?
- A) S3 Versioning + MFA Delete
- B) S3 Object Lock in Compliance mode with 7-year retention period
- C) S3 Glacier Vault Lock with retention policy
- D) S3 Bucket Policy denying DeleteObject

<details><summary>Answer</summary>

**B** — S3 Object Lock in Compliance mode: **not even the root account** can delete or modify objects during the retention period. Perfect for WORM compliance. Governance mode allows specially permissioned admins to override. Bucket Policy can be changed by admin; MFA Delete does not prevent all deletion types.

</details>

---

**12.** A microservices application on ECS needs each container to access a database secret stored in AWS Secrets Manager. What is the most secure way to provide the secret to the container?
- A) Pass the secret as an environment variable in the task definition
- B) Use native ECS + Secrets Manager integration in the task definition with the `secrets` field
- C) Store the secret in encrypted S3 and have Lambda fetch it before the container starts
- D) Embed the secret in the container image

<details><summary>Answer</summary>

**B** — ECS supports injecting secrets from Secrets Manager and Parameter Store directly into environment variables or as volumes — the ECS agent fetches the value at runtime. The secret is never exposed in the image or task definition in plain text. The task execution role needs permission for `secretsmanager:GetSecretValue`.

</details>

---

**13.** An analytics solution processes large 10 GB CSV files in S3. Athena queries are slow and expensive. Which single-action improvement would have the most impact?
- A) Convert files to Parquet and partition by date
- B) Move to Redshift for faster queries
- C) Increase block size in S3
- D) Use S3 Select to filter before sending to Athena

<details><summary>Answer</summary>

**A** — Parquet is a compressed columnar format: Athena reads only the needed columns and scans far less data. Date partitioning avoids full table scans. Combined, they can reduce query cost and time by 90%+. This is the most impactful optimization for Athena.

</details>

---

**14.** A company needs Lambda and ECS container logs centralized, with 90-day retention and analytical query capability. Which solution should be implemented?
- A) Kinesis Firehose → S3 → Athena
- B) CloudWatch Logs with log groups, 90-day retention, and CloudWatch Logs Insights
- C) Elasticsearch (OpenSearch) with log agent
- D) CloudWatch Logs Subscription → Kinesis Firehose → S3 + Athena

<details><summary>Answer</summary>

**B** — Lambda and ECS automatically send logs to CloudWatch Logs. Configure 90-day retention per group. CloudWatch Logs Insights allows analytical queries on the logs directly. Simplest and most cost-effective solution for the described case.

</details>

---

**15.** An EC2 instance in a private subnet needs to make calls to an external API on the internet without exposing its private IP. What should be configured?
- A) Add an Elastic IP to the instance
- B) Create a NAT Gateway in a public subnet and add route 0.0.0.0/0 to the private subnet's route table
- C) Configure VPC Peering with a public VPC
- D) Enable DNS resolution on the VPC

<details><summary>Answer</summary>

**B** — NAT Gateway in a public subnet (with IGW) allows instances in private subnets to initiate connections to the internet. The NAT translates the private IP to the NAT Gateway's IP. Elastic IP on the private instance doesn't work without IGW in the route table.

</details>

---

**16.** A company wants to ensure that only SigV4-signed requests can access its S3 bucket. Which policy should be applied to the bucket?
- A) Bucket Policy with `"Effect": "Deny"` for `"Principal": "*"` with condition on `aws:SecureTransport`
- B) Bucket Policy with Condition `"StringEquals": {"s3:authType": "REST-QUERY-STRING"}`
- C) Bucket ACL configuring private access
- D) Amazon Macie to monitor unauthorized access

<details><summary>Answer</summary>

**A** — The correct condition is `"Condition": {"Bool": {"aws:SecureTransport": "false"}}` with Deny to force HTTPS. To force SigV4 (AWS authentication), remove public access + have IAM policies only for AWS identities. Amazon Macie is detection, not access control.

</details>

---

**17.** A company uses AWS Organizations with multiple accounts. It needs to prevent developers in member accounts from creating resources in unapproved regions. Which service should be implemented?
- A) IAM Permission Boundaries in each member account
- B) Service Control Policy (SCP) at the Organizations OU applying Deny for unapproved regions
- C) AWS Config Rules in each member account
- D) IAM Role with region condition in each member account

<details><summary>Answer</summary>

**B** — SCPs are applied at the OU or account level in Organizations and limit what any identity (even root) can do in member accounts. An SCP `Deny + Condition: aws:RequestedRegion NotEquals [us-east-1, us-west-2]` blocks all actions in unlisted regions.

</details>

---

### Section B — Performance (Questions 18-33) — Quick Reference

| # | Area | Expected Answer |
|---|---|---|
| 18 | EC2 high compute workload | C5/C6i, placement group cluster |
| 19 | Low latency inter-service same AZ | Placement Group Cluster |
| 20 | High IOPS for database | EBS io2 Block Express |
| 21 | Global static content low latency | CloudFront |
| 22 | TCP/UDP global acceleration | Global Accelerator |
| 23 | In-memory cache for repeated reads | ElastiCache Redis |
| 24 | DynamoDB microsecond reads | DAX (DynamoDB Accelerator) |
| 25 | ECS tasks internal communication | Service Connect or Service Discovery (Cloud Map) |
| 26 | Lambda with large Python dependency | Lambda Container Image (up to 10 GB) |
| 27 | S3 queries without moving data | Amazon Athena |
| 28 | Optimized large file S3 upload | Multipart Upload + Transfer Acceleration |
| 29 | EFS high performance (HPC) | EFS Max I/O or FSx for Lustre |
| 30 | Redshift slow queries with concurrent users | Concurrency Scaling |
| 31 | API GW throttling to protect backend | Usage Plans + Rate Limits |
| 32 | Graviton instances | Best price/performance for Cloud-native workloads |
| 33 | Critical Java Lambda cold start | SnapStart (Java 11+) or Provisioned Concurrency |

---

### Section C — Security (Questions 34-54) — Quick Reference

| # | Area | Expected Answer |
|---|---|---|
| 34 | Detect compromised instances | GuardDuty |
| 35 | Detect sensitive data in S3 | Macie |
| 36 | EC2/Lambda vulnerability scanning | Inspector |
| 37 | Cross-account role | sts:AssumeRole with trust policy |
| 38 | Automatic RDS secret rotation | Secrets Manager with rotation Lambda |
| 39 | DynamoDB data encryption at rest | AWS KMS CMK (Customer Managed Key) |
| 40 | Block SQL injection on API | WAF with AWS Managed Rules |
| 41 | EC2 access without key pair | SSM Session Manager |
| 42 | S3 bucket policy vs IAM policy | S3 Bucket Policy for cross-account; IAM for same-account |
| 43 | CloudFront + S3 — prevent direct S3 access | Origin Access Control (OAC) |
| 44 | PCI DSS compliance on AWS | Shared Responsibility + AWS Artifact (reports) |
| 45 | Encrypt existing EBS volume | Snapshot → Encrypted Copy → Restore |
| 46 | Audit which APIs were called | CloudTrail (Management Events) |
| 47 | Multitenancy — isolate data by tenant | DynamoDB with partition key per tenant + Resource Policy |
| 48 | EKS pod permissions | IRSA (IAM Roles for Service Accounts) |
| 49 | Automatic key rotation | KMS Key Rotation annual (AWS Managed Keys auto; CMK configurable) |
| 50 | VPC endpoint S3 without internet | Gateway VPC Endpoint for S3 (free) |
| 51 | S3 access logs | S3 Server Access Logging or CloudTrail Data Events |
| 52 | Prevent accidental CloudFormation deletion | Termination Protection + DeletionPolicy: Retain |
| 53 | ACM certificate renewal | Automatic for ACM-provisioned certificates |
| 54 | Network Firewall vs WAF | Network Firewall = Layer 4 (VPC level); WAF = Layer 7 (HTTP) |

---

### Section D — Cost (Questions 55-65) — Quick Reference

| # | Area | Expected Answer |
|---|---|---|
| 55 | Non-prod instances outside business hours | EventBridge event → Lambda → Stop/Start EC2 |
| 56 | Interruption-tolerant batch workload | Spot Instances |
| 57 | Known long-term commitment | Reserved Instances or Savings Plans |
| 58 | EC2 rightsizing | Compute Optimizer |
| 59 | S3 unpredictable access | S3 Intelligent-Tiering |
| 60 | Data transfer — zero cost | Data to EC2 in same region is free; egress has cost |
| 61 | Redshift vs Athena — when to use | Athena for ad-hoc; Redshift for recurring analytical DW |
| 62 | EFS vs EBS cost | EBS cheaper but single-instance; EFS multi-instance but more expensive/GB |
| 63 | Lambda vs EC2 for sporadic workload | Lambda more economical (pay per invocation, no idle cost) |
| 64 | NAT GW cost | ~$0.045/hour + $0.045/GB processed; use VPC Endpoint for S3/DynamoDB (free) |
| 65 | Multi-AZ RDS cost | ~2x Single-AZ cost; necessary for HA; don't skimp on this in production |

---

## Summary Answer Key — Practice Exam 1

| Q | A | Q | A | Q | A | Q | A | Q | A |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 14 | B | 27 | Athena | 40 | WAF | 53 | Automatic |
| 2 | D | 15 | B | 28 | Multipart | 41 | SSM | 54 | Net FW |
| 3 | D | 16 | A | 29 | FSx Lustre | 42 | Bucket Policy | 55 | EventBridge |
| 4 | B | 17 | B | 30 | Concurrency | 43 | OAC | 56 | Spot |
| 5 | B | 18 | C5/C6i | 31 | Usage Plans | 44 | Artifact | 57 | RI/SP |
| 6 | B | 19 | Cluster PG | 32 | Graviton | 45 | Snapshot | 58 | Optimizer |
| 7 | B | 20 | io2 | 33 | SnapStart | 46 | CloudTrail | 59 | Int-Tiering |
| 8 | B | 21 | CloudFront | 34 | GuardDuty | 47 | Partition key | 60 | Free |
| 9 | B | 22 | Global Acc | 35 | Macie | 48 | IRSA | 61 | Redshift DW |
| 10 | B | 23 | ElastiCache | 36 | Inspector | 49 | KMS Rotation | 62 | EBS cheaper |
| 11 | B | 24 | DAX | 37 | AssumeRole | 50 | GW Endpoint | 63 | Lambda |
| 12 | B | 25 | Service Conn | 38 | Secrets Mgr | 51 | S3 Logging | 64 | VPC Endpoint |
| 13 | A | 26 | Container | 39 | CMK | 52 | Termination P | 65 | Multi-AZ prod |
