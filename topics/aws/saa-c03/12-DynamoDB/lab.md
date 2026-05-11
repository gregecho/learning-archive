# Practical Lab — DynamoDB: Modeling, GSI, DAX and Streams (Module 07)

> **Region:** us-east-1 | **Estimated cost:** ~$0 (on-demand mode + DAX ~$0.08/h — destroy after lab)  
> **Prerequisites:** AWS CLI configured, Python 3.8+, pip

---

## Objective

Practice NoSQL data modeling in DynamoDB, create GSIs, enable Streams, explore TTL, and understand the consistency model.

---

## Part 1 — Create Table with GSI and TTL

```bash
# Table: orders with GSI for customer queries
aws dynamodb create-table \
  --table-name "orders" \
  --attribute-definitions \
    "AttributeName=order_id,AttributeType=S" \
    "AttributeName=customer_id,AttributeType=S" \
    "AttributeName=order_date,AttributeType=S" \
  --key-schema \
    "AttributeName=order_id,KeyType=HASH" \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "customer-date-index",
      "KeySchema": [
        {"AttributeName": "customer_id", "KeyType": "HASH"},
        {"AttributeName": "order_date", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]' \
  --stream-specification "StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES"

# Enable TTL (expires_at field = Unix timestamp)
aws dynamodb update-time-to-live \
  --table-name "orders" \
  --time-to-live-specification "Enabled=true,AttributeName=expires_at"

aws dynamodb wait table-exists --table-name "orders"
echo "Orders table created!"

# Second table: cart with TTL (1-hour session)
aws dynamodb create-table \
  --table-name "cart" \
  --attribute-definitions \
    "AttributeName=session_id,AttributeType=S" \
    "AttributeName=item_id,AttributeType=S" \
  --key-schema \
    "AttributeName=session_id,KeyType=HASH" \
    "AttributeName=item_id,KeyType=RANGE" \
  --billing-mode PAY_PER_REQUEST

aws dynamodb update-time-to-live \
  --table-name "cart" \
  --time-to-live-specification "Enabled=true,AttributeName=expires_at"

aws dynamodb wait table-exists --table-name "cart"
echo "Cart table created!"
```

---

## Part 2 — CRUD Operations and Queries

```python
# dynamo_lab.py
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta, timezone
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
orders_table  = dynamodb.Table('orders')
cart_table = dynamodb.Table('cart')

# ──────────────────────────────────────────
# 1. PutItem — create orders
# ──────────────────────────────────────────
now = datetime.utcnow()
order_ids = []

for i, (customer, product, amount) in enumerate([
    ("CUST-001", "Notebook Pro",   3500.00),
    ("CUST-002", "Wireless Mouse",   89.90),
    ("CUST-001", "Keyboard",         350.00),
    ("CUST-003", "Monitor",        1200.00),
    ("CUST-001", "Headset",         180.00),
]):
    oid = str(uuid.uuid4())[:8]
    order_ids.append(oid)
    orders_table.put_item(Item={
        'order_id':   oid,
        'customer_id':  customer,
        'product':     product,
        'amount':       str(amount),
        'status':      'pending' if i % 2 == 0 else 'approved',
        'order_date': (now - timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S'),
        'expires_at':  int((now + timedelta(days=30)).timestamp()),
    })

print(f"Inserted {len(order_ids)} orders")

# ──────────────────────────────────────────
# 2. GetItem — lookup by HASH key
# ──────────────────────────────────────────
resp = orders_table.get_item(
    Key={'order_id': order_ids[0]},
    ConsistentRead=True  # Strongly consistent read
)
print(f"\nGetItem (consistent): {resp['Item']}")

# Without ConsistentRead = Eventually Consistent (default, cheaper)
resp2 = orders_table.get_item(Key={'order_id': order_ids[0]})
print(f"GetItem (eventual): {resp2['Item']['product']}")

# ──────────────────────────────────────────
# 3. Query via GSI: all orders for CUST-001
# ──────────────────────────────────────────
resp = orders_table.query(
    IndexName='customer-date-index',
    KeyConditionExpression=Key('customer_id').eq('CUST-001'),
    ScanIndexForward=False  # descending order by date
)
print(f"\nGSI Query (CUST-001): {len(resp['Items'])} orders")
for p in resp['Items']:
    print(f"  {p['order_date']} — {p['product']} — {p['status']}")

# ──────────────────────────────────────────
# 4. Query with range: recent orders for CUST-001
# ──────────────────────────────────────────
cutoff_date = (now - timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%S')
resp = orders_table.query(
    IndexName='customer-date-index',
    KeyConditionExpression=(
        Key('customer_id').eq('CUST-001') &
        Key('order_date').gt(cutoff_date)
    )
)
print(f"\nRecent orders CUST-001 (last 3 days): {len(resp['Items'])}")

# ──────────────────────────────────────────
# 5. UpdateItem — update status
# ──────────────────────────────────────────
orders_table.update_item(
    Key={'order_id': order_ids[0]},
    UpdateExpression='SET #s = :ns, updated_at = :ts',
    ExpressionAttributeNames={'#s': 'status'},
    ExpressionAttributeValues={':ns': 'shipped', ':ts': now.isoformat()},
    ConditionExpression=Attr('status').eq('pending')  # Conditional write
)
print(f"\nStatus conditionally updated: order {order_ids[0]} → shipped")

# ──────────────────────────────────────────
# 6. Scan with FilterExpression (less efficient than Query)
# ──────────────────────────────────────────
resp = orders_table.scan(
    FilterExpression=Attr('status').eq('approved'),
    Select='COUNT'
)
print(f"\nScan (status=approved): {resp['Count']} orders")

# ──────────────────────────────────────────
# 7. Cart with TTL (expires in 1 hour)
# ──────────────────────────────────────────
session = str(uuid.uuid4())[:8]
expires = int((now + timedelta(hours=1)).timestamp())

for item_id, product, qty in [("PROD-1", "Notebook", 1), ("PROD-2", "Mouse", 2)]:
    cart_table.put_item(Item={
        'session_id':  session,
        'item_id':    item_id,
        'product':    product,
        'quantity': qty,
        'expires_at': expires,
    })

print(f"\nCart {session}: 2 items (TTL in 1 hour)")

# ──────────────────────────────────────────
# 8. BatchWrite
# ──────────────────────────────────────────
with orders_table.batch_writer() as batch:
    for j in range(10):
        batch.put_item(Item={
            'order_id': f'batch-{j:03}',
            'customer_id': f'CUST-{j % 3:03}',
            'product': f'Product {j}',
            'amount': str(j * 10.0),
            'status': 'pending',
            'order_date': now.isoformat(),
            'expires_at': int((now + timedelta(days=7)).timestamp()),
        })
print("BatchWrite: 10 orders inserted")
```

```bash
python3 dynamo_lab.py
```

---

## Part 3 — DynamoDB Streams + Lambda Trigger

```bash
# Get Stream ARN
STREAM_ARN=$(aws dynamodb describe-table \
  --table-name "orders" \
  --query 'Table.LatestStreamArn' --output text)

echo "Stream ARN: $STREAM_ARN"

# Create Lambda that processes the stream
LAMBDA_ROLE=$(aws iam create-role \
  --role-name "lab-dynamo-stream-role" \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"}}]}' \
  --query 'Role.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-dynamo-stream-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole"

sleep 10

zip -j /tmp/stream_handler.zip - << 'PYTHON'
import json

def handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']
            print(f"NEW ORDER: id={new_item['order_id']['S']} customer={new_item.get('customer_id',{}).get('S')}")
        elif record['eventName'] == 'MODIFY':
            old_item = record['dynamodb'].get('OldImage', {})
            new_item = record['dynamodb']['NewImage']
            old_status = old_item.get('status', {}).get('S', '?')
            new_status = new_item.get('status', {}).get('S', '?')
            if old_status != new_status:
                print(f"STATUS CHANGED: {old_status} → {new_status}")
        elif record['eventName'] == 'REMOVE':
            print(f"ITEM REMOVED (TTL expired)")
    return {'batchItemFailures': []}
PYTHON

FUNC_ARN=$(aws lambda create-function \
  --function-name "lab-dynamo-stream-processor" \
  --runtime python3.12 \
  --role "$LAMBDA_ROLE" \
  --handler stream_handler.handler \
  --zip-file fileb:///tmp/stream_handler.zip \
  --query 'FunctionArn' --output text)

# Connect stream to Lambda
aws lambda create-event-source-mapping \
  --event-source-arn "$STREAM_ARN" \
  --function-name "lab-dynamo-stream-processor" \
  --starting-position TRIM_HORIZON \
  --batch-size 10

echo "Stream trigger created!"
sleep 15

# Check Lambda logs (batch write events)
aws logs filter-log-events \
  --log-group-name "/aws/lambda/lab-dynamo-stream-processor" \
  --filter-pattern "NEW ORDER" \
  --query 'events[*].message' \
  --output text | head -10
```

---

## Cleanup

```bash
# Delete Lambda and trigger
aws lambda delete-function --function-name "lab-dynamo-stream-processor"
aws iam detach-role-policy \
  --role-name "lab-dynamo-stream-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole"
aws iam delete-role --role-name "lab-dynamo-stream-role"

# Delete tables
aws dynamodb delete-table --table-name "orders"
aws dynamodb delete-table --table-name "cart"

rm -f dynamo_lab.py /tmp/stream_handler.zip
```

---

## What You Learned

- **Partition Key** distributes data; **Sort Key** enables range queries within a partition
- **GSI:** new view of the table with different keys; eventual consistency by default
- **Scan vs Query:** Scan reads EVERYTHING then filters (expensive); Query uses index (efficient)
- **TTL:** automatic and free expiration via Unix timestamp attribute — not immediate (up to 48h)
- **Streams:** immutable change log; integrates with Lambda for real-time reactions (event sourcing)
- **ConditionExpression:** idempotent atomic writes — prevents lost updates under concurrency
