# Module 09 — Decoupling: SQS, SNS, EventBridge

## Why Decouple?

Tightly-coupled architectures create failure cascades: if the consumer is slow or failing, the producer stops. Messaging and event services introduce a buffer or router between producer and consumer, increasing resilience, independent scalability, and fault tolerance.

---

## Amazon SQS (Simple Queue Service)

Fully managed message queue service.

### Standard vs FIFO

| Feature | Standard | FIFO |
|---|---|---|
| Throughput | **Unlimited** | 300 TPS (without batching), 3,000 TPS (with batching of 10) |
| Order | Best-effort (may be out of order) | **Strict FIFO** (First In, First Out) |
| Deduplication | Duplicate delivery possible | **Exactly once** (deduplication window 5 min) |
| Naming | Any name | Must end in `.fifo` |
| Typical use | High throughput, tolerant of duplicates | Financial orders, sequential commands |

### Visibility Timeout
- When a message is received, it becomes **invisible** for a period (default: 30s, max: 12h)
- During this time, processing must complete and delete the message
- If processing fails and the timeout expires, the message reappears for another consumer
- **ChangeMessageVisibility**: extends the timeout if processing takes longer

### DLQ (Dead-Letter Queue)
- Messages that failed `maxReceiveCount` times are moved to the DLQ
- Allows inspecting and reprocessing problematic messages
- DLQ must be the same type as the source queue (FIFO → FIFO DLQ, Standard → Standard DLQ)
- **DLQ Redrive**: reprocess messages from the DLQ back to the source queue

### Long Polling
- `waitTimeSeconds` > 0 (max 20s): the receive request waits until a message is available or timeout
- Reduces empty API calls (and cost) vs. Short Polling (returns immediately, even without a message)
- **Enable Long Polling**: configure on the queue or on the `ReceiveMessage` call

### Other Key Configurations
| Parameter | Default | Maximum | Description |
|---|---|---|---|
| Message Retention | 4 days | 14 days | Time the message stays in the queue |
| Message Size | — | 256 KB | Per message (use S3 + SQS Extended Client for larger) |
| Delay Queue | 0 | 15 min | Delay before the message becomes visible |
| Receive Request Wait Time | 0 | 20s | Long polling window |

### SQS + Auto Scaling
- ASG scales based on `ApproximateNumberOfMessagesVisible` (via CloudWatch Custom Metric)
- Pattern: "worker" instances consume from the queue, ASG scales with the backlog

---

## Amazon SNS (Simple Notification Service)

Fully managed pub/sub service. Producers publish to **Topics**, Subscribers receive.

### Distribution Models
- **Fan-out**: 1 publication → multiple subscribers (SQS, Lambda, HTTP, Email, SMS, Mobile Push)
- Typically: application publishes to SNS → SNS distributes to multiple SQS queues (fan-out without coupling)

```
Purchase Event
    │
    ▼
SNS Topic: order-created
    ├── SQS: process-payment
    ├── SQS: update-inventory
    ├── SQS: send-email
    └── Lambda: update-analytics
```

### FIFO Topics
- Like FIFO SQS but for pub/sub
- Subscribers must be SQS FIFO Queues
- 300 publishes/s, ordered, no duplicates

### Message Filtering
- Each subscriber can have a **filter policy** (JSON) defining which message attributes to receive
- Reduces unnecessary processing at the subscriber
```json
{"event_type": ["ORDER_PLACED", "ORDER_FAILED"]}
```

### SNS vs SQS
| SNS | SQS |
|---|---|
| Pub/Sub (1 → N) | Queue (1:1 pull) |
| Push to subscribers | Consumers poll/pull |
| No message retention | Retention up to 14 days |
| Fan-out | Point-to-point |

---

## Amazon EventBridge

Serverless event bus. Evolution of CloudWatch Events.

### Event Buses
| Type | Description |
|---|---|
| **Default** | Events from AWS services (EC2 state-change, S3 object created, etc.) |
| **Custom** | You create, for your own application events |
| **Partner** | Events from SaaS partners (Zendesk, Datadog, PagerDuty, Auth0) |

### Rules
- Define **event pattern** (what triggers) + **target** (what executes)
- Targets: Lambda, SQS, SNS, Step Functions, Kinesis, CodePipeline, another account's EventBridge, and 20+ others
- **Schedule**: cron or rate-based rules (no event needed)
- **Event Archive**: archives all events (or filtered) for replay
- **Event Replay**: reprocesses archived events (useful for debugging and retroactive new consumers)

### Schema Registry
- Automatically discovers and registers event schemas
- Generates binding code (Java, Python, TypeScript) to work with typed events
- Validates events against schemas

### EventBridge vs SNS vs SQS
| Aspect | EventBridge | SNS | SQS |
|---|---|---|---|
| Model | Event bus (rules + targets) | Pub/Sub (topics) | Queue |
| Routing | Content-based filtering (JSON path) | Basic filter policies | N/A |
| Sources | AWS services, custom, SaaS partners | Your applications | — |
| Replay | Yes (archive + replay) | No | No |
| Targets | 20+ types | SQS, Lambda, HTTP, etc. | Pull by consumers |
| Use | Complex event orchestration | Simple fan-out | Buffer/decoupling |

---

## Amazon Kinesis

Platform for real-time streaming data processing.

### Kinesis Data Streams

- **Shards**: capacity unit (1 MB/s input, 2 MB/s output per shard)
- Retention: 24h default, up to 365 days
- **Producers**: SDK, Kinesis Agent, Kinesis Producer Library (KPL — batching + compression)
- **Consumers**: Lambda, Kinesis Data Analytics, KCL (Kinesis Client Library), Firehose
- **Enhanced Fan-Out**: 2 MB/s per consumer per shard (push via HTTP/2, vs default poll)
- **Partition Key**: determines which shard receives the record (similar to DynamoDB partition key — high cardinality avoids hot shards)

### Kinesis Data Firehose

- **Fully managed**, no shard administration (serverless)
- **Destinations**: S3, Redshift (via S3), OpenSearch, Splunk, DataDog, custom HTTP
- Not stored (streaming, no replay)
- **Buffer**: groups records before delivery (buffer size or buffer interval)
- Can apply transformations with Lambda before delivery
- **Firehose != Streams**: Firehose is near-real-time (seconds/minutes latency); Streams is real-time

### Kinesis Data Streams vs Firehose
| Feature | Data Streams | Data Firehose |
|---|---|---|
| Latency | Real-time (<200ms) | Near-real-time (60s–900s buffer) |
| Management | Manual (shards) | Serverless (automatic) |
| Replay | Yes (up to 365 days) | No |
| Destinations | Custom consumers | S3, Redshift, OpenSearch, etc. |
| Cost | Per shard-hour | Per GB ingested |

---

## Amazon MQ

Managed message broker compatible with open messaging protocols: **AMQP, MQTT, OpenWire, STOMP**.

- Supports **Apache ActiveMQ** and **RabbitMQ**
- Different from SQS/SNS (proprietary AWS protocols)
- Used for **lift-and-shift of existing applications** that already use ActiveMQ/RabbitMQ
- Deploy in 1 or 2 AZs (Active/Standby for HA)
- For new projects: prefer SQS/SNS (serverless, more scalable)

---

## Exam Tips

- **SQS + SNS fan-out** = classic decoupling pattern — SNS distributes to multiple SQS
- **SQS FIFO**: exactly-once + ordered, but limited to 300/3,000 TPS
- **Visibility Timeout** shorter than processing time = duplicates; longer = delay in redelivery
- **DLQ** is for messages that failed `maxReceiveCount` times — not for slow messages
- **Long Polling** (waitTimeSeconds=20) reduces cost and number of empty calls
- **EventBridge** is preferred over CloudWatch Events (EventBridge is the same thing, but with more features)
- EventBridge **archive + replay** = retroactive debugging and onboarding of new consumers
- **Kinesis Data Streams** for real-time analytics + replay; **Firehose** for near-real-time → S3/Redshift
- **Hot shard in Kinesis** = partition key with low cardinality (e.g., only "user"/"event") — distribute keys better
- **Amazon MQ** = lift-and-shift migration of ActiveMQ/RabbitMQ; for new projects, use SQS/SNS
