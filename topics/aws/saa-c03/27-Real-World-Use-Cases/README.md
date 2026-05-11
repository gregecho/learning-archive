# Module 27 — Real-World Use Cases: Multi-Service Architectures

## About This Module

Real architectures integrate multiple AWS services. This module presents recurring architectural patterns in the SAA-C03 exam, where the right combination of services determines the optimal solution.

---

## Case 1: High Availability E-commerce

**Requirements**: Global web application, scalable, with secure payments and product catalog.

```
Global Users
    ↓
Route 53 (DNS + Health Checks + failover/latency routing)
    ↓
CloudFront (CDN — static assets at edge locations)
    ↓
WAF + Shield Standard (DDoS protection at the edge)
    ↓
ALB (Application Load Balancer — distributes across multiple AZs)
    ↓
Auto Scaling Group → EC2 (app tier) or ECS Fargate
    │
    ├── RDS Aurora MySQL (Multi-AZ for orders/users)
    │     └── Aurora Read Replicas (heavy read)
    ├── ElastiCache Redis (session and catalog cache)
    ├── DynamoDB (shopping cart — low latency)
    │
    └── S3 (product images) → CloudFront origin
         └── SQS (order queues) → Lambda (async processing)
              └── SNS (notifications) → SES (confirmation email)
```

**Key services and justifications:**
- Aurora Multi-AZ: availability for transactional data  
- ElastiCache: reduces latency and database load
- SQS decouples order processing (fault tolerance in integration)
- CloudFront reduces global latency and transfer cost

---

## Case 2: Real-Time Data Pipeline

**Requirements**: IoT event ingestion, real-time processing, analytics, and alerts.

```
IoT Devices
    ↓
IoT Core (MQTT) or Kinesis Data Streams
    ↓
Lambda (event transformation) ─── DynamoDB (current device state)
    │
    ├── Kinesis Firehose → S3 (raw data lake, Parquet)
    │         └── Glue Crawlers → Glue Catalog
    │               └── Athena (analyst ad-hoc queries)
    │
    └── Kinesis Data Analytics (Apache Flink)
          └── Anomaly detection → SNS → Lambda → PagerDuty
                                → CloudWatch Alarms
```

**Key services and justifications:**
- Kinesis Data Streams: high-volume real-time ingestion
- Kinesis Firehose: near real-time delivery to S3 (zero management code)
- Lambda ESM: processes Kinesis events in batches  
- Athena: serverless analysis of data in S3

---

## Case 3: Serverless Application with Authentication

**Requirements**: Serverless REST API, user authentication, variable data.

```
Mobile/Web App
    ↓
Amazon Cognito User Pool (signup/login/MFA/JWT tokens)
    ↓
API Gateway HTTP API (+ JWT Authorizer with Cognito)
    ↓
Lambda Functions:
    ├── GET /products   → DynamoDB (read, DAX for cache)
    ├── POST /orders    → DynamoDB + EventBridge
    ├── GET /files      → Pre-signed S3 URL returned to client
    └── POST /files     → Pre-signed S3 URL for direct upload

EventBridge:
    └── Rule: order.created → Lambda (send email) → SES
    └── Rule: order.created → SQS → Lambda (process payment)

Monitoring:
    X-Ray (tracing API GW → Lambda → DynamoDB)
    CloudWatch Logs (structured logging)
    CloudWatch Alarms (Lambda errors, throttles)
```

**Key services and justifications:**
- Cognito User Pool: complete auth (OAuth2/OIDC) without custom code
- API GW HTTP API: 71% lower cost than REST API for simple endpoints
- Pre-signed S3 URLs: clients upload/download directly to S3 (does not go through Lambda)
- DAX: in-memory cache for DynamoDB (microseconds for repeated reads)

---

## Case 4: Multi-Region Disaster Recovery

**Requirements**: RTO < 15 min, RPO < 5 min for critical application.

```
Primary Region (us-east-1)
    ├── RDS Aurora (primary)     ──[global database]──→  DR Region (us-west-2)
    ├── DynamoDB Global Tables   ──[multi-master]──────→  DynamoDB Global Table
    ├── S3 (application data)    ──[CRR]──────────────→  S3 replica
    └── EC2 ASG (app)

Route 53:
    ├── Health Check → ALB us-east-1 (primary, weight 100)
    └── Failover Record → ALB us-west-2 (DR, weight 0)
           └── Trigger: health check fails → DNS TTL flip to us-west-2

DR Region (us-west-2) — Warm Standby:
    ├── Aurora Secondary (read, promotes to primary on failover)
    ├── DynamoDB Global Table (already active — local read available)
    ├── EC2 ASG (reduced capacity — scales upon receiving traffic)
    └── ALB
```

**Strategy: Warm Standby** → RTO ~10-15 min, RPO ~1-5 min (Aurora async replication ~1s)

---

## Case 5: Migrating from Monolith to Microservices

**Requirements**: Migrate legacy .NET application to modern architecture, without downtime.

```
Phase 1 — Strangler Fig Pattern:
  Original monolith → Route 53 (via path-based routing on ALB)
      ├── /api/auth → New auth service (Fargate + Cognito)
      ├── /api/catalog → New catalog service (Lambda + DynamoDB)
      └── /* → Monolith (EC2) still in production

Phase 2 — Async Decoupling:
  Monolith emits events → SNS/EventBridge
    └── Microservices consume events (replacing synchronous calls)

Phase 3 — Complete Migration:
  ECS/EKS (containers) or Lambda (serverless) by business domain
  API Gateway (single facade for all microservices)
  Service Connect or App Mesh (inter-service communication)
```

**Patterns used:**
- **Strangler Fig**: replaces parts incrementally, never full cutover at once
- **Event-driven**: decouples services with EventBridge/SNS/SQS
- **API Gateway as facade**: clients don't need to know internal topology

---

## Case 6: Big Data Analytics with Lake House

**Requirements**: Scalable data lake for batch and real-time analytics.

```
Diverse Sources:
  ├── RDS/Aurora → DMS (CDC) → S3 (raw) 
  ├── SaaS APIs → Lambda → S3
  ├── Clickstream → Kinesis Firehose → S3
  └── Files → DataSync → S3

S3 Lake (zones):
  raw/ → bronze/ (Glue ETL) → silver/ (Parquet + partitioned) → gold/ (aggregated)

Catalog:
  Glue Crawlers → Glue Data Catalog → Lake Formation (FGA permissions)

Consumption:
  Athena → ad-hoc reporting (pay per scan)
  Redshift Spectrum → DW queries mixing S3 + Redshift
  QuickSight (SPICE) → executive dashboards
  SageMaker → ML models on gold/ data
```

---

## Recurring Exam Patterns

| Pattern | Services | Context |
|---|---|---|
| Fan-out | SNS → multiple SQS | Notify multiple systems simultaneously |
| Decoupling | SQS between producer/consumer | Buffer, tolerate peaks, retry |
| CQRS | DynamoDB (write) + ElastiCache (read) | Separate reads from writes to optimize |
| Event Sourcing | Kinesis/EventBridge → Lambda → DynamoDB | Audit trail + async processing |
| Cache-aside | Lambda → ElastiCache miss → DynamoDB | Reduce repeated read latency |
| Blue/Green | CodeDeploy or R53 weighted | Zero-downtime deployment |

---

## Exam Tips

- Architecture questions: look for the **most managed** service that satisfies the requirements
- "High availability" → Multi-AZ (RDS Multi-AZ, ASG across multiple AZs, ELB)
- "Low global latency" → CloudFront (assets), Global Accelerator (TCP/UDP), Aurora Global DB
- "Decoupling" → SQS (point-to-point) or SNS (fan-out)
- "Asynchronous processing" → SQS + Lambda or EventBridge + Lambda
- "Cost-effective for variable workloads" → Lambda (serverless), Fargate On-Demand, Spot ASG
- "Security in layers" → WAF + Shield + SG + NACL + KMS + Macie
