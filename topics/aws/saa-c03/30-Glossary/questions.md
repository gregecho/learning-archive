# Questions — Module 20: Glossary

> **Definitions Quiz** — Test your knowledge of AWS terms  
> **Difficulty**: Basic-Medium

---

**1.** What is an ARN (Amazon Resource Name) and what is its format?

- A) AWS region identifier. Format: `aws:region:name`
- B) Unique identifier for any AWS resource. Format: `arn:aws:service:region:account-id:resource`
- C) Automatic name assigned to EC2 instances. Format: `ec2-ip-address.region.compute.internal`
- D) IAM user identifier. Format: `iam::user:name`

<details><summary>Answer</summary>

**B** — ARN uniquely identifies any AWS resource. Example: `arn:aws:s3:::my-bucket`, `arn:aws:ec2:us-east-1:123456:instance/i-xxx`, `arn:aws:iam::123456:role/my-role`. Used in IAM policies, resource policies, and APIs to reference specific resources.

</details>

---

**2.** What is the difference between RTO and RPO in Disaster Recovery strategies?

- A) RTO = how much data can be lost; RPO = how long the system can be offline
- B) RTO = maximum acceptable downtime; RPO = maximum amount of data that can be lost
- C) RTO and RPO are synonyms for "Recovery Time"
- D) RTO is for databases; RPO is for applications

<details><summary>Answer</summary>

**B** — RTO (Recovery Time Objective): how long can I take to restore the service? → defines the DR strategy (lower RTO = more expensive strategy). RPO (Recovery Point Objective): how much data can I lose? → defines backup/replication frequency. For example: RTO 1h, RPO 15 min = max 1h offline + max 15 min of lost data.

</details>

---

**3.** What does IOPS mean in the context of AWS storage?

- A) Internet Operations Per Second — download speed
- B) Input/Output Operations Per Second — storage read/write performance measurement
- C) Instance Operations Per Second — EC2 throughput
- D) Infrastructure Operations Per Service — SLA metric

<details><summary>Answer</summary>

**B** — IOPS = Input/Output Operations Per Second. The more IOPS, the more read/write operations per second the storage supports. EBS gp3 baseline = 3,000 IOPS; io2 Block Express = up to 256,000 IOPS. Relevant for databases that need many I/O operations per second.

</details>

---

**4.** What is the difference between a Security Group and a NACL in VPC?

- A) Security Group: subnet level (stateless); NACL: instance level (stateful)
- B) Security Group: instance/ENI level (stateful, Allow only); NACL: subnet level (stateless, Allow and Deny)
- C) They are equivalent features; Security Group is the AWS term and NACL is the market standard
- D) NACL is for IPv4; Security Group is for IPv6

<details><summary>Answer</summary>

**B** — SG: ENI (instance) level, stateful (automatic return allowed), Allow-only rules, references other SGs. NACL: subnet level, stateless (must explicitly allow outbound as well), has numbered Allow and Deny rules evaluated in order.

</details>

---

**5.** What is WORM in the context of S3 Object Lock?

- A) Write Once Read Many — written data cannot be modified or deleted during the retention period
- B) Write Once Replicate Many — objects are automatically replicated
- C) Web Object Routing Mechanism — how objects are routed via CloudFront
- D) Workload Object Retention Method — S3 lifecycle policy

<details><summary>Answer</summary>

**A** — WORM = Write Once Read Many. S3 Object Lock Compliance mode: once written, the object cannot be deleted or overwritten by anyone (not even the root account) during the retention period. Ideal for: financial regulations, auditing, compliance, forensic evidence.

</details>

---

**6.** What is a VPC Endpoint and what are the two types?

- A) DNS endpoint to resolve names in a VPC. Types: Route 53 Inbound and Outbound
- B) Private connection between VPC and AWS services without going to the internet. Types: Gateway (S3, DynamoDB) and Interface (PrivateLink for other services)
- C) Fixed public IP for services within a VPC. Types: Elastic IP and NAT Gateway
- D) VPN access point. Types: Site-to-Site and Client VPN

<details><summary>Answer</summary>

**B** — VPC Endpoint: access to AWS services without internet (traffic stays on the private AWS network). Gateway Endpoint: free, for S3 and DynamoDB, added to the route table. Interface Endpoint (PrivateLink): paid (~$0.01/hour + data), creates ENI in the VPC, supports 150+ AWS services and private third-party services.

</details>

---

**7.** What does "stateful" mean in a Security Group?

- A) The Security Group keeps logs of all connections
- B) The return traffic of an allowed connection is automatically permitted without an explicit outbound rule
- C) The Security Group maintains history of all applied rules
- D) Only connections with ESTABLISHED state are allowed

<details><summary>Answer</summary>

**B** — Stateful: the Security Group tracks connection state. If you allow inbound traffic on port 443 (HTTPS), the return traffic (outbound response) is automatically allowed without needing an outbound rule. Unlike NACL (stateless), where you need explicit rules for both inbound AND outbound.

</details>

---

**8.** What is DAX and which service is it specific to?

- A) AWS Data Aggregation Exchange — multi-account consolidation tool
- B) DynamoDB Accelerator — in-memory cache specific to DynamoDB with microsecond latency
- C) Direct Access eXchange — protocol for Direct Connect
- D) Data Analytics eXecutor — serverless analytics engine

<details><summary>Answer</summary>

**B** — DAX = DynamoDB Accelerator: managed in-memory cache compatible with the DynamoDB API. No application code changes (drop-in replacement). Reads: from milliseconds to microseconds. Ideal for: very frequent reads of the same items (hot items), gaming leaderboards, user sessions.

</details>

---

**9.** What is an IAM Role and how does it differ from an IAM User?

- A) Role is for AWS services; User is for humans. Role has no permanent credentials (uses temporary STS credentials)
- B) Role is more secure than User because it has more permissions
- C) User is more modern than Role and should be used in new projects
- D) Role and User are identical; the difference is only in the console

<details><summary>Answer</summary>

**A** — IAM Role: identity without permanent credentials; assumed temporarily (STS AssumeRole → short-lived credentials). For: AWS services (EC2, Lambda), federated users (SSO), cross-account access. IAM User: has permanent credentials (password + access keys). Best practices: use Roles whenever possible, avoid access keys for humans.

</details>

---

**10.** What is SPICE in Amazon QuickSight?

- A) Security Protocol for Intelligence and Cloud Events — security protocol
- B) Super-fast Parallel In-memory Calculation Engine — QuickSight in-memory cache mechanism
- C) Standard Protocol for Inter-Cloud Exchange
- D) Scalable Processing of Intelligent Content Engine

<details><summary>Answer</summary>

**B** — SPICE: QuickSight in-memory cache. Data imported into SPICE stays in memory for ultra-fast dashboards (independent of real-time queries to the database or S3). Each QuickSight user has a SPICE quota (GB). Scheduled or manual refresh updates SPICE data.

</details>

---

**11.** What differentiates CRR from SRR in Amazon S3?

- A) CRR = automatic replication between regions; SRR = replication in the same region. Both require versioning enabled on the source bucket
- B) CRR = large object backup; SRR = metadata backup
- C) SRR is cheaper than CRR; CRR has lower latency
- D) CRR is for objects < 5 GB; SRR for larger objects

<details><summary>Answer</summary>

**A** — CRR (Cross-Region Replication): replicates objects to a bucket in another region (DR, compliance, global latency). SRR (Same-Region Replication): replicates to a bucket in the same region (log aggregation, copy compliance, testing without affecting production). Both: versioning required, replicate only new objects (not retroactive), support prefix/tag filters.

</details>

---

**12.** What does "serverless" mean in the AWS context?

- A) The application does not use servers — runs directly on hardware
- B) AWS manages all server infrastructure; you only define code/configuration and pay for actual usage
- C) Servers are virtual (like EC2) without dedicated hardware
- D) The application does not need code — it is configured declaratively

<details><summary>Answer</summary>

**B** — Serverless: no server provisioning or management by the user. AWS manages: instances, patches, scalability, HA. You define only: code (Lambda), tables (DynamoDB), queries (Athena), configuration (S3). Pay for actual consumption (invocations, GB processed, objects). Examples: Lambda, Fargate, DynamoDB, S3, Athena, API Gateway.

</details>

---

**13.** What is the "fan-out" architecture pattern on AWS?

- A) Scaling horizontally by adding more servers
- B) Sending one message to multiple consumers in parallel using SNS → multiple SQS queues
- C) Distributing traffic among multiple instances using a Load Balancer
- D) Replicating data to multiple regions

<details><summary>Answer</summary>

**B** — Fan-out: one message published to an SNS topic is delivered simultaneously to multiple subscribers (SQS queues, Lambda functions, HTTP endpoints). Each subscriber processes independently. Example: one order_created goes to: email queue, analytics queue, fulfillment queue, audit queue — all in parallel.

</details>

---

**14.** What is a Cluster Placement Group in EC2?

- A) Group of instances distributed across different racks for high availability
- B) Group of instances on the same physical rack/hardware for maximum network performance (low latency, high bandwidth between instances)
- C) Group of instances reserved in advance
- D) Set of Spot instances with consistent pricing

<details><summary>Answer</summary>

**B** — Cluster Placement Group: instances very close physically (same rack/hardware). Result: ultra-low network latency and up to 100 Gbps throughput between instances. Sacrifices availability (rack failure affects all). Use for: HPC, MPI applications, intensive computing, simulations. Contrast: Spread PG (maximum HA, instances on separate racks).

</details>

---

**15.** What is the AWS Shared Responsibility Model?

- A) AWS is responsible for all cloud security; the client has no responsibilities
- B) AWS is responsible for security OF the cloud (infrastructure); the client is responsible for security IN the cloud (data, IAM, OS configuration, application)
- C) Responsibility is equal between AWS and client in all areas
- D) The client is responsible for security only in production environments

<details><summary>Answer</summary>

**B** — AWS: hardware, data centers, physical network, hypervisor, managed services. Client: IAM (who can access), SG/NACL configuration, data encryption (at rest and in transit), OS patches on EC2, application code, compliance settings. In managed services (RDS, Lambda), the client has fewer infrastructure responsibilities.

</details>
