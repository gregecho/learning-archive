# Module 20 — AWS Glossary SAA-C03

## About This Module

Dictionary of essential terms and concepts for the AWS Solutions Architect Associate (SAA-C03) exam. Organized by domain for quick review.

---

## A

| Term | Definition |
|---|---|
| **ACL (Access Control List)** | List of access rules. In S3: legacy per-bucket/object permission configuration. In VPC: NACL — stateless firewall at the subnet level |
| **ACM (AWS Certificate Manager)** | Service to provision, manage, and deploy free SSL/TLS certificates for use with CloudFront, ALB, API Gateway |
| **ALB (Application Load Balancer)** | Layer 7 load balancer (HTTP/HTTPS). Supports path-based and host-based routing, WebSocket, gRPC |
| **AMI (Amazon Machine Image)** | EC2 instance template containing OS, applications, and settings. Region-specific (can be copied between regions) |
| **ARN (Amazon Resource Name)** | Unique identifier for AWS resources. Format: `arn:aws:service:region:account-id:resource` |
| **ASG (Auto Scaling Group)** | Group of EC2 instances that scales automatically based on scaling policies or demand |
| **Athena** | Serverless SQL query service over data in S3. Pay per TB scanned |
| **Aurora** | MySQL/PostgreSQL-compatible relational database built by AWS. 5x performance over MySQL, 3x over PostgreSQL |
| **Availability Zone (AZ)** | Isolated data center within an AWS region. Multiple AZs per region ensure high availability |
| **AWS Organizations** | Centralized management of multiple AWS accounts with policies (SCPs) and consolidated billing |

---

## B

| Term | Definition |
|---|---|
| **Bastion Host** | EC2 instance in a public subnet used as an SSH access point to instances in private subnets. More secure replacement: SSM Session Manager |
| **Bedrock** | AWS Generative AI service. Access Foundation Models (Anthropic Claude, Amazon Titan, etc.) via API without managing infrastructure |
| **Blue/Green Deployment** | Deployment strategy with two identical environments; traffic is gradually or fully migrated from "blue" (current) to "green" (new) |
| **Bucket Policy** | Resource-based JSON policy applied directly to the S3 bucket. Controls access from any entity (cross-account) |
| **Burst** | Temporary capacity beyond the provisioned limit. EC2 (T instances): burstable CPU credits. Lambda: 3,000 initial concurrent executions per region |

---

## C

| Term | Definition |
|---|---|
| **CIDR (Classless Inter-Domain Routing)** | Notation for IP ranges. E.g.: `10.0.0.0/16` = 65,536 IPs. VPC CIDR defines the virtual network address space |
| **CloudFormation** | AWS IaC (Infrastructure as Code). YAML/JSON templates that define and provision AWS resources as code |
| **CloudFront** | AWS global CDN (Content Delivery Network) with 400+ edge locations. Improves latency and reduces origin load |
| **CloudTrail** | Audit service that records all API calls made in the AWS account. Essential for compliance and incident investigation |
| **CloudWatch** | Monitoring and observability service. Collects metrics, logs, creates alarms and dashboards |
| **CMK (Customer Managed Key)** | KMS key created and managed by the customer. Enables full control over usage policies and rotation |
| **Cognito** | Authentication and authorization service for web/mobile applications. User Pools (auth) + Identity Pools (AWS credential federation) |
| **Cold Start** | Delay on the first invocation of a Lambda function when a new execution environment needs to be initialized |
| **Compliance** | Conformity with regulations and standards (PCI-DSS, HIPAA, SOC2, ISO 27001). AWS is responsible for infrastructure; client for the application |
| **CRR (Cross-Region Replication)** | Automatic replication of S3 objects to a bucket in another region. Requires versioning enabled |

---

## D

| Term | Definition |
|---|---|
| **DAX (DynamoDB Accelerator)** | In-memory cache for DynamoDB with microsecond latency. Fully managed and compatible with DynamoDB API |
| **DLQ (Dead Letter Queue)** | Queue (SQS) or topic (SNS) that receives messages that could not be processed after the maximum number of attempts |
| **DMS (Database Migration Service)** | Database migration service. Supports homogeneous and heterogeneous migrations with CDC (Change Data Capture) option |
| **DynamoDB** | Fully managed key-value NoSQL database. Infinite scalability, millisecond latency, multi-region with Global Tables |
| **DX (Direct Connect)** | Dedicated private network connection between on-prem and AWS. Bandwidth of 1, 10, or 100 Gbps with consistent latency |

---

## E

| Term | Definition |
|---|---|
| **EBS (Elastic Block Store)** | High-performance disk volumes for EC2. Types: gp2/gp3 (general SSD), io1/io2 (high-performance SSD), st1 (throughput HDD), sc1 (cold HDD) |
| **EC2 (Elastic Compute Cloud)** | AWS virtual computing service (VMs). Hundreds of instance types for different workloads |
| **ECR (Elastic Container Registry)** | Managed private Docker image registry. Integrated with ECS, EKS, and Lambda Container Image |
| **ECS (Elastic Container Service)** | AWS-managed container orchestrator. Runs tasks on EC2 or Fargate |
| **EFS (Elastic File System)** | Managed and elastic NFS file system for Linux. Multi-AZ and multi-instance simultaneously |
| **EKS (Elastic Kubernetes Service)** | AWS-managed Kubernetes. Reduces operational complexity of the Kubernetes control plane |
| **ElastiCache** | Managed in-memory cache service. Two engines: Redis (persistence, Pub/Sub, sorted sets) and Memcached (simple, multi-thread) |
| **Endpoint (VPC)** | Private connection between VPC and AWS services without going to the internet. Gateway (S3, DynamoDB — free) or Interface (PrivateLink — paid) |
| **ESM (Event Source Mapping)** | Configuration that allows Lambda to receive events from Kinesis, DynamoDB Streams, SQS, MSK automatically |
| **EventBridge** | Serverless event bus. Routes events between AWS services, SaaS, and custom applications via rules |

---

## F–G

| Term | Definition |
|---|---|
| **Fargate** | Serverless computing for containers (ECS/EKS). No servers to manage; pay for vCPU/memory used by the task |
| **FIFO Queue** | SQS FIFO: guarantees ordering and exactly-once delivery. Limited to 300 TPS (3,000 with batching) |
| **FSx** | Managed high-performance file systems: Lustre (HPC), Windows (SMB), NetApp ONTAP, OpenZFS |
| **Global Accelerator** | Network service that uses the private AWS network (anycast) to route TCP/UDP traffic with lower global latency. 2 static anycast IPs |
| **Glue** | Serverless ETL service and data catalog. Crawlers discover schemas; Jobs process data with managed Spark |
| **GuardDuty** | Threat detection service using ML. Analyzes CloudTrail, VPC Flow Logs, DNS Logs to detect malicious behavior |

---

## H–I

| Term | Definition |
|---|---|
| **HA (High Availability)** | System's ability to continue operating even with component failures. Usually requires resources in multiple AZs |
| **IAM (Identity and Access Management)** | Access control for AWS resources. Users, groups, roles, and policies define who can do what |
| **IOPS (I/O Operations Per Second)** | Storage performance measurement. EBS gp3 baseline 3,000 IOPS; io2 Block Express up to 256,000 IOPS |
| **IRSA (IAM Roles for Service Accounts)** | EKS mechanism that associates IAM roles to Kubernetes service accounts. Pods obtain AWS credentials without hardcoded secrets |
| **Inspector** | Automated vulnerability assessment for EC2, Lambda Functions, and ECR images. Uses CVE database |

---

## J–K

| Term | Definition |
|---|---|
| **Jump Box** | See Bastion Host |
| **Kinesis Data Streams** | Real-time streaming service. Producers → Shards → Consumers. Retention up to 365 days; replay possible |
| **Kinesis Firehose** | Near-real-time data delivery to S3, Redshift, OpenSearch, Splunk. Fully managed without consumer code |
| **KMS (Key Management Service)** | Managed encryption key service. Integrated with all AWS services that support encryption |

---

## L–M

| Term | Definition |
|---|---|
| **Lambda** | Serverless computing. Runs code in response to events without provisioning servers. Pay per invocation + duration (GB-seconds) |
| **Lake Formation** | Data lake governance service over S3. Manages fine-grained permissions (column/row) for Glue + Athena |
| **Macie** | Data security service that uses ML to discover and protect sensitive data in S3 (PII, keys, credentials) |
| **MGN (Application Migration Service)** | Automated lift-and-shift service. Continuously replicates servers to AWS and performs cutover with minimal downtime |
| **MSK (Managed Streaming for Kafka)** | Managed Apache Kafka on AWS. Compatible with existing Kafka clients without changing code |
| **Multi-AZ** | High availability with resources in multiple Availability Zones. For RDS: synchronous automatic failover to standby |

---

## N–O

| Term | Definition |
|---|---|
| **NAT Gateway** | Network component that allows instances in private subnets to initiate connections to the internet without being accessible from the internet |
| **NACL (Network Access Control List)** | Stateless firewall at the subnet level. Evaluates numbered rules in order; separate inbound and outbound rules |
| **NLB (Network Load Balancer)** | Layer 4 load balancer (TCP/UDP/TLS). Extremely high performance (millions of RPS), static IP via EIP, ultra-low latency |
| **OAC (Origin Access Control)** | Current method (replaces OAI) for CloudFront to access S3 privately. The S3 bucket denies direct internet access |
| **OpenSearch** | Managed fork of Elasticsearch. Search, log analytics, and visualization with Kibana/OpenSearch Dashboards |

---

## P–Q

| Term | Definition |
|---|---|
| **Parameter Store** | Hierarchical configuration and secrets storage in Systems Manager. Free for standard (up to 4 KB/parameter) |
| **Placement Group** | Grouping of EC2 instances by proximity or distribution. Cluster (low latency), Spread (maximum availability), Partition (HBase/HDFS) |
| **PrivateLink** | AWS PrivateLink: exposes private services via Interface Endpoint (ENI) without traffic going through the internet |
| **QuickSight** | AWS serverless BI. SPICE engine for in-memory cache; embeddable dashboards; automatic ML Insights |

---

## R

| Term | Definition |
|---|---|
| **RDS (Relational Database Service)** | Managed relational databases: MySQL, PostgreSQL, Oracle, SQL Server, MariaDB, and Aurora |
| **Read Replica** | Asynchronous database copy to scale reads. RDS: up to 5 replicas; Aurora: up to 15 replicas |
| **Rekognition** | Computer vision as a service. Image and video analysis: objects, faces, text, content moderation |
| **Reserved Instance (RI)** | 1 or 3 year commitment with up to 72% discount vs On-Demand. Standard RI: fixed instance; Convertible RI: can change type |
| **Route 53** | AWS managed DNS with 100% SLA. Supports 8 routing policies + health checks |
| **RPO (Recovery Point Objective)** | Maximum amount of data that can be lost in a disaster event (determines backup frequency) |
| **RTO (Recovery Time Objective)** | Maximum acceptable time to restore system after failure (determines DR strategy) |

---

## S

| Term | Definition |
|---|---|
| **S3 (Simple Storage Service)** | Durable object storage (11 9s), virtually unlimited. Buckets per region; objects up to 5 TB |
| **SAM (Serverless Application Model)** | Simplified IaC framework for serverless Lambda/API GW/DynamoDB applications. CloudFormation extension |
| **Savings Plans** | Up to 66% (Compute) or 72% (EC2) discount in exchange for $$/hour commitment for 1 or 3 years. More flexible than Reserved Instances |
| **SCT (Schema Conversion Tool)** | Desktop tool that converts database schema between different engines in heterogeneous migration (alongside DMS) |
| **Security Group (SG)** | Stateful firewall at the instance/ENI level. Allow-only rules (no explicit Deny). Reference to other SGs by ID |
| **Shield** | DDoS protection. Standard (free, automatic for all); Advanced (paid, extra protection + DRT + free WAF) |
| **Spot Instance** | EC2 with up to 90% discount using idle capacity. Can be interrupted with 2-minute notice |
| **SQS (Simple Queue Service)** | Managed message queue. Standard (high throughput, at-least-once) or FIFO (guaranteed ordering, exactly-once) |
| **SSM (Systems Manager)** | Operational tools suite: Session Manager, Parameter Store, Patch Manager, Run Command, Automation |
| **SRR (Same-Region Replication)** | S3 object replication between buckets in the same region (e.g., consolidate logs, compliance) |
| **Step Functions** | Serverless workflow orchestrator. Coordinates lambdas, ECS tasks, and other services in visual state machines |

---

## T–Z

| Term | Definition |
|---|---|
| **TGW (Transit Gateway)** | Centralized network hub connecting VPCs and on-prem in hub-and-spoke topology. Transitive routing (unlike VPC Peering) |
| **Transcribe** | Managed Speech-to-Text. Supports streaming, speaker identification, custom vocabulary |
| **Transfer Family** | Managed SFTP/FTPS/FTP/AS2 server with S3 or EFS backend. Clients do not need to change existing tools |
| **Trusted Advisor** | Tool that recommends improvements in cost, security, performance, fault tolerance, and service limits |
| **VPC (Virtual Private Cloud)** | Isolated virtual network on AWS. You control CIDR, subnets, routing tables, security groups, and NACLs |
| **VPC Peering** | Connection between two VPCs (same or different account/region) via the AWS network. Non-transitive (A-B, B-C != A-C) |
| **WAF (Web Application Firewall)** | Layer 7 web application firewall. Protects against SQL injection, XSS, and other attacks via web ACLs and managed rules |
| **WORM (Write Once Read Many)** | Storage model where data cannot be modified after being written. S3 Object Lock Compliance mode |
| **X-Ray** | Distributed tracing service. Visualizes latency, errors, and performance between services in an application |

---

## Acronym Table

| Acronym | Meaning |
|---|---|
| ACL | Access Control List |
| ACM | AWS Certificate Manager |
| ALB | Application Load Balancer |
| AMI | Amazon Machine Image |
| ARN | Amazon Resource Name |
| ASG | Auto Scaling Group |
| CDC | Change Data Capture |
| CDN | Content Delivery Network |
| CMK | Customer Managed Key |
| CRR | Cross-Region Replication |
| DAX | DynamoDB Accelerator |
| DLQ | Dead Letter Queue |
| DMS | Database Migration Service |
| DX | Direct Connect |
| EBS | Elastic Block Store |
| ECR | Elastic Container Registry |
| ECS | Elastic Container Service |
| EFS | Elastic File System |
| EKS | Elastic Kubernetes Service |
| ELB | Elastic Load Balancing |
| ENI | Elastic Network Interface |
| ESM | Event Source Mapping |
| FGA | Fine-Grained Access Control |
| FM | Foundation Model (Bedrock) |
| FSx | Amazon FSx (file systems) |
| IAM | Identity and Access Management |
| IGW | Internet Gateway |
| IOPS | Input/Output Operations Per Second |
| IRSA | IAM Roles for Service Accounts |
| IaC | Infrastructure as Code |
| KMS | Key Management Service |
| MGN | AWS Application Migration Service |
| MPP | Massively Parallel Processing |
| MSK | Managed Streaming for Kafka |
| NACL | Network Access Control List |
| NLB | Network Load Balancer |
| NLP | Natural Language Processing |
| OAC | Origin Access Control |
| OAI | Origin Access Identity (legacy) |
| PII | Personally Identifiable Information |
| RI | Reserved Instance |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SCP | Service Control Policy |
| SCT | Schema Conversion Tool |
| SG | Security Group |
| SNS | Simple Notification Service |
| SQS | Simple Queue Service |
| SRR | Same-Region Replication |
| SSE | Server-Side Encryption |
| SSM | AWS Systems Manager |
| TGW | Transit Gateway |
| TTS | Text-to-Speech |
| VGW | Virtual Private Gateway |
| VPC | Virtual Private Cloud |
| WAF | Web Application Firewall |
| WAT | Well-Architected Tool |
| WORM | Write Once Read Many |
