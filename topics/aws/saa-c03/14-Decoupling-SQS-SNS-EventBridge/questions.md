# Exam Questions — Module 09: Decoupling (SQS, SNS, EventBridge)

<!-- SAA-C03 Domain: Design Resilient Architectures / High-Performing Architectures -->

---

**1.** An application processes orders and wants to ensure that each order is processed exactly once, in the order of arrival. Which SQS queue to use?

- A) SQS Standard with Dead Letter Queue
- B) SQS FIFO with deduplication ID
- C) SQS Standard with long VisibilityTimeout
- D) SQS FIFO with Message Group ID per order type

<details>
<summary>Answer</summary>
**B — SQS FIFO with deduplication ID**
SQS FIFO guarantees: **ordering** (First-In-First-Out) and **deduplication** (exactly one delivery). Message Deduplication ID prevents duplicate processing within a 5-minute window. Standard Queue offers at-least-once delivery (may duplicate) and best-effort ordering (may reorder). For exactly once + ordering: FIFO is mandatory.
</details>

---

**2.** A Lambda function takes an average of 90 seconds to process an SQS message. Which configuration is critical to avoid duplicate processing?

- A) Increase Message Retention Period to > 90 seconds
- B) Configure VisibilityTimeout > 90 seconds (e.g., 120s)
- C) Use FIFO queue to avoid duplication
- D) Enable Long Polling on the consumer

<details>
<summary>Answer</summary>
**B — VisibilityTimeout > processing time**
VisibilityTimeout defines how long the message stays "invisible" to other consumers after being read. If processing takes 90s and VisibilityTimeout is the default 30s, the message returns to the queue before being confirmed (deleted), causing reprocessing. Rule: VisibilityTimeout >= maximum processing timeout.
</details>

---

**3.** An application processes messages but after 3 attempts, messages continue to fail. How to prevent them from looping in the queue indefinitely?

- A) Configure Message Retention Period of 1 hour
- B) Use SQS FIFO with deduplication
- C) Configure Dead Letter Queue (DLQ) with maxReceiveCount = 3
- D) Decrease VisibilityTimeout to detect failure faster

<details>
<summary>Answer</summary>
**C — DLQ with maxReceiveCount**
Dead Letter Queue receives messages that exceeded the `maxReceiveCount` of processing attempts. After 3 failures, the message is moved to the DLQ for analysis without impacting the normal flow. Message Retention is how long the message exists in the queue (unrelated to attempts). DLQ is the standard solution for poison pills.
</details>

---

**4.** What is the difference between SQS Long Polling and Short Polling?

- A) Long Polling returns immediately even without messages; Short Polling waits
- B) Long Polling waits until messages arrive (waitTimeSeconds > 0) or timeout; Short Polling returns immediately
- C) Short Polling is recommended for production; Long Polling for development
- D) Long Polling works only with FIFO queues

<details>
<summary>Answer</summary>
**B — Correct**
Short Polling: returns immediately (even without messages) → multiple empty requests = unnecessary cost. Long Polling: Consumer waits up to `waitTimeSeconds` (maximum 20 seconds) for messages — reduces number of requests, cost, and consumer CPU. Long Polling is recommended for production.
</details>

---

**5.** A system needs to send the same "new order" notification to 3 different systems: inventory, billing, and email notification. Which architecture to use?

- A) 3 separate SQS queues with each system polling
- B) SNS Topic → 3 SQS Queues (fan-out pattern)
- C) EventBridge with 3 different rules
- D) Kinesis Data Stream with 3 consumers

<details>
<summary>Answer</summary>
**B — Fan-out with SNS → SQS**
Classic fan-out: publish one message to SNS and have multiple SQS queues as subscriptions. Each system consumes from its own queue independently. Advantages: complete decoupling, systems can be slow without affecting the publisher, DLQ per system, independent retry. EventBridge also works but SNS→SQS is simpler for this case.
</details>

---

**6.** An application publishes events to SNS with multiple subscribers: Lambda A, Lambda B, SQS C. Only Lambda A should receive events of type `order.completed`. How to filter?

- A) Lambda A must filter internally when receiving all events
- B) SNS Message Filtering on Lambda A's subscription with FilterPolicy based on attributes
- C) Create a separate SNS Topic only for order.completed
- D) EventBridge rule with event pattern

<details>
<summary>Answer</summary>
**B — SNS Message Filtering**
SNS Message Filtering (FilterPolicy) allows each subscription to specify a JSON with conditions to receive only messages matching the attributes. E.g., `{"eventType": ["order.completed"]}`. Lambda A receives only `order.completed`; other subscribers receive their own filters. Avoids unnecessary processing.
</details>

---

**7.** A company uses multiple AWS and SaaS services and wants to create automations (e.g., "when RDS CPU > 90%, create snapshot and notify") without writing polling code. Which service to use?

- A) CloudWatch Events (deprecated)
- B) Amazon EventBridge
- C) SNS with CloudWatch Alarm
- D) Step Functions with Lambda polling

<details>
<summary>Answer</summary>
**B — Amazon EventBridge**
EventBridge is the evolution of CloudWatch Events. Receives events from over 200 AWS services, SaaS partners (Salesforce, Datadog, etc.), and custom apps. Rules with Event Patterns filter and route to targets (Lambda, Step Functions, SQS, SNS, etc.). CloudWatch Alarm + SNS works for specific metrics, but EventBridge is more flexible for state events.
</details>

---

**8.** What is the main difference between Kinesis Data Streams and SQS?

- A) Kinesis is for real-time streaming data with retention and replay; SQS is for message queues with deletion after consumption
- B) SQS supports more simultaneous consumers than Kinesis
- C) Kinesis is cheaper than SQS for all use cases
- D) SQS has lower latency than Kinesis

<details>
<summary>Answer</summary>
**A — Correct**
Kinesis Data Streams: data retained for 1-365 days, multiple consumers read the same data (replay), ordered by shard, base64 bytes. SQS: message is deleted after consumption confirmation (at-most-once with MessageVisibility, at-least-once by default), no native replay, ordering only in FIFO. Kinesis for analytics pipelines; SQS for task queues.
</details>

---

**9.** A company processes 1 million transactions per second for real-time fraud analysis. Which streaming service to use?

- A) SQS FIFO (3,000 TPS by default)
- B) SNS with filters per transaction type
- C) Kinesis Data Streams with sufficient shards
- D) Amazon MQ (ActiveMQ) cluster

<details>
<summary>Answer</summary>
**C — Kinesis Data Streams**
Kinesis scales by **shards**: each shard supports 1 MB/s input and 2 MB/s output. For 1M TPS, add sufficient shards. Kinesis Data Analytics can process in real time. SQS FIFO has a limit of 3,000 TPS (with batching). MQ is for migrating legacy systems with AMQP/STOMP/MQTT protocols.
</details>

---

**10.** What is "Enhanced Fan-Out" in Kinesis Data Streams?

- A) Allows sending data from multiple sources to a single stream
- B) Allows each registered consumer to receive dedicated 2 MB/s output per shard
- C) Enables multiple partitions per shard for higher input throughput
- D) Automatically distributes data across multiple Kinesis Firehose deliveries

<details>
<summary>Answer</summary>
**B — 2 MB/s dedicated per consumer per shard**
Without Enhanced Fan-Out: output is shared across all consumers (2 MB/s total per shard divided by N consumers). With Enhanced Fan-Out: each registered consumer via `SubscribeToShard` receives **2 MB/s dedicated per shard** via HTTP/2 push (instead of polling). Ideal for multiple consumers processing the same stream in parallel at high speed.
</details>

---

**11.** What is the difference between Kinesis Data Streams and Kinesis Data Firehose?

- A) Firehose needs custom consumers (polling); Streams delivers directly to destinations
- B) Streams require shard and consumer management; Firehose is fully managed and delivers to destinations (S3, Redshift, OpenSearch)
- C) Firehose supports data replay; Streams does not
- D) Streams is serverless; Firehose requires capacity provisioning

<details>
<summary>Answer</summary>
**B — Correct**
Kinesis Data Streams: you manage shards, write consumers (KCL, Lambda), data stays in the stream for 1-365 days (replay possible). Kinesis Firehose: fully managed, no shards to manage, automatic delivery to S3/Redshift/OpenSearch/Splunk/HTTP endpoints, near real-time (buffer of 60s or 1 MB), no replay. Firehose for simple ingest-to-destination pipeline.
</details>

---

**12.** A company migrated from on-premises RabbitMQ to AWS. They want to keep the application code using the AMQP protocol with no changes. Which AWS service?

- A) Amazon SQS with AMQP adapter
- B) Amazon MQ (managed RabbitMQ or ActiveMQ)
- C) Amazon Kinesis with AMQP SDK
- D) SNS with FIFO topics

<details>
<summary>Answer</summary>
**B — Amazon MQ**
Amazon MQ offers managed ActiveMQ and RabbitMQ, compatible with standard protocols: AMQP, MQTT, STOMP, OpenWire, WebSocket. Allows lift-and-shift of applications with legacy brokers without rewriting. SQS/SNS are proprietary AWS APIs. Use Amazon MQ when existing code needs the native AMQP/MQTT protocol.
</details>

---

**13.** What purpose do EventBridge Archive and Replay serve?

- A) Compress old events to reduce storage cost
- B) Archive events from the event bus to retransmit them (replay) in case of a bug in the consumer
- C) Create snapshots of the event bus for disaster recovery
- D) Replicate events between regions automatically

<details>
<summary>Answer</summary>
**B — Archive and retransmit events**
Archive: saves events from an event bus with configurable retention (indefinite or N days). Replay: retransmits archived events to the event bus (or another target), choosing a time window. Useful for: fixing a bug in a consumer and reprocessing historical events, testing with real production data, auditing event sequences.
</details>

---

**14.** Which service to use when you need guaranteed ordered, exactly-once delivery for messages between microservices, with throughput of 300 messages/second?

- A) SQS Standard Queue
- B) SNS FIFO Topic → SQS FIFO Queue
- C) EventBridge with retry policy
- D) Kinesis Data Streams (1 shard)

<details>
<summary>Answer</summary>
**B — SNS FIFO → SQS FIFO**
SQS FIFO guarantees ordering and deduplication, 300 TPS (or 3,000 TPS with batching). For fan-out with FIFO semantics: SNS FIFO Topic subscribes SQS FIFO Queues. EventBridge does not guarantee ordering. Standard SQS does not guarantee ordering. Kinesis could work with 1 shard and a single consumer, but queue semantics (delete after consumption) do not exist in Kinesis.
</details>

---

**15.** An application needs a 5-minute delay before messages enter the queue for processing. Which SQS configuration to use?

- A) VisibilityTimeout of 300 seconds
- B) Message Timer (per-message delay) or Delay Queue (delay at queue creation)
- C) Dead Letter Queue with maxReceiveCount = 0
- D) Long Polling with waitTimeSeconds = 300

<details>
<summary>Answer</summary>
**B — Delay Queue or Message Timer**
**Delay Queue**: delay configured on the queue (default 0, maximum 15 minutes) — all messages wait before appearing to consumers. **Message Timer**: per-message delay overrides the queue delay. VisibilityTimeout hides a message **already received**, not before entering. Long Polling maximum is 20 seconds (not 300).
</details>
