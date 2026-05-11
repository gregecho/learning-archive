# Cheatsheet — Module 11: Serverless, Lambda and API Gateway

## Critical Lambda Limits

| Parameter | Value |
|---|---|
| Maximum timeout | 15 minutes |
| Memory | 128 MB to 10,240 MB |
| Synchronous payload (request/response) | 6 MB each |
| Asynchronous payload | 256 KB |
| Package size (zip) | 50 MB (zip) / 250 MB (uncompressed) |
| Concurrent executions per account/region | 1,000 (default, increasable) |
| Maximum layers per function | 5 |
| Environment variables | 4 KB total |
| Tmp storage (/tmp) | 512 MB to 10,240 MB |

---

## Lambda Invocation Types

| Type | Who Uses It | Retry | DLQ |
|---|---|---|---|
| **Synchronous** | API GW, ALB, SDK, CLI | None (client retry) | N/A |
| **Asynchronous** | S3, SNS, EventBridge, SES | 2 automatic retries | SQS/SNS via Destinations |
| **Event Source Mapping** | SQS, Kinesis, DynamoDB Streams, MSK | Retry until expiry (Kinesis) or maxReceiveCount (SQS) | DLQ configured on the queue |

---

## Lambda Concurrency

| Type | Description | Cost |
|---|---|---|
| **On-demand** | Scales automatically as demand increases | Standard (pay-per-use) |
| **Reserved** | Guarantees exclusive capacity for the function; limits to the defined maximum | Standard |
| **Provisioned** | Pre-warms instances (eliminates cold starts) | $0.015/GB-hour provisioned |

**Throttling:** if `concurrent executions > reserved/account limit` → **HTTP 429** (sync) or event goes to the retry queue (async).

---

## API Gateway — API Types

| Type | Features | Cost | Best For |
|---|---|---|---|
| **REST API** | Stages, caching, usage plans, API keys, full transform | Medium | Full production APIs |
| **HTTP API** | Native JWT/OAuth, no mapping templates | ~70% cheaper | Simple microservices |
| **WebSocket API** | Persistent bidirectional connections | Per connection + message | Chat, real-time updates |

---

## API Gateway Throttling

| Limit | Default Value |
|---|---|
| Request rate per account | 10,000 req/s |
| Burst | 5,000 concurrent req |
| HTTP 429 | Too Many Requests (when exceeded) |

---

## API Gateway Integrations

| Type | Description |
|---|---|
| **Lambda Proxy** | Full event to Lambda; Lambda returns statusCode + headers + body |
| **Lambda Custom** | Mapping templates (VTL) transform request/response |
| **HTTP Proxy** | Forwards HTTP request without transformation |
| **AWS Service** | Calls AWS API directly (e.g., SQS SendMessage without Lambda) |
| **Mock** | Returns static response (for testing, CORS OPTIONS) |
| **VPC Link** | Accesses NLB in private VPC |

---

## API Gateway Authorizers

| Type | How It Works |
|---|---|
| **Lambda Authorizer Token** | Token in header → Lambda evaluates → returns IAM Policy (ALLOW/DENY) |
| **Lambda Authorizer Request** | Headers + query params → Lambda → IAM Policy; flexible |
| **Cognito User Pools** | Cognito JWT token natively validated by API GW |

Result cache: up to **3600 seconds** (configurable, default 300s).

---

## Lambda Execution Environment Lifecycle

```
INIT phase     → download code, start runtime, execute init code (outside handler)
INVOKE phase   → execute handler function
SHUTDOWN phase → cleanup (response to SIGTERM)
```

**Cold Start** occurs on: first invocation, after idle period, new deployment, concurrency increase beyond warm instances.

---

## Lambda + VPC — Connectivity Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ AWS CLOUD                                                   │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │   Lambda        │     │   VPC                       │   │
│  │   (hyperplane)  │─ENI─│  ┌──────────┐ ┌──────────┐ │   │
│  │                 │     │  │ Private  │ │ RDS / EC2│ │   │
│  └─────────────────┘     │  │ Subnet   │ │          │ │   │
│                          │  └──────────┘ └──────────┘ │   │
│                          │         ↓ NAT GW (if internet needed) │   │
│                          └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Without NAT GW**: Lambda in VPC has no internet access (SSM, DynamoDB need VPC Endpoint or NAT GW).

---

## Lambda vs Other Compute — When to Use

| Scenario | Service |
|---|---|
| Event-driven, < 15 min, stateless | Lambda |
| Containerized, microservices, > 15 min | ECS Fargate |
| Needs GPU, HPC, specific software | EC2 |
| Long batch job (hours/days) | AWS Batch |
| Multi-step orchestrated workflow | Step Functions + Lambda |
| ML Training/Inference | SageMaker |

---

## Exam Tips — Common Patterns

| Clue in the Question | Likely Answer |
|---|---|
| "Cold start" + Java | Lambda SnapStart |
| "Consistent latency" serverless | Provisioned Concurrency |
| "Custom authentication" API GW | Lambda Authorizer |
| "JWT / OAuth" API GW | HTTP API + JWT Authorizer |
| "Lambda cannot access RDS" | Check SG + VPC config + NAT GW |
| "Lambda needs 30 min" | Lambda does NOT work → ECS Fargate or AWS Batch |
| "Gradual deployment 10% → 100%" | Lambda Alias with weights (canary) |
| "Multiple environments (dev/staging/prod)" | API GW Stages |
| "Mount dependencies across functions" | Lambda Layers |
| "Lambda must not be invoked more than N times/s" | Reserved Concurrency |
