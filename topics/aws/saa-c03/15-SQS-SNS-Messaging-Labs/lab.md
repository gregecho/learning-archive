# Practical Lab — SQS and SNS: Queues, DLQ and Fan-out (Module 10)

> **Region:** us-east-1 | **Estimated cost:** ~$0 (first million messages free/month)  
> **Prerequisites:** AWS CLI configured, Python 3.8+

---

## Objective

Practice SQS Standard and FIFO, Dead Letter Queue, visibility timeout, SNS fan-out, and SQS → Lambda integration.

---

## Part 1 — SQS Standard + DLQ

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create DLQ first
DLQ_URL=$(aws sqs create-queue \
  --queue-name "lab-orders-dlq" \
  --attributes "MessageRetentionPeriod=1209600" \
  --query 'QueueUrl' --output text)

DLQ_ARN=$(aws sqs get-queue-attributes \
  --queue-url "$DLQ_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' --output text)

echo "DLQ created: $DLQ_ARN"

# Create main queue with redrive policy
QUEUE_URL=$(aws sqs create-queue \
  --queue-name "lab-orders" \
  --attributes "{
    \"VisibilityTimeout\": \"30\",
    \"ReceiveMessageWaitTimeSeconds\": \"20\",
    \"MessageRetentionPeriod\": \"345600\",
    \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARN}\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"
  }" \
  --query 'QueueUrl' --output text)

echo "Main queue created: $QUEUE_URL"

# Verify attributes
aws sqs get-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attribute-names All \
  --query 'Attributes.[VisibilityTimeout, ReceiveMessageWaitTimeSeconds, RedrivePolicy]' \
  --output json | python3 -m json.tool
```

---

## Part 2 — Produce and Consume Messages

```python
# sqs_lab.py
import boto3
import json
import time

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = "REPLACE_WITH_QUEUE_URL"  # terraform output or CLI

# ──────────────────────────────────────────
# 1. Send messages in batch
# ──────────────────────────────────────────
orders = [
    {"order_id": f"ORD-{i:03}", "customer": f"CUST-{i % 5:03}",
     "product": f"Product {i}", "amount": i * 50.0}
    for i in range(10)
]

entries = [
    {
        'Id': str(i),
        'MessageBody': json.dumps(p),
        'MessageAttributes': {
            'priority': {
                'DataType': 'String',
                'StringValue': 'high' if p['amount'] > 200 else 'normal'
            }
        }
    }
    for i, p in enumerate(orders)
]

# Batch of 10 (maximum per call)
resp = sqs.send_message_batch(QueueUrl=QUEUE_URL, Entries=entries)
print(f"Sent: {len(resp['Successful'])} messages")

# ──────────────────────────────────────────
# 2. Consume messages (long polling)
# ──────────────────────────────────────────
processed = 0
MAX = 10

print("\nConsuming messages...")
while processed < MAX:
    resp = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=5,
        MessageAttributeNames=['All']
    )
    
    messages = resp.get('Messages', [])
    if not messages:
        print("Queue empty.")
        break
    
    for msg in messages:
        body = json.loads(msg['Body'])
        priority = msg.get('MessageAttributes', {}).get('priority', {}).get('StringValue', 'normal')
        
        print(f"  Processing: {body['order_id']} | priority={priority}")
        time.sleep(0.1)  # simulate processing
        
        # Delete after processing
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        processed += 1

print(f"\nTotal processed: {processed}")

# ──────────────────────────────────────────
# 3. Simulate a failing message (goes to DLQ)
# ──────────────────────────────────────────
sqs.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=json.dumps({"order_id": "ORD-FAIL", "type": "invalid"})
)
print("\nFailure message sent (maxReceive=3 → DLQ)")
print("Receive without deleting 3x to send to DLQ...")

DLQ_URL = QUEUE_URL.replace('lab-orders', 'lab-orders-dlq')
for attempt in range(3):
    msgs = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1
    ).get('Messages', [])
    
    for msg in msgs:
        body = json.loads(msg['Body'])
        if body.get('type') == 'invalid':
            print(f"  Attempt {attempt+1}: pretending failure (NOT deleting)")
            # Wait for visibility timeout to expire (30s = wait or use ChangeMessageVisibility)
            sqs.change_message_visibility(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg['ReceiptHandle'],
                VisibilityTimeout=0  # makes visible immediately for next attempt
            )
```

```bash
# Replace URL and run
QUEUE_URL=$(aws sqs get-queue-url --queue-name "lab-orders" --query 'QueueUrl' --output text)
sed -i "s|REPLACE_WITH_QUEUE_URL|$QUEUE_URL|" sqs_lab.py
python3 sqs_lab.py
```

---

## Part 3 — SQS FIFO

```bash
# Create FIFO queue (name must end in .fifo)
FIFO_URL=$(aws sqs create-queue \
  --queue-name "lab-payments.fifo" \
  --attributes "{
    \"FifoQueue\": \"true\",
    \"ContentBasedDeduplication\": \"false\",
    \"VisibilityTimeout\": \"30\",
    \"ReceiveMessageWaitTimeSeconds\": \"10\",
    \"DeduplicationScope\": \"messageGroup\",
    \"FifoThroughputLimit\": \"perMessageGroupId\"
  }" \
  --query 'QueueUrl' --output text)

echo "FIFO created: $FIFO_URL"

# Send messages with MessageGroupId and MessageDeduplicationId
for i in 1 2 3 4 5; do
  aws sqs send-message \
    --queue-url "$FIFO_URL" \
    --message-body "{\"payment_id\": \"PAY-$i\", \"amount\": $((i*100))}" \
    --message-group-id "customer-001" \
    --message-deduplication-id "pay-cust001-seq-$i"
done

# Messages arrive IN ORDER of sending for the same MessageGroupId
echo "5 payments sent in order for customer-001"

# Consume FIFO
aws sqs receive-message \
  --queue-url "$FIFO_URL" \
  --max-number-of-messages 5 \
  --query 'Messages[*].Body' \
  --output text
```

---

## Part 4 — SNS Fan-out to SQS

```bash
# Create SNS Topic
SNS_ARN=$(aws sns create-topic \
  --name "lab-purchase-events" \
  --query 'TopicArn' --output text)

# Create queues to subscribe
INVENTORY_QUEUE_URL=$(aws sqs create-queue \
  --queue-name "lab-inventory-queue" \
  --query 'QueueUrl' --output text)
INVENTORY_QUEUE_ARN=$(aws sqs get-queue-attributes \
  --queue-url "$INVENTORY_QUEUE_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' --output text)

EMAIL_QUEUE_URL=$(aws sqs create-queue \
  --queue-name "lab-email-queue" \
  --query 'QueueUrl' --output text)
EMAIL_QUEUE_ARN=$(aws sqs get-queue-attributes \
  --queue-url "$EMAIL_QUEUE_URL" \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' --output text)

# Policy for SQS to accept messages from SNS
aws sqs set-queue-attributes \
  --queue-url "$INVENTORY_QUEUE_URL" \
  --attributes "{
    \"Policy\": \"{\\\"Statement\\\":[{\\\"Effect\\\":\\\"Allow\\\",\\\"Principal\\\":{\\\"Service\\\":\\\"sns.amazonaws.com\\\"},\\\"Action\\\":\\\"sqs:SendMessage\\\",\\\"Resource\\\":\\\"${INVENTORY_QUEUE_ARN}\\\",\\\"Condition\\\":{\\\"ArnEquals\\\":{\\\"aws:SourceArn\\\":\\\"${SNS_ARN}\\\"}}}]}\"
  }"

aws sqs set-queue-attributes \
  --queue-url "$EMAIL_QUEUE_URL" \
  --attributes "{
    \"Policy\": \"{\\\"Statement\\\":[{\\\"Effect\\\":\\\"Allow\\\",\\\"Principal\\\":{\\\"Service\\\":\\\"sns.amazonaws.com\\\"},\\\"Action\\\":\\\"sqs:SendMessage\\\",\\\"Resource\\\":\\\"${EMAIL_QUEUE_ARN}\\\",\\\"Condition\\\":{\\\"ArnEquals\\\":{\\\"aws:SourceArn\\\":\\\"${SNS_ARN}\\\"}}}]}\"
  }"

# Subscribe queues to the topic
aws sns subscribe \
  --topic-arn "$SNS_ARN" \
  --protocol sqs \
  --notification-endpoint "$INVENTORY_QUEUE_ARN"

aws sns subscribe \
  --topic-arn "$SNS_ARN" \
  --protocol sqs \
  --notification-endpoint "$EMAIL_QUEUE_ARN"

# Publish message — goes to BOTH queues
aws sns publish \
  --topic-arn "$SNS_ARN" \
  --message '{"purchase_id":"P001","customer":"john@ex.com","total":350.00}' \
  --subject "New Purchase Confirmed"

sleep 5

# Check messages in queues
echo "Inventory Queue:"
aws sqs receive-message --queue-url "$INVENTORY_QUEUE_URL" \
  --query 'Messages[0].Body' --output text | python3 -m json.tool

echo "Email Queue:"
aws sqs receive-message --queue-url "$EMAIL_QUEUE_URL" \
  --query 'Messages[0].Body' --output text | python3 -m json.tool
```

---

## Cleanup

```bash
# Delete subscriptions and SNS
aws sns delete-topic --topic-arn "$SNS_ARN"
aws sqs delete-queue --queue-url "$INVENTORY_QUEUE_URL"
aws sqs delete-queue --queue-url "$EMAIL_QUEUE_URL"
aws sqs delete-queue --queue-url "$QUEUE_URL"
aws sqs delete-queue --queue-url "$DLQ_URL"
aws sqs delete-queue --queue-url "$FIFO_URL"

rm -f sqs_lab.py
```

---

## What You Learned

- **Visibility Timeout:** during processing the message is "invisible"; if not deleted, it returns to the queue
- **Long Polling (WaitTimeSeconds=20):** reduces empty calls by 99% vs short polling — ALWAYS prefer it
- **DLQ:** after `maxReceiveCount` failures, message is diverted to DLQ; set alarms on messages in the DLQ
- **FIFO:** guarantees strict ordering (FIFO), exactly-once via MessageDeduplicationId; max 300 TPS without batching
- **Standard:** at-least-once, out-of-order, practically unlimited throughput — for most cases
- **SNS fan-out:** publish once → multiple independent consumers; DLQ on SQS protects lost messages
