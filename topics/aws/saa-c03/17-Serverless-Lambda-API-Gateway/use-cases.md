# Real-World Use Cases — Serverless, Lambda and API Gateway (Module 11)

## Case 1 — Serverless REST API for E-commerce

**Context:** E-commerce startup needs an API for a product catalog and order creation. Expects traffic spikes on holidays (Black Friday, Christmas). Limited budget — does not want to pay for idle capacity.

**Requirements:**
- Automatic scaling without manual intervention
- Cost proportional to usage (no traffic = no cost)
- Latency < 500ms for product reads
- JWT authentication for order routes

**Architecture:**
```
Mobile/Web Client
       │
       ▼
  CloudFront (cache GET /products)
       │
       ▼
 API Gateway (REST)
  ├── GET /products      → Lambda (no auth) → DynamoDB (catalog)
  ├── GET /products/{id} → Lambda (no auth) → DynamoDB
  ├── POST /orders       → Lambda (JWT auth) → DynamoDB + SNS
  └── GET /orders/{id}   → Lambda (JWT auth) → DynamoDB
           │
     Cognito Authorizer (validates JWT)
           │
     DynamoDB (orders, TTL on session items)
           │
     SNS → SQS → Lambda (process payment async)
```

**Design Decisions:**
| Decision | Discarded Alternative | Reason |
|---------|----------------------|--------|
| Lambda + DynamoDB | EC2 + RDS | No idle capacity; DynamoDB scales horizontally |
| Cognito Authorizer | Lambda Authorizer | Less operational overhead; Cognito manages JWT rotation |
| CloudFront in front | API GW only | GET caching reduces Lambda invocations |
| SNS → SQS async | Lambda sync for payment | Decouples; payment can take time without timeout |

**Cost Estimate (1M req/month):**
- API Gateway: ~$3.50
- Lambda: ~$0.20 (Free Tier covers)
- DynamoDB On-Demand: ~$1.25
- **Total: < $5/month** vs EC2 t3.small ($13/month idle)

---

## Case 2 — Image Processing Pipeline

**Context:** Social media platform needs to resize and apply filters to user-uploaded images. Volume of 50,000 uploads/day with peaks of 500 uploads/minute.

**Requirements:**
- Process images asynchronously (user does not wait)
- Ensure no image is lost (at-least-once)
- Multiple outputs: 100px thumbnail, 600px medium, original
- Store results in a global CDN

**Architecture:**
```
User uploads
       │
       ▼
  S3 (bucket: original-uploads)
       │ S3 Event Notification
       ▼
  SQS (buffer — ensures at-least-once)
       │
       ▼
  Lambda (processImage)
  ├── Reads image from S3
  ├── Resizes with Pillow Layer
  ├── Writes thumbnail/medium/original to S3 (bucket: processed)
  └── Updates DynamoDB (status = "processed")
       │
       ▼
  CloudFront → S3 (bucket: processed)
  
  DLQ (SQS) → SNS → Email (failure alerts)
  CloudWatch → Alarm → SNS (Lambda errors > 10)
```

**Points of Attention:**
- Lambda Layer with Pillow library (max 250 MB uncompressed)
- Reserved concurrency to avoid S3 throttling
- SQS visibility timeout > Lambda max runtime (e.g., Lambda 30s → SQS timeout 35s)
- DLQ configured with maxReceiveCount=3

---

## Case 3 — Webhook Fanout with SNS → Lambda

**Context:** SaaS platform needs to notify multiple systems when a business event occurs (e.g., "customer closed a deal"): CRM, ERP, billing system, email marketing.

**Requirements:**
- Event published once → multiple systems receive it
- Failure in 1 system does not affect others
- Each system has its own processing pace

**Architecture:**
```
App (publishes event)
       │
       ▼
  SNS Topic: contract-closed
  ├── Subscriber 1: SQS → Lambda (update CRM)
  ├── Subscriber 2: SQS → Lambda (update ERP)
  ├── Subscriber 3: SQS → Lambda (generate billing)
  └── Subscriber 4: SQS → Lambda (trigger email marketing)

  Each SQS has its own DLQ
  Each Lambda has a separate CloudWatch Log Group
```

**Why SQS between SNS and Lambda (and not SNS → Lambda directly)?**
- SQS ensures persistence if Lambda fails
- SQS allows concurrency control (Lambda does not get overwhelmed)
- SQS allows DLQ per subscriber (CRM failure does not contaminate ERP)
- SNS → Lambda directly: event loss if Lambda fails (no native retry)

---

## Case 4 — GraphQL API with AppSync + Lambda

**Context:** Social network mobile app needs real-time subscriptions (feed notifications), optimized queries, and custom resolvers for business logic.

**Requirements:**
- Real-time updates (native WebSocket)
- Direct DynamoDB resolvers (no Lambda for simple CRUD)
- Lambda resolvers only for complex logic (friend recommendations)
- Authentication with Cognito User Pool

**Architecture:**
```
Mobile App
    │ GraphQL (HTTP/WebSocket)
    ▼
AWS AppSync
    ├── Query getUserProfile → DynamoDB Resolver (direct)
    ├── Query getFeed       → DynamoDB Resolver (direct)
    ├── Mutation createPost → DynamoDB Resolver + Pipeline Resolver
    ├── Query recommendations → Lambda Resolver (ML logic)
    └── Subscription onNewPost → Automatic WebSocket push
    
Cognito User Pool (AppSync authentication)
DynamoDB (users, posts, follows)
Lambda (recommendation engine)
```

**AppSync vs API Gateway:**
| Criterion | AppSync | API GW REST |
|---------|---------|------------|
| Real-time subscriptions | Native WebSocket | Requires separate API GW WebSocket |
| Optimized queries | GraphQL (1 request) | REST multiple endpoints |
| Direct DB resolvers | DynamoDB, Aurora | Always via Lambda |
| Complexity | Higher initial setup | Simple for pure REST |

---

## Case 5 — Batch Processing with Lambda and Step Functions

**Context:** Financial analysis company needs to process 1 million daily transactions by 6 AM. Each transaction goes through 3 sequential steps: validation, enrichment (external API query), and score calculation.

**Requirements:**
- Process everything in < 4 hours
- Automatic retry on step failure
- Final report of rejected transactions
- Real-time progress visibility

**Architecture:**
```
EventBridge Scheduler (02:00 UTC daily)
       │
       ▼
  Step Functions (Express Workflow)
  ┌─────────────────────────────────┐
  │ Map State (parallel processing)  │
  │   ├── Lambda: Validate Transaction│
  │   │     (retry: 3x, backoff 2s)  │
  │   ├── Lambda: Enrich Data        │
  │   │     (retry: 5x, backoff 10s) │
  │   └── Lambda: Calculate Score    │
  │         (retry: 2x, backoff 1s)  │
  └─────────────────────────────────┘
       │
       ▼
  DynamoDB (calculated scores)
  S3 (JSON report of rejected)
  SNS → Email (completion notification)
  CloudWatch Logs (details of each execution)
```

**Why Step Functions and not chained SQS?**
- Step Functions: state visibility, configurable retry per step, native Map State for parallelism
- Chained SQS: works, but no pipeline state visibility, retry is hard to configure per step
- Lambda timeout 15min: sufficient for 1 transaction, Step Functions orchestrates the batch

**Cost for 1M transactions/day:**
- Step Functions Express: $1.00 per 1M state executions
- Lambda: ~$0.20 per 1M invocations
- DynamoDB: ~$1.25 write
- **Total: < $3/day**
