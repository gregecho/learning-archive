# Cheatsheet — Practice Exams and Questions (Module 29)

## SAA-C03 Exam Structure

| Domain | Weight | Key Topics |
|---------|------|---------------|
| **1 — Design Secure Architectures** | 30% | IAM, KMS, SCPs, VPC, WAF, Shield, Cognito |
| **2 — Design Resilient Architectures** | 26% | Multi-AZ, Multi-Region, Auto Scaling, DR, SQS, SNS |
| **3 — Design High-Performing Architectures** | 24% | ElastiCache, CloudFront, Kinesis, RDS Read Replicas, DynamoDB |
| **4 — Design Cost-Optimized Architectures** | 20% | Savings Plans, Reserved, Spot, S3 tiers, Trusted Advisor |

- **Questions:** 65 (50 scored + 15 unscored / experimental)
- **Duration:** 130 minutes (~2 min/question)
- **Passing score:** 720/1000 (100-1000 scale)
- **Format:** multiple choice (1 answer) + multiple response (2-3 answers)
- **Available languages:** English, Japanese, Korean, Simplified Chinese, etc.

---

## Time Strategy

| Phase | Time | Action |
|------|-------|------|
| **1st pass** | ~70 min | Answer questions you know. Mark doubts. |
| **2nd pass** | ~40 min | Review marked. Eliminate and choose. |
| **Buffer** | ~20 min | Difficult questions / final review |
| **Total** | 130 min | |

> **Rule:** Never leave a question blank. Smart guessing is better than zero.

---

## Service Decision Matrix

### Compute
| Criteria | Lambda | ECS/Fargate | EC2 |
|---------|--------|-------------|-----|
| Max duration | 15 min | unlimited | unlimited |
| OS management | zero | zero | you |
| Cold start | yes | yes (lower) | no |
| Local state | no | yes (ephemeral) | yes |
| Base cost | per req | per vCPU/mem/h | per h |
| When to use | event-driven, short | containers, long-running | full control, licenses |

### Database
| Criteria | DynamoDB | RDS / Aurora | ElastiCache |
|---------|---------|--------------|-------------|
| Model | NoSQL (KV/Doc) | SQL relational | In-memory |
| Scalability | auto horizontal | vertical + read replicas | clustered |
| Latency | single-digit ms | ms–s | sub-ms |
| Transactions | yes (limited) | full ACID | no |
| When to use | massive scale, KV | relational data | L1 cache, sessions |

### Object Storage (S3)
| Class | Access | Relative Cost | Minimum Storage |
|--------|--------|----------------|-----------------|
| Standard | Frequent | High | — |
| Intelligent-Tiering | Variable (auto-move) | Medium + monitoring fee | — |
| Standard-IA | Infrequent | Medium-low | 30 days |
| One Zone-IA | Infrequent, 1 AZ | Low | 30 days |
| Glacier Instant | Archive, fast access | Very low | 90 days |
| Glacier Flexible | Archive, 1-5h retrieval | Ultra low | 90 days |
| Glacier Deep Archive | Long-term archive, 12h | Minimum | 180 days |

---

## Critical Numeric Values to Memorize

| Service | Value | What It Is |
|---------|-------|---------|
| **Lambda** | 15 min | Maximum timeout |
| **Lambda** | 10 GB | Maximum memory |
| **Lambda** | 512 MB → 10 GB | /tmp storage |
| **SQS Standard** | 14 days | Maximum retention |
| **SQS FIFO** | 300/s (3,000 with batching) | Maximum throughput |
| **SQS** | 256 KB | Maximum message size |
| **SNS** | 256 KB | Maximum message size |
| **S3** | 11 nines (99.999999999%) | Durability |
| **S3** | 5 TB | Maximum object size |
| **S3 Multipart** | > 100 MB recommended | When to use multipart upload |
| **DynamoDB** | 400 KB | Maximum item size |
| **DynamoDB** | single-digit ms | Typical latency |
| **Kinesis KDS** | 1 MB/s or 1,000 rec/s | Per shard (ingestion) |
| **Kinesis KDS** | 2 MB/s | Per shard (read) |
| **Kinesis KDS** | 7 days | Default retention (max 365) |
| **API Gateway** | 29 seconds | Maximum integration timeout |
| **CloudFront** | 1 year | Maximum TTL |
| **RDS** | 35 days | Maximum automatic backup |
| **Aurora** | 6 copies across 3 AZs | Storage replication |
| **EBS GP3** | 16,000 IOPS | Maximum |
| **EBS io2** | 64,000 IOPS | Maximum (io2 Block Express: 256K) |
| **EFS** | Unlimited (elastic) | Capacity |
| **VPC** | /16 | Largest allowed CIDR |
| **VPC** | /28 | Smallest allowed CIDR |
| **Reserved subnets** | 5 IPs | AWS reserves first 4 + last |
| **IAM** | 5,000 users | Default account limit |
| **CloudTrail** | 90 days | Default retention (Event History) |

---

## Elimination Strategies

### Tips to Eliminate Wrong Answers

1. **Negative trigger words:**
   - "manually" → almost always wrong (AWS = automation)
   - "requires downtime" → generally wrong for HA
   - "share root credentials" → always wrong

2. **Words pointing to correct answer:**
   - "least operational change" → managed service
   - "lowest cost" → check Spot, Reserved, serverless, S3-IA
   - "highest availability" → Multi-AZ, Auto Scaling
   - "minimum code" → managed/fully-managed service

3. **Common traps:**
   - **Multi-AZ vs Read Replica:** Multi-AZ = availability/failover, Read Replica = performance/reading
   - **SQS vs SNS:** SQS = queue (1 consumer per msg default), SNS = pub/sub (N consumers)
   - **S3 Standard-IA vs Glacier:** IA = sporadic but fast access, Glacier = archive
   - **Security Group vs NACL:** SG = stateful (automatic return), NACL = stateless (explicit rule)

---

## Quick Service Identification Patterns

| Keyword | Likely Service |
|--------------|-----------------|
| "serverless" | Lambda, Fargate, Aurora Serverless, DynamoDB |
| "event-driven" | Lambda + EventBridge / SQS / SNS |
| "real-time streaming" | Kinesis Data Streams |
| "streaming transformation/delivery" | Kinesis Data Firehose |
| "decoupled queue" | SQS |
| "pub/sub" / "broadcast" | SNS |
| "workflow / orchestration" | Step Functions |
| "CDN / static content" | CloudFront |
| "DNS / global routing" | Route 53 |
| "HTTP/HTTPS load balancing" | ALB |
| "TCP/UDP extreme performance balancing" | NLB |
| "user authentication" | Cognito |
| "cross-account permissions" | IAM Roles + STS |
| "secrets / rotatable passwords" | Secrets Manager |
| "configuration parameters" | SSM Parameter Store |
| "managed key encryption" | KMS |
| "DDoS layer 7 protection" | WAF + Shield |
| "SQL log analysis" | Athena |
| "big data ETL" | Glue |
| "data warehouse" | Redshift |
| "pre-trained ML (NLP/vision)" | Rekognition / Comprehend / Textract |
| "custom ML training" | SageMaker |

---

## Route 53 Routing Policies

| Policy | When to Use | Key Question |
|---------|-------------|----------------|
| **Simple** | 1 resource, no logic | Basic |
| **Weighted** | A/B testing, gradual deploy | "% of traffic" |
| **Latency** | Lowest latency per region | "best global performance" |
| **Failover** | Active-passive DR | "automatic failover" |
| **Geolocation** | Content by country/continent | "local laws / location" |
| **Geoproximity** | Bias traffic routing | "fine-tune routing" |
| **Multivalue Answer** | Health check + multiple IPs | "simple multi-IP availability" |

---

## Exam Tips

| Clue in the Question | Expected Answer |
|-----------------|------------------|
| "immediate response, 65 questions, 130 min" | ~2 min per question |
| "SAA-C03 minimum passing score" | 720/1000 |
| "highest exam weight" | Domain 1 — Secure Architectures (30%) |
| "Multi-AZ RDS — what benefit?" | Automatic failover (HA), not performance |
| "RDS Read Replica — what benefit?" | Scale reads (not failover) |
| "S3 durability?" | 11 nines (99.999999999%) |
| "Lambda max timeout?" | 15 minutes |
| "SQS max retention?" | 14 days |
| "question asks minimum cost + rare file access" | S3 Glacier Deep Archive |
| "question asks minimum cost + unpredictable access" | S3 Intelligent-Tiering |
| "VPC subnets: how many IPs does AWS reserve?" | 5 (first 4 + last) |
