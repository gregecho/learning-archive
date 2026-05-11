# Cheatsheet — AWS Glossary (Module 20)

## Acronyms and Abbreviations — Quick Reference

| Acronym | Meaning | Context |
|-------|-------------|---------|
| **ACL** | Access Control List | S3 object/bucket access; NACL in VPC |
| **ACM** | AWS Certificate Manager | Free TLS/SSL certificates |
| **AMI** | Amazon Machine Image | Template for EC2 instances |
| **ARN** | Amazon Resource Name | Unique identifier for AWS resources |
| **ASG** | Auto Scaling Group | EC2 group with automatic scaling |
| **AZ** | Availability Zone | Isolated data center(s) within a Region |
| **BAA** | Business Associate Agreement | Contract for HIPAA/health data |
| **BYOL** | Bring Your Own License | Use your own license on EC2 Dedicated |
| **CDN** | Content Delivery Network | CloudFront distributes content globally |
| **CIDR** | Classless Inter-Domain Routing | IP block notation (e.g., 10.0.0.0/16) |
| **CMK** | Customer Managed Key | KMS key managed by the customer |
| **CORS** | Cross-Origin Resource Sharing | S3/API GW policy for cross-domain access |
| **CRR** | Cross-Region Replication | S3 replication between regions |
| **DAX** | DynamoDB Accelerator | In-memory cache for DynamoDB |
| **DNSSEC** | DNS Security Extensions | Verification of DNS record authenticity |
| **EBS** | Elastic Block Store | Disk volume for EC2 |
| **EC2** | Elastic Compute Cloud | Virtual machine service |
| **ECS** | Elastic Container Service | Container orchestrator |
| **EFS** | Elastic File System | Managed NFS file system |
| **EIP** | Elastic IP | Static public IP for EC2/NAT GW |
| **EKS** | Elastic Kubernetes Service | Managed Kubernetes |
| **EMR** | Elastic MapReduce | Big data processing (Spark/Hadoop) |
| **ETL** | Extract, Transform, Load | Data pipeline (AWS Glue) |
| **FSx** | Amazon FSx | Managed file systems (Windows, Lustre) |
| **GS** | General Purpose SSD | EBS type — gp2/gp3 |
| **HA** | High Availability | High availability |
| **IAM** | Identity and Access Management | AWS access control |
| **IGW** | Internet Gateway | Enables internet access in VPC |
| **IOPS** | Input/Output Operations Per Second | Disk performance metric |
| **KDS** | Kinesis Data Streams | Real-time data stream |
| **KDF** | Kinesis Data Firehose | Streaming delivery to S3/Redshift/ES |
| **KMS** | Key Management Service | Encryption key management |
| **MFA** | Multi-Factor Authentication | Multi-factor authentication |
| **MGN** | Application Migration Service | Lift-and-shift servers to AWS |
| **MTBF** | Mean Time Between Failures | Mean time between failures |
| **MTTR** | Mean Time To Recovery | Mean time to recovery |
| **NACL** | Network Access Control List | Stateless firewall for VPC subnets |
| **NLB** | Network Load Balancer | Layer 4 LB (TCP/UDP), high performance |
| **ALB** | Application Load Balancer | Layer 7 LB (HTTP/HTTPS) |
| **CLB** | Classic Load Balancer | Legacy LB (not recommended) |
| **NAT** | Network Address Translation | NAT GW/Instance for private subnets |
| **OIDC** | OpenID Connect | Federated identity protocol |
| **OAC** | Origin Access Control | CloudFront accesses private S3 (new) |
| **OAI** | Origin Access Identity | CloudFront accesses private S3 (legacy) |
| **PCI DSS** | Payment Card Industry Data Security Standard | Compliance for card data |
| **RPO** | Recovery Point Objective | Maximum amount of data you can lose |
| **RTO** | Recovery Time Objective | Maximum time to recover after failure |
| **SAML** | Security Assertion Markup Language | SSO identity federation |
| **SCP** | Service Control Policy | Control policy in AWS Organizations |
| **SDK** | Software Development Kit | AWS development libraries |
| **SG** | Security Group | Stateful firewall for instances/resources |
| **SLA** | Service Level Agreement | Service level agreement (uptime) |
| **SNS** | Simple Notification Service | Pub/sub, notifications |
| **SOC** | Service Organization Control | Audit report (SOC1/SOC2/SOC3) |
| **SQS** | Simple Queue Service | Managed message queue |
| **SRR** | Same-Region Replication | S3 replication within the same region |
| **SSE** | Server-Side Encryption | Server-side encryption (S3/DynamoDB) |
| **SSM** | Systems Manager | Instance management, parameters |
| **STS** | Security Token Service | Temporary tokens (AssumeRole) |
| **TGW** | Transit Gateway | Multi-VPC connectivity hub |
| **TTL** | Time To Live | Expiration time (DNS, cache, DynamoDB) |
| **VPC** | Virtual Private Cloud | Isolated virtual network on AWS |
| **VPN** | Virtual Private Network | Encrypted connection on-premises ↔ AWS |
| **WAF** | Web Application Firewall | Layer 7 protection (SQLi, XSS) |
| **WORM** | Write Once Read Many | S3 Object Lock — immutability |

---

## Frequent Exam Confusions

| Concept A | vs | Concept B | How to Differentiate |
|------------|----|-----------|--------------|
| **RTO** | vs | **RPO** | RTO = recovery time; RPO = data lost (point in the past) |
| **Availability** | vs | **Durability** | Availability = can I access now? Durability = was data lost? |
| **Throughput** | vs | **Latency** | Throughput = how much per second; Latency = how long 1 operation takes |
| **Multi-AZ** | vs | **Read Replica** | Multi-AZ = HA/failover (synchronous standby); Read Replica = scale reads |
| **SG** | vs | **NACL** | SG = stateful (automatic return); NACL = stateless (inbound AND outbound rules) |
| **Secrets Manager** | vs | **SSM Param Store** | Secrets = automatic rotation, higher cost; SSM = general settings, free for Standard |
| **KMS CMK** | vs | **KMS AWS-managed** | CMK = you control rotation/access; AWS-managed = AWS controls |
| **SNS** | vs | **SQS** | SNS = push to N subscribers (fan-out); SQS = pull by application (1 consumer per msg) |
| **Elasticity** | vs | **Scalability** | Elasticity = scales in and out automatically; Scalability = ability to grow |
| **IaaS** | vs | **PaaS** | IaaS = EC2 (you manage OS); PaaS = Elastic Beanstalk/RDS (AWS manages OS/infra) |

---

## Storage Types

| Type | Service | Protocol | When to Use |
|------|---------|-----------|-------------|
| **Block** | EBS | iSCSI / NVMe | Boot volume, DB, app needing local disk |
| **File** | EFS | NFS v4.1 | Sharing between EC2s, Linux apps |
| **File** | FSx for Windows | SMB / CIFS | Windows apps, Active Directory |
| **Object** | S3 | HTTP REST | Backup, media, logs, data lake |
| **Archive** | S3 Glacier | HTTP | Compliance, long-term backup |
| **In-Memory** | ElastiCache | Redis/Memcached | Session cache, hot data |

---

## Shared Responsibility Model

| Responsibility | AWS | Client |
|-----------------|-----|---------|
| Physical hardware | Yes | |
| Hypervisor | Yes | |
| Physical network | Yes | |
| Operating System (EC2) | | Yes |
| OS patches | | Yes |
| Security Group configuration | | Yes |
| Customer data | | Yes |
| Data encryption | Tools | Configuration |
| IAM (users/roles) | | Yes |
| RDS OS patches | Yes | |
| RDS data | | Yes |

---

## Consistency in DynamoDB

| Type | What It Means | When to Use |
|------|----------------|-------------|
| **Eventual Consistency** | Read may return slightly outdated data | Default; lower cost; tolerant apps |
| **Strong Consistency** | Read always returns the most recent data | 2x read cost; when guarantee is needed |

---

## Availability SLAs — Reference

| Percentage | Downtime/year | Downtime/month | Example Service |
|------------|-------------|-------------|----------------|
| 99% | ~87.6h | ~7.3h | Basic services |
| 99.9% | ~8.7h | ~43.8min | EC2, S3 Standard-IA |
| 99.95% | ~4.4h | ~21.9min | RDS Multi-AZ |
| 99.99% | ~52.6min | ~4.4min | S3 Standard, DynamoDB |
| 99.999% | ~5.3min | ~26s | Route 53 |

---

## Exam Tips

| Clue in Question | Expected Answer |
|-----------------|------------------|
| "identify AWS resource by unique ID" | ARN (Amazon Resource Name) |
| "access AWS API with code" | SDK + IAM Role (never hardcoded access key) |
| "IP block for VPC" | CIDR (e.g., 10.0.0.0/16) |
| "free SSL certificate for ALB/CloudFront" | ACM (AWS Certificate Manager) |
| "maintain compliance with health laws" | HIPAA + BAA with AWS |
| "data that cannot be changed after writing" | S3 Object Lock (WORM) |
| "automatic database failover" | RDS Multi-AZ (not Read Replica) |
| "scale database reads" | RDS Read Replica (not Multi-AZ) |
| "SG returns response automatically" | Stateful (SG) vs Stateless (NACL) |
| "connect multiple VPCs as hub-and-spoke" | Transit Gateway (TGW) |
