# Use Cases — Module 09: Decoupling (SQS, SNS, EventBridge)

## Case 1: Fan-Out with SNS + SQS for Order Processing

**Scenario:** E-commerce needs each new order to trigger: inventory update, invoice generation, and confirmation email — independently.

**Architecture:**
```
Order Service (Producer)
  └── SNS Topic: order-events
        ├── SQS Queue: inventory-queue → Lambda: InventoryService
        │     └── [FilterPolicy: {eventType: ["order.created"]}]
        │           └── DLQ: inventory-dlq (maxReceiveCount=3)
        │
        ├── SQS Queue: invoice-queue → Lambda: InvoiceService
        │     └── [FilterPolicy: {eventType: ["order.created", "order.completed"]}]
        │           └── DLQ: invoice-dlq
        │
        └── Lambda: EmailService (direct) → SES
              └── [FilterPolicy: {eventType: ["order.created"]}]

Benefits:
✓ Order Service does not know the consumers
✓ Failure in InvoiceService does not affect InventoryService
✓ Each queue has its own DLQ and retry
✓ Add new consumer = new SQS subscription (zero impact on others)
```

---

## Case 2: Asynchronous Worker with SQS + Auto Scaling

**Scenario:** Video processing system. Users upload videos and they need to be transcoded. Load varies greatly throughout the day.

**Architecture:**
```
S3 (upload) → S3 Event Notification → SQS Queue: video-transcode
                                              │
                                        SNS Alarm (CW metric)
                                              │
                              ApproximateNumberOfMessagesVisible ÷ FleetSize
                                              │
                                    ASG Target Tracking Policy
                                              │
                                Auto Scale EC2 Workers (min=1, max=20)
                                              │
                        EC2 Worker: polling SQS → transcode → S3 (output)
```

**Why not Lambda?** Transcoding can take 30+ minutes (Lambda max = 15min). EC2 with ASG based on SQS metric is the standard for long-duration workloads.

**Cost optimization:** Workers can be Spot Instances (up to 90% discount). If spot is interrupted, the SQS message reappears after VisibilityTimeout → another worker picks it up.

---

## Case 3: IoT Pipeline with Kinesis + Lambda

**Scenario:** 10,000 IoT sensors send temperature data every second. Data needs to be stored in S3 and alerts generated in real time for abnormal temperatures.

**Architecture:**
```
IoT Sensors (10,000 × 1 msg/s = 10K msgs/s)
  └── AWS IoT Core (MQTT)
        └── IoT Rule → Kinesis Data Stream (10 shards × 1K req/s = 10K/s)
                            ├── Lambda Consumer (Enhanced Fan-Out)
                            │     └── Analyzes temperature in real-time
                            │           └── > 80°C → SNS → PagerDuty
                            │
                            └── Kinesis Data Firehose
                                  └── (buffer 60s) → S3 (Parquet)
                                        └── Glue Catalog → Athena queries
```

**KDS vs Firehose:** KDS for real-time alerts (Lambda, < 200ms). Firehose for batch ingestion into S3 (near real-time, no consumer code).

---

## Case 4: Event-Driven with EventBridge for Operations Automation

**Scenario:** Ops team wants automations: when EC2 instances scale, notify the team; when an IAM user is created, verify policies; when code is updated in CodePipeline, update the wiki.

**EventBridge Rules:**
```
Default Event Bus (AWS events)
  ├── Rule 1: EC2 Instance State Change → RUNNING
  │     └── Target: Lambda → Slack webhook ("New instance i-xxx in us-east-1")
  │
  ├── Rule 2: IAM CreateUser API (via CloudTrail)
  │     └── Target: Lambda → IAM Compliance Check → SNS if violation
  │
  └── Rule 3: CodePipeline → Execution Succeeded
        └── Target: Step Functions → Confluence API Update

Custom Event Bus: app-events
  └── PutEvents → application custom events
        ├── Rule: source = "app.orders" → Step Functions (complex workflows)
        └── Rule: source = "app.billing" → Firehose → S3 (audit log)
```

---

## Case 5: Decoupling with Amazon MQ for Legacy System Migration

**Scenario:** Legacy banking system in Java uses ActiveMQ for communication between microservices. Company wants to move to AWS without rewriting the code.

**Lift-and-Shift Strategy:**
```
BEFORE (on-premises):
  ServiceA (AMQP) → ActiveMQ Broker → ServiceB (AMQP)
                                     → ServiceC (STOMP)

AFTER (AWS - Amazon MQ):
  ServiceA (AMQP) → Amazon MQ (Active/Standby) → ServiceB (AMQP)
                    ├── Broker 1 (us-east-1a) Active       → ServiceC (STOMP)
                    └── Broker 2 (us-east-1b) Standby
```

**Incremental modernization strategy:**
```
Phase 2 (Future):
  ServiceA → Amazon MQ → Bridge Lambda → SNS/SQS
  [Lambda consumes from MQ and republishes to SNS]
  [New services use SQS/SNS; legacy ones continue with MQ]
  [Gradual migration without big-bang]
```

**Why not go straight to SQS?** Production code uses AMQP/STOMP client libraries. Changing to the SQS SDK would require significant refactoring and testing. Amazon MQ = zero code changes.
