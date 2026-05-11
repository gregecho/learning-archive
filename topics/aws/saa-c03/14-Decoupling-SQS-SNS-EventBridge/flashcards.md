# Flashcards — Module 09: Decoupling (SQS, SNS, EventBridge)

---

**Q:** What is the default SQS VisibilityTimeout and why is it important?
**A:** Default: **30 seconds** (range: 0s to 12h). After a message is read, it becomes "invisible" for that time. If not deleted within the timeout, it reappears in the queue. Must be >= maximum processing time to avoid duplicate reprocessing

---

**Q:** What is the maximum throughput of an SQS FIFO queue?
**A:** 300 TPS (transactions per second) without batching. With batching of up to 10 messages: **3,000 TPS**. Without high-scale batching, if you need more → use SQS Standard (nearly unlimited) but lose ordering guarantees

---

**Q:** What is the maximum message retention period in SQS?
**A:** **14 days** (default: 4 days). Minimum: 1 minute. After the period, messages are automatically deleted even without being consumed

---

**Q:** What is SQS Long Polling and why use it?
**A:** Consumer waits up to `waitTimeSeconds` (maximum **20 seconds**) for available messages before returning. Reduces empty requests (cost), reduces latency. Short Polling returns immediately (even without messages) — more expensive and inefficient

---

**Q:** What is a Dead Letter Queue (DLQ) and when does a message go to it?
**A:** A separate queue for messages that failed processing. A message goes to the DLQ when the `ReceiveCount` exceeds the `maxReceiveCount` configured in the redrive policy. Serves to isolate "poison pills" (unprocessable messages) for analysis

---

**Q:** What is the maximum message size in SQS?
**A:** **256 KB** per message. For larger messages, use the "S3 + SQS" pattern: store the payload in S3 and put only the S3 object reference in the SQS message (via SQS Extended Client Library)

---

**Q:** What is Delay Queue in SQS?
**A:** Queue with delivery delay configured (0 to **15 minutes**). Published messages remain invisible for that period before appearing to consumers. Message Timer allows per-message delay (overrides the queue delay)

---

**Q:** What is SNS Message Filtering and how does it work?
**A:** Each SNS subscription can have a FilterPolicy (JSON with conditions on message attributes). Only messages matching the filter are delivered to that subscription. Example: `{"eventType": ["order.completed", "order.refunded"]}` — subscription only receives those types

---

**Q:** What is an SNS FIFO Topic? What are the limitations?
**A:** SNS FIFO guarantees ordering and deduplication. Only SQS FIFO Queues can subscribe to SNS FIFO Topics. Throughput limited to 300 TPS (3,000 with batching) — same limit as SQS FIFO. Does not integrate with Lambda, email, HTTP directly (only SQS FIFO)

---

**Q:** What is the difference between EventBridge Default Bus, Custom Bus, and Partner Bus?
**A:** Default Bus: events from AWS services (CloudTrail, EC2, RDS, etc.). Custom Bus: events from your own application (PutEvents API). Partner Bus: events from SaaS partners (Datadog, Salesforce, Zendesk, etc.) directly in EventBridge without needing API polling

---

**Q:** What is the EventBridge Schema Registry?
**A:** Automatically discovers and stores event schemas. Allows generating binding code (Java, Python, TypeScript) to serialize/deserialize events type-safely. Facilitates event-driven development with type safety

---

**Q:** What is the capacity per shard in Kinesis Data Streams?
**A:** Input: **1 MB/s** or 1,000 records/s per shard. Output: **2 MB/s** per shard (shared across consumers) or 2 MB/s per consumer with Enhanced Fan-Out (dedicated HTTP/2 push)

---

**Q:** How long does Kinesis Data Streams retain data?
**A:** Default: **24 hours**. Can be extended to up to **365 days** (with additional cost). Allows multiple consumers to read the same stream at different times (replay)

---

**Q:** What is the latency difference between Kinesis Data Streams and Kinesis Firehose?
**A:** Kinesis Data Streams: latency of ~200ms (real-time). Kinesis Firehose: **near real-time** — buffer of 60 seconds (minimum) or 1 MB before delivering to destination (S3, Redshift, OpenSearch, Splunk). Firehose does not allow direct stream access or replay

---

**Q:** What is Kinesis Producer Library (KPL) and what is the benefit?
**A:** High-level library for Kinesis producers. Implements batching (PutRecords), retry with backoff, compression, and integrated monitoring. Increases throughput and efficiency compared to direct SDK. Requires decompression on the consumer side via KCL

---

**Q:** For which use case is Amazon MQ the correct service?
**A:** Lift-and-shift migration of existing applications that use message brokers with standard protocols: **AMQP, MQTT, STOMP, OpenWire**. Supports managed ActiveMQ and RabbitMQ. If you are creating a new application, prefer SQS/SNS (more scalable and managed)

---

**Q:** What is the "fan-out" architecture pattern with SNS and SQS?
**A:** Publish 1 message to an SNS Topic → multiple SQS queues (or Lambda, HTTP) subscribe. Each subscriber processes independently, can have its own DLQ, its own retry. Decouples the publisher from multiple consumers

---

**Q:** What is "at-least-once delivery" in SQS Standard?
**A:** SQS Standard guarantees that the message is delivered **at least once** — it may be delivered more than once (rare duplication). Applications should be **idempotent** (process the same message multiple times without side effects). For "exactly once": use SQS FIFO with deduplication ID

---

**Q:** How to integrate SQS with Auto Scaling to scale consumers based on queue depth?
**A:** CloudWatch Alarm based on `ApproximateNumberOfMessagesVisible` (or `NumberOfMessagesSent` / instances) → Step Scaling or Target Tracking on the Auto Scaling Group. Target: e.g., keep <= 100 messages per instance. ECS can also scale tasks with this custom metric

---

**Q:** What is EventBridge Pipe?
**A:** Point-to-point connection between a source (SQS, Kinesis, DynamoDB Streams, Kafka) and a target (Lambda, Step Functions, EventBridge Bus), with optional filtering and enrichment in between. Simplifies event pipelines without an intermediate Lambda just for routing
