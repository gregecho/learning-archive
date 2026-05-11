# Real-World Use Cases — Multi-Service Architectures (Module 27)

## Case 1 — Multi-Tenant SaaS Platform with Tier-Based Isolation

**Context:** B2B software company offers a management platform for clients of 3 sizes: Free (thousands of clients), Business (500 clients), Enterprise (50 large contracts). Each tier requires different levels of isolation and performance guarantees.

**Hybrid Architecture (Pool + Silo):**
```
ROUTING LAYER:
Route 53 → ALB → API Gateway

Tenant Routing Logic:
├── ENTERPRISE (silo): dedicated stack
│     ALB → dedicated ECS → dedicated Aurora (no sharing)
│     DDoS: Shield Advanced individual
│     SLA: 99.99%
│
├── BUSINESS (bridge): shared infra, separate DB
│     ALB → shared ECS → Aurora Schema per tenant
│     Compute: shared, Storage: isolated
│     SLA: 99.9%
│
└── FREE (pool): everything shared
      ALB → shared ECS → DynamoDB (tenantId = partition key)
      SLA: 99%

TENANT IDENTIFICATION:
JWT token → API GW Authorizer (Lambda)
Lambda extracts tenantId → injects into X-Tenant-ID header
ECS app uses X-Tenant-ID to route to correct queue / correct DB

NOISY NEIGHBOR PROTECTION (Free tier):
SQS per tenant-tier: Business has separate queue from Free
Lambda reserved concurrency: Business = 100, Free = 20
DynamoDB: on-demand (scales per tenant without affecting others)
```

---

## Case 2 — Strangler Fig Migration from Java Monolith to Microservices

**Context:** Legacy ERP system (Java monolith, 15 years old) needs gradual modernization. Cannot rewrite everything at once — high risk and prohibitive cost. Strategy: extract modules one by one without downtime.

**Strangler Fig Process:**
```
INITIAL STATE:
Everything in the Java monolith:
CLI → Java Server → PostgreSQL Oracle

PHASE 1 — INSERT PROXY (Strangler):
CLI → API GW / ALB ← NEW ENTRY POINT
        ├── /api/inventory → Java Monolith (legacy)
        ├── /api/clients → Java Monolith (legacy)
        ├── /api/orders → Java Monolith (legacy)
        └── /api/reports → Java Monolith (legacy)

PHASE 2 — EXTRACT INVENTORY MODULE:
← Develop inventory microservice in parallel
← Integration tests with real data
ALB Route: /api/inventory → NEW Lambda + DynamoDB
           (other /api/* still go to monolith)

PHASE 3 — EXTRACT ORDERS MODULE:
/api/orders → NEW ECS Service + Aurora PostgreSQL
/api/inventory → Lambda + DynamoDB (already migrated)
/api/clients, /api/reports → Monolith still

FINAL PHASE — "KILL" THE MONOLITH:
When last module extracted:
ALB no longer has routes to monolith
Java Monolith decommissioned
100% microservices on AWS

ANTI-PATTERN AVOIDED:
NO "Big Bang" — rewrite everything before going to production
YES Incremental — each extraction validated in production before the next
```

---

## Case 3 — Order Processing Pipeline with Saga Pattern

**Context:** Online marketplace with 3 independent microservices: Orders, Inventory and Payment. When an order is created, all 3 must be consistent — if payment fails, inventory must be released.

**Choreographed Saga (Event-Driven):**
```
HAPPY PATH:
Order created → SQS (OrderCreated)
                     │
              Lambda InventoryService
              ├── Reserve inventory
              └── SQS (InventoryReserved)
                            │
                     Lambda PaymentService  
                     ├── Charge payment
                     └── SQS (PaymentApproved)
                                    │
                             Lambda OrderService
                             └── Confirm order (status = CONFIRMED)
                             └── SNS (OrderConfirmed) → notify user

COMPENSATION (Rollback):
PaymentService fails → SQS (PaymentRejected)
                              │
                       Lambda InventoryService
                       └── Release inventory (compensation)
                       └── SQS (InventoryReleased)
                                   │
                            Lambda OrderService
                            └── Cancel order (status = CANCELLED)
                            └── SNS → notify user
```

**Orchestrated Saga (Step Functions):**
```
Step Functions Express Workflow:
State 1: Task (ReserveInventory) → retry 3x, catch → CancelOrder
State 2: Task (ProcessPayment) → retry 2x, catch → ReleaseInventory → CancelOrder
State 3: Task (ConfirmOrder)
State 4: Task (NotifyUser)

Compensation (Catch):
ReleaseInventory → CancelOrder → NotifyFailure

Advantage vs Choreography:
- Full state visibility at each step
- Configurable retry per step
- Easy debugging (integrated X-Ray)
```

---

## Case 4 — Event Sourcing for Financial Audit System

**Context:** Investment bank needs a complete, immutable history of all changes in accounts and portfolios. Regulation requires 10-year traceability + "replay" capability for auditing.

**Event Sourcing Architecture:**
```
WRITE MODEL:
App → API GW → Lambda (command handler)
                    │ Does NOT update state directly
                    │ WRITES immutable EVENT
                    ▼
              DynamoDB (event store — events table)
              ├── PK: aggregateId (ex: account-123)
              ├── SK: version (1, 2, 3...)
              ├── eventType: "BalanceDebited", "BalanceCredited"
              ├── payload: {amount: 5000, currency: "BRL"}
              └── timestamp: ISO 8601
              
DynamoDB Streams → Lambda (projections updater)
                        └── ElastiCache (current balance — fast read)
                        └── Athena/Redshift (analytical reports)

READ MODEL (CQRS):
App → API GW → Lambda (query handler)
                    └── ElastiCache (fast read of current state)

REPLAY FOR AUDIT:
Query: SELECT * FROM event_store WHERE accountId = 'account-123' ORDER BY version
      → Replay all events → recalculate state at any point in time
      
S3 (event store backup, compressed by month, Object Lock 10 years)
```

---

## Case 5 — Live Streaming Platform with IVS + Lambda

**Context:** Online education platform wants to offer live classes with very low latency (< 5 seconds), real-time chat, polls during the broadcast, and automatic recording for later replay.

**Architecture:**
```
BROADCAST:
Instructor → OBS/Encoder (RTMP) → Amazon IVS (Interactive Video Service)
                                        │
                                  CloudFront CDN (global delivery)
                                        │
                                  Student players (< 5s latency)

REAL-TIME CHAT:
Student → API GW WebSocket
             ├── Lambda (onConnect) → DynamoDB (connectionIds)
             ├── Lambda (sendMessage) → DynamoDB + broadcast
             └── Lambda (onDisconnect) → remove connectionId
             
Broadcast to everyone in the room:
Lambda → API GW Management API → POST /connections/{connectionId}

POLLS:
Instructor → REST API → Lambda → DynamoDB (poll + responses)
IVS Timed Metadata event → Player displays poll synchronized with video

RECORDING AND REPLAY:
IVS → S3 automatic (full recording)
     └── MediaConvert (transcoding to multiple resolutions)
            └── S3 (adaptive HLS)
                └── CloudFront (CDN for replay)

METRICS:
IVS → CloudWatch (viewers, bitrate, buffering ratio)
Custom: Lambda → CloudWatch Metrics (messages/min, poll responses)
```

**IVS vs MediaLive:**
| Criteria | IVS | MediaLive |
|---------|-----|-----------|
| Latency | < 5s (ultra-low latency) | 15-30s (standard) |
| Configuration | Low (managed) | High (many parameters) |
| Interactivity | Native (timed metadata, chat) | Limited |
| Cost | Per hour + GB | Per hour (more expensive at scale) |
| When to use | Simple interactive live streams | Broadcasting broadcast TV |
