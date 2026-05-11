# Module 11 — Serverless: Lambda and API Gateway

## Serverless Computing on AWS

In the serverless model, you do not provision or manage servers — you define only the code and AWS handles the rest (provisioning, scalability, patches, HA). You pay only for what you execute.

---

## AWS Lambda

### Execution Model

```
Event Source → Lambda Service → Execution Environment
                                  └── Runtime (Python/Node/Java/Go/Ruby/.NET)
                                        └── your-handler(event, context)
```

- **Handler**: entry point (`module.function`, e.g., `app.lambda_handler`)
- **Event**: JSON payload with trigger data (varies by event source)
- **Context**: object with metadata (request_id, remaining_time, function_name, memory_limit)

### Important Limits

| Parameter | Limit | Notes |
|---|---|---|
| Timeout | 3s default, **15 minutes** maximum | Configure as needed |
| Memory | 128 MB to **10,240 MB** (10 GB) | CPU scales proportionally |
| /tmp storage | 512 MB default, up to **10,240 MB** | Ephemeral per execution environment |
| Input payload (sync) | 6 MB | - |
| Input payload (async) | 256 KB | - |
| Package size (zip) | 50 MB (direct), 250 MB (S3) | 250 MB uncompressed |
| Layers | Up to 5 per function | Total 250 MB uncompressed |
| Default concurrency | 1,000 per region | Increase via support ticket |

### Invocation Models

| Model | Who invokes | Behavior on Error | Examples |
|---|---|---|---|
| **Synchronous** | Caller waits for response | Caller handles the error | API GW, ALB, direct Lambda invoke |
| **Asynchronous** | Lambda returns 202 and processes later | Automatic retry 2x + DLQ | S3, SNS, EventBridge, CloudWatch |
| **Event Source Mapping** | Lambda polls the source | Retry until expiry + DLQ/bisect | SQS, Kinesis, DynamoDB Streams, Kafka |

### Lambda Concurrency

```
Account Concurrency = 1,000 (default, increasable)

                ┌─ Reserved Concurrency (guaranteed for function X)
                │   [blocks others' concurrency]
Function Pool  ─┤
                └─ Unreserved Concurrency (shared among the rest)

Provisioned Concurrency:
  Pre-warms N execution environments → eliminates cold start
  Charged per hour (even without invocations)
  Required for: latency-sensitive applications (interactive APIs)
```

**Burst Limit (per region):**
- Initial scaling: 3,000 concurrent executions (us-east-1, us-west-2, eu-west-1)
- Smaller regions: 500-1,000 initial
- Expansion: +500/minute after burst

### Cold Start

Occurs when Lambda needs to create a new execution environment:
1. Download the package (code + layers)
2. Initialize the runtime
3. Run initialization code (outside the handler)

**Mitigations:**
- **Provisioned Concurrency**: pre-warmed environments (additional cost)
- **Lambda SnapStart** (Java): snapshot of the environment after initialization; restores instead of re-initializing (**Java 11+ only**)
- Keep package small; avoid heavy imports in the handler

### Lambda Layers

- Shared packages across multiple functions (libraries, dependencies, tools)
- Separation between application code and dependencies
- Versioned; can be shared across AWS accounts
- Limit: 5 layers per function, 250 MB total (uncompressed)

### Lambda in a VPC

```
Lambda (inside VPC):
  ├── Accesses private resources (RDS, ElastiCache, EC2)
  ├── Uses its own ENI (Hyperplane ENI — shared among functions in the same VPC/subnet/SG)
  └── To access the internet: needs NAT Gateway (public subnet + IGW)
      [Lambda in a VPC does NOT have internet access by default]
```

**Impact on cold start:** Lambda in a VPC uses Hyperplane ENI (not dedicated ENI since 2019) — minimal impact.

### Lambda Event Source Mapping (ESM)
For SQS, Kinesis, DynamoDB Streams, MSK:
- Lambda **polls** the source (not the source pushing)
- Processes in **batches** (configurable batch size)
- **Filtering**: processes only events with certain attributes (e.g., only `eventType = ORDER`)
- **Bisect on Error**: splits the batch in 2 on failure to isolate the problematic message
- **DLQ or Destination**: messages that fail all attempts go to SQS/SNS/S3

---

## Amazon API Gateway

### API Types

| Type | Use | Cost | Features |
|---|---|---|---|
| **REST API** | Full REST APIs | Higher | Cache, usage plans, request validation, X-Ray, WAF |
| **HTTP API** | Simple APIs + high throughput | ~71% lower | Lambda proxy, JWT, OIDC/OAuth2, fewer features |
| **WebSocket API** | Persistent bidirectional connections | Per connection + message | Chat, real-time alerts, $connect/$disconnect/$default |

### API Gateway REST — Components

```
API → Resource (/users) → Method (GET, POST, PUT, DELETE)
                              ├── Method Request (input validation, authorization)
                              ├── Integration Request (mapping → backend)
                              ├── Backend (Lambda, HTTP, AWS Service, Mock)
                              ├── Integration Response (mapping back)
                              └── Method Response (status codes, headers)
```

### Integration Types

| Type | How it works |
|---|---|
| **Lambda Proxy** | API GW passes the complete event to Lambda; Lambda returns response in the expected format |
| **Lambda Custom** | You define mapping templates (Velocity) to transform request/response |
| **HTTP Proxy** | Proxies to an external HTTP endpoint |
| **HTTP Custom** | Proxies to HTTP with transformation |
| **AWS Service** | Directly integrates with an AWS service (e.g., SQS SendMessage, DynamoDB PutItem) |
| **Mock** | Returns a response without a real backend (for testing) |

### Authorizers

| Type | How it works | Cache |
|---|---|---|
| **Lambda Authorizer** | Lambda receives token/header, returns IAM policy (Allow/Deny) | Configurable TTL (0-3600s) |
| **Cognito User Pool** | Validates Cognito User Pool JWT token | Automatic via token |
| **IAM Authorization** | Signs requests with AWS SigV4 (for internal AWS clients) | N/A |

### Throttling

- **Account limit**: 10,000 RPS + 5,000 burst (REST API)
- **Usage Plans**: rate (RPS) and quota (requests/day or week) per client via API Key
- HTTP 429 when throttled
- Throttling can be configured per stage and per method

### API Gateway Cache
- Per stage; default TTL 300s (5 min), up to 3,600s
- Cache key: configurable query strings and headers
- Invalidate per request: `Cache-Control: max-age=0` + required permission
- Sizes: 0.5 GB to 237 GB

### Stages and Deploy
- API is not available until you make a **deployment to a stage**
- Stage variables: like environment variables for stages (e.g., backend endpoint changes per stage)
- **Canary Deployments**: send % of the stage's traffic to a new version

---

## AWS SAM (Serverless Application Model)

Framework for IaC of serverless applications:
```yaml
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      Runtime: python3.12
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /hello
            Method: GET
```
`sam build && sam deploy --guided` → creates/updates CloudFormation stack

---

## Typical Serverless Architecture

```
Client
  └── API Gateway (REST/HTTP API)
        ├── Authorizer: Lambda / Cognito
        └── Integration: Lambda Proxy
              ├── Lambda A (GET /users)    → DynamoDB
              ├── Lambda B (POST /orders)  → DynamoDB + SNS (async)
              └── Lambda C (GET /reports)  → S3 Select / Athena

Async:
  SNS → SQS → Lambda (processor) → SES (email)
  EventBridge → Lambda (scheduler) → Reports in S3

Monitoring:
  CloudWatch Logs (automatic)
  X-Ray (distributed tracing)
```

---

## Exam Tips

- Lambda does **not** have state between invocations — use DynamoDB/ElastiCache for state
- `/tmp` persists only for the life of the execution environment (not between different invocations)
- Lambda is **free** up to 1 million invocations and 400,000 GB-seconds/month
- **Reserved Concurrency = 0** → function effectively disabled
- API Gateway HTTP API does NOT support: response caching, request validation, native WAF, UsagePlan/ApiKey
- Lambda SnapStart: Java only; snapshot after init phase; restored with `CRaC` (Coordinated Restore at Checkpoint)
- SQS with Lambda: queue VisibilityTimeout must be >= 6x the Lambda function timeout
- Lambda layers vs container image: container image (up to 10 GB) allows packaging everything; does not use layers
- Event Source Mapping with Kinesis/DynamoDB Streams: Lambda processes shards in parallel (1 concurrent invocation per shard by default)
- API Gateway cannot be accessed directly from within a VPC without a VPC Link or Resource Policy
