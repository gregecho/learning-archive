# Flashcards — Module 20: Glossary

> **Format:** Q = Question | A = Answer  
> **Total:** 30 flashcards — definitions of AWS terms and acronyms

---

**Q:** What does SLA mean in the AWS context?  
**A:** **Service Level Agreement** — service level agreement that defines the guaranteed uptime of an AWS service. Ex: EC2 SLA = 99.99% per region. If AWS does not meet it, customers receive service credits. SLA is different from SLO (Service Level Objective — internal target) and SLI (Service Level Indicator — actual metric).

---

**Q:** What is a CDN and how does CloudFront implement it?  
**A:** **Content Delivery Network** — globally distributed network of servers that caches content close to users. CloudFront: 500+ Points of Presence (PoPs) in 90+ cities. Reduces latency (user accesses local PoP vs distant server), reduces origin load, cached responses for static content.

---

**Q:** What is Idempotency and why is it important in APIs and queues?  
**A:** **Idempotency:** executing the same operation multiple times produces the same result. Ex: `DELETE /order/123` executed 3 times = identical result to executing 1 time. Important in: queue systems (SQS at-least-once delivery, can re-deliver), HTTP retries, payments (avoid duplicate charges). Design: use unique transaction IDs, check-before-write.

---

**Q:** What is throughput vs latency?  
**A:** **Throughput:** amount of data processed per unit of time (GB/s, requests/s). **Latency:** time to process a single operation (ms, us). They can be inversely related: processing more items in batch increases throughput but may increase individual latency. In the exam: "lots of data" → throughput; "fast response for user" → latency.

---

**Q:** What is an SQS Message Visibility Timeout?  
**A:** After a consumer picks up a message from SQS, it becomes **invisible** in the queue for `VisibilityTimeout` (default: 30s, max: 12h). If the consumer processes successfully and deletes the message: permanently removed. If the consumer fails/times out: the message becomes visible again for other consumers. Prevents double processing.

---

**Q:** What is a NAT Gateway and why do private instances need it?  
**A:** **Network Address Translation Gateway** — allows instances in private subnets (without public IP) to access the internet for outbound connections (updates, external APIs), but the internet cannot initiate connections to them. NAT GW sits in the public subnet with an Elastic IP. Private subnet route: `0.0.0.0/0 → NAT GW`. Managed, scalable, highly available per AZ.

---

**Q:** What is CIDR Notation?  
**A:** **Classless Inter-Domain Routing** — notation for IP addressing. Ex: `10.0.0.0/16` = 65,536 IPs (10.0.0.0 to 10.0.255.255). The `/16` = 16 fixed bits (prefix), 16 variable bits. `/24` = 256 IPs. The smaller the number after `/`, the larger the block. AWS VPC: `/16` max, `/28` min (11 usable IPs — AWS reserves 5).

---

**Q:** What is a Bastion Host and what is the modern alternative?  
**A:** **Bastion Host (Jump Box):** EC2 in public subnet with SSH port open. Access: SSH to bastion → SSH to private instances. Problem: attack surface (exposed SSH). **Modern alternative:** AWS Systems Manager Session Manager — no open port 22, no bastion, auditable, works in private subnets without internet.

---

**Q:** What is the "pay-as-you-go" pricing model on AWS?  
**A:** **Pay for actual usage**, with no minimum commitment (for On-Demand services). No setup fee. No mandatory long-term contracts. Opposite of on-premises: no need to buy hardware for peak capacity. On AWS: EC2 On-Demand billed per second; Lambda per millisecond; S3 per GB/month; RDS per hour.

---

**Q:** What is a Managed Service on AWS and what is its benefit?  
**A:** A service where AWS manages the underlying infrastructure: patches, hardware, HA, backups. Ex: RDS (AWS manages OS, MySQL patches, backups), Lambda (AWS manages runtime, scaling), DynamoDB (AWS manages storage, replication). You are responsible for: configuration, data, IAM. Reduces operational overhead.

---

**Q:** What is an Elastic IP Address?  
**A:** **Persistent static public IP** in your AWS account. Unlike the EC2 public IP that changes on every restart, the Elastic IP persists. It is associated with an EC2 instance or NAT Gateway. Free while associated with a running instance; charged ($0.005/hr) when not associated (to prevent waste). Maximum 5 EIPs per account by default.

---

**Q:** What is DNS (Domain Name System) in the AWS context?  
**A:** Service that translates domain names (`www.example.com`) to IP addresses. AWS: **Route 53** is the managed DNS service. Record types: **A** (name → IPv4), **AAAA** (name → IPv6), **CNAME** (name → another name), **Alias** (Route 53 specific, points to AWS resources — ELB, CloudFront, S3 Website).

---

**Q:** What is edge computing in the AWS context?  
**A:** Data processing **close to the source** (devices, users) instead of in a central data center. AWS edge: CloudFront PoPs (cache + Lambda@Edge), AWS Outposts (AWS hardware in customer data center), Snow Family (Snowball Edge — compute in the field), IoT Greengrass (Lambda on IoT devices), Wavelength (inside telco 5G network).

---

**Q:** What is TLS/SSL and how does AWS implement it?  
**A:** **Transport Layer Security** — encryption protocol for secure communication over the internet (HTTPS). AWS: **ACM (AWS Certificate Manager)** provisions, manages, and automatically renews TLS certificates for: CloudFront, ALB, API Gateway. TLS termination: CloudFront or ALB decrypts and re-encrypts (or passes to backend). Free via ACM.

---

**Q:** What is eventual consistency vs strong consistency?  
**A:** **Strong Consistency:** read always returns the most recent data after write. **Eventual Consistency:** read may temporarily return old data, but eventually converges to the current state. AWS: S3 default = strong consistency (since 2020). DynamoDB: **Eventually Consistent Reads** (default, 2x more efficient capacity units) and **Strongly Consistent Reads** (available, uses more RCUs).

---

**Q:** What is an Availability Zone (AZ)?  
**A:** Physically separate data center(s) within an AWS region, with independent power, network, and cooling. Connection between AZs: low-latency private network (<1ms). Each AZ has a unique real ID (e.g., `use1-az1`), but names (`us-east-1a`) vary by account (random mapping). Failure in one AZ should not affect others. Multi-AZ = HA against AZ failure.

---

**Q:** What is the principle of Least Privilege?  
**A:** Giving each identity (user, role, service) **only the permissions needed** for the job and nothing more. Reduces blast radius: if credential is compromised, attacker has minimal access. On AWS: specific IAM policies (not `*`), Resource-based policies, SCPs to limit accounts. Best practice: start with zero permissions and add as needed.

---

**Q:** What is Infrastructure as Code (IaC)?  
**A:** Managing and provisioning infrastructure via code (declarative or imperative) instead of manually in the console. Benefits: reproducible, versionable (Git), auditable, testable, automatic documentation. AWS native: **CloudFormation** (declarative YAML/JSON). Multi-cloud: **Terraform** (HCL). CDK: Python/TypeScript code that generates CloudFormation. GitOps: IaC + Git as source of truth.

---

**Q:** What is a Service Mesh and how does AWS implement it?  
**A:** Dedicated infrastructure for communication between microservices (service discovery, load balancing, circuit breaking, observability, mTLS). AWS: **AWS App Mesh** (based on Envoy proxy, integrated with ECS/EKS), **Amazon VPC Lattice** (simpler managed service-to-service networking). Solves: how services find and communicate with each other securely and observably.

---

**Q:** What is Object Storage vs Block Storage vs File Storage?  
**A:** **Object Storage (S3):** files with metadata and unique ID, accessed via HTTP API, virtually unlimited scale, cannot be mounted as filesystem. **Block Storage (EBS):** low-level volumes (like HD), mounted on EC2, high performance, configurable IOPS, ideal for databases. **File Storage (EFS, FSx):** shared filesystem NFS/SMB, multiple instances access simultaneously.

---

**Q:** What is the AWS Savings Plans pricing model?  
**A:** Minimum spend commitment per hour (e.g., $10/hr for 1 or 3 years), in exchange for a discount. **Compute Savings Plans:** more flexible — applies to EC2 (any type/region/OS), Fargate, and Lambda. **EC2 Instance Savings Plans:** less flexible (specific family + region), higher discount (up to 72%). Different from Reserved Instances: does not reserve specific capacity.

---

**Q:** What is a CloudFormation Stack vs StackSet?  
**A:** **Stack:** set of AWS resources created/managed as a unit by CloudFormation in a single account/region. **StackSet:** deploys Stacks to **multiple accounts and regions** simultaneously. Requires cross-account permissions (IAM Roles). Use StackSets for: organization-wide security baseline, GuardDuty in all accounts, global AWS Config rules.

---

**Q:** What is the AWS Free Tier and what are its 3 types?  
**A:** **(1) Always Free:** never expires. Ex: Lambda 1M req/month, DynamoDB 25 GB, CloudFront 1 TB, SNS 1M req. **(2) 12-Month Free:** after creating an account, 12 months of limited usage. Ex: EC2 t2.micro/t3.micro 750h/month, S3 5 GB, RDS db.t2.micro 750h/month. **(3) Trials:** trial periods for specific services. Free Tier does not cover all resources — check limits.

---

**Q:** What is a Tag on AWS resources and how does it contribute to Cost Allocation?  
**A:** **Tags:** key-value pairs applied to AWS resources. Examples: `Environment:prod`, `Project:phoenix`, `CostCenter:123`. **Cost Allocation Tags:** activated in the Billing Console, appear in Cost Explorer allowing filtering and grouping costs by tag. Best practices: tag all resources, automation via CloudFormation/Terraform, SCP that requires mandatory tags.

---

**Q:** What is Multi-Factor Authentication (MFA) on AWS?  
**A:** Second authentication factor beyond password. AWS supports: **Virtual MFA** (apps like Google Authenticator, Authy — TOTP), **Hardware MFA** (physical TOTP or FIDO2 device — YubiKey), **SMS MFA** (deprecated for IAM). Required for: root account protection, critical actions (S3 MFA Delete, IAM delete with MFA condition). IAM best practice: MFA on all users with console access.

---

**Q:** What is the concept of "Shared Responsibility Model" with an S3 example?  
**A:** In S3: **AWS:** physical infrastructure, S3 server hardware, network, durability (11 nines), internal object replication. **Client:** bucket policy configuration, Block Public Access settings, object encryption (SSE-S3/KMS), access control (IAM policies), versioning, cross-region replication. What happens TO the data is the client's responsibility.

---

**Q:** What is the Amazon Resource Name (ARN) of a Lambda Function?  
**A:** Full format: `arn:aws:lambda:us-east-1:123456789012:function:MyFunction`. Components: `arn` (prefix) : `aws` (partition) : `lambda` (service) : `us-east-1` (region) : `123456789012` (account ID) : `function` (resource type) : `MyFunction` (resource name). For alias: `:MyFunction:PROD`. For version: `:MyFunction:1`.

---

**Q:** What is an "endpoint" on AWS?  
**A:** Can mean: **(1) VPC Endpoint:** private connection between VPC and AWS service. **(2) SageMaker Endpoint:** inference instance serving an ML model. **(3) API Endpoint:** URL of an API (e.g., `https://abc123.execute-api.us-east-1.amazonaws.com/prod/users`). **(4) DynamoDB Endpoint:** regional endpoint for accessing DynamoDB without internet (VPC endpoint). Context determines the meaning.

---

**Q:** What is durability vs availability in S3?  
**A:** **Durability:** probability of not losing data. S3 Standard = **11 nines** (99.999999999%) — for 10 million objects, losing one every 10,000 years. Stores data in 3 AZs. **Availability:** fraction of time the service is accessible. S3 Standard = 99.99%/year. S3 One Zone-IA: durability 11 nines (but in 1 AZ), availability 99.5%. Durability != availability.

---

**Q:** What is a security finding and how does AWS consolidate them?  
**A:** **Finding:** a record of a potential security issue detected. Generated by: GuardDuty (threats), Inspector (EC2/ECR/Lambda vulnerabilities), Macie (sensitive data in S3), Config (non-compliance), IAM Access Analyzer (excessive permissions). **AWS Security Hub** consolidates all findings into a centralized dashboard, normalized to the AWS Security Finding Format (ASFF).
