# Practical Lab — Practice Exams and Final Review: Study Environment Setup (Module 29)

> **Region:** us-east-1 | **Estimated cost:** ~$0.01 (DynamoDB on-demand, Lambda minimal)  
> **Prerequisites:** AWS CLI configured, Python 3.8+, pip

---

## Objective

Build a personalized review environment: flashcard deck in DynamoDB, interactive quiz script, and CloudWatch dashboard to track study progress.

---

## Part 1 — DynamoDB as Flashcard Database

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TABLE_FLASH="saa-flashcards"
TABLE_PROGRESS="saa-progress"

# Create flashcards table
aws dynamodb create-table \
  --table-name "$TABLE_FLASH" \
  --attribute-definitions \
    "AttributeName=module,AttributeType=S" \
    "AttributeName=card_id,AttributeType=S" \
  --key-schema \
    "AttributeName=module,KeyType=HASH" \
    "AttributeName=card_id,KeyType=RANGE" \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[{
    "IndexName": "difficulty-index",
    "KeySchema": [
      {"AttributeName": "module", "KeyType": "HASH"},
      {"AttributeName": "card_id", "KeyType": "RANGE"}
    ],
    "Projection": {"ProjectionType": "ALL"}
  }]'

# Create progress table
aws dynamodb create-table \
  --table-name "$TABLE_PROGRESS" \
  --attribute-definitions \
    "AttributeName=user,AttributeType=S" \
    "AttributeName=session_date,AttributeType=S" \
  --key-schema \
    "AttributeName=user,KeyType=HASH" \
    "AttributeName=session_date,KeyType=RANGE" \
  --billing-mode PAY_PER_REQUEST

aws dynamodb wait table-exists --table-name "$TABLE_FLASH"
aws dynamodb wait table-exists --table-name "$TABLE_PROGRESS"
echo "Tables created!"

# Populating final review flashcards
python3 << 'PYTHON'
import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('saa-flashcards')

flashcards = [
    # EC2 Module
    {"module": "ec2", "card_id": str(uuid.uuid4()),
     "question": "Which instance type is most suitable for in-memory databases?",
     "answer": "R (Memory Optimized) — e.g., r6g, r5. High RAM/vCPU ratio for Redis, SAP HANA, in-memory databases.",
     "difficulty": "medium"},
    {"module": "ec2", "card_id": str(uuid.uuid4()),
     "question": "What is a Spot Instance Fleet?",
     "answer": "Set of Spot Instances of multiple types/AZs configured to maintain target capacity. Uses automatic replacement.",
     "difficulty": "hard"},

    # S3 Module
    {"module": "s3", "card_id": str(uuid.uuid4()),
     "question": "Which S3 class has retrieval fee and minimum storage cost of 90 days?",
     "answer": "S3 Glacier Flexible Retrieval — min 90 days billing, retrieval in minutes to 12h.",
     "difficulty": "medium"},
    {"module": "s3", "card_id": str(uuid.uuid4()),
     "question": "How does S3 Transfer Acceleration work?",
     "answer": "Uses CloudFront edge locations to optimize upload via long-haul TCP. Endpoint: bucket.s3-accelerate.amazonaws.com",
     "difficulty": "easy"},

    # VPC Module
    {"module": "vpc", "card_id": str(uuid.uuid4()),
     "question": "Difference between Security Group and NACL?",
     "answer": "SG: stateful, instance level, ALLOW only. NACL: stateless, subnet level, ALLOW and DENY, numbered rules.",
     "difficulty": "easy"},
    {"module": "vpc", "card_id": str(uuid.uuid4()),
     "question": "What is VPC Peering and what is its main limitation?",
     "answer": "Direct connection between VPCs without transitivity. A→B and B→C does NOT allow A→C. Alternative: Transit Gateway.",
     "difficulty": "medium"},

    # IAM Module
    {"module": "iam", "card_id": str(uuid.uuid4()),
     "question": "What is an IAM Permission Boundary?",
     "answer": "Policy that defines the MAXIMUM permission an entity can have. Does not grant — only limits the ceiling.",
     "difficulty": "hard"},

    # RDS Module
    {"module": "rds", "card_id": str(uuid.uuid4()),
     "question": "Multi-AZ RDS vs Read Replica: which is for DR and which is for performance?",
     "answer": "Multi-AZ = DR/HA (automatic failover, synchronous, same region). Read Replica = scaled reading (asynchronous, can be cross-region).",
     "difficulty": "easy"},

    # Serverless Module
    {"module": "serverless", "card_id": str(uuid.uuid4()),
     "question": "What is Lambda's maximum timeout?",
     "answer": "15 minutes (900 seconds). For longer processes: SQS → Lambda, Step Functions, ECS/Fargate.",
     "difficulty": "easy"},

    # Security
    {"module": "security", "card_id": str(uuid.uuid4()),
     "question": "Which service protects against DDoS Layer 3/4 at no additional cost?",
     "answer": "AWS Shield Standard — automatically enabled for all customers. Shield Advanced: Layer 7 + 24/7 support.",
     "difficulty": "easy"},
    {"module": "security", "card_id": str(uuid.uuid4()),
     "question": "Difference: GuardDuty vs Macie vs Inspector vs WAF?",
     "answer": "GuardDuty=account/network/S3 threats. Macie=S3 sensitive data (PII). Inspector=EC2/Lambda/ECR vulnerabilities. WAF=HTTP Layer 7 protection.",
     "difficulty": "hard"},
]

with table.batch_writer() as batch:
    for card in flashcards:
        batch.put_item(Item=card)

print(f"{len(flashcards)} flashcards inserted!")
PYTHON
```

---

## Part 2 — Interactive Quiz Script

```python
# quiz.py — Save and run with: python3 quiz.py
import boto3
import random
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_flash = dynamodb.Table('saa-flashcards')
table_prog  = dynamodb.Table('saa-progress')

def fetch_cards(module=None, difficulty=None):
    if module:
        resp = table_flash.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('module').eq(module)
        )
    else:
        resp = table_flash.scan()

    cards = resp['Items']
    if difficulty:
        cards = [c for c in cards if c.get('difficulty') == difficulty]
    return cards

def run_quiz():
    print("\n=== SAA-C03 Quiz ===")
    print("Modules: ec2, s3, vpc, iam, rds, serverless, security (or ENTER for all)")
    module = input("Module: ").strip() or None

    cards = fetch_cards(module=module)
    if not cards:
        print("No cards found!")
        return

    random.shuffle(cards)
    cards = cards[:10]  # max 10 per session

    correct = 0
    total = len(cards)
    errors = []

    for i, card in enumerate(cards, 1):
        print(f"\n[{i}/{total}] Module: {card['module'].upper()}")
        print(f"Q: {card['question']}")
        input("Press ENTER to see the answer...")
        print(f"A: {card['answer']}")
        got_it = input("Did you get it right? (y/n): ").strip().lower() == 'y'

        if got_it:
            correct += 1
        else:
            errors.append(card)

    percentage = (correct / total) * 100
    print(f"\n=== Result ===")
    print(f"Correct: {correct}/{total} ({percentage:.0f}%)")

    if errors:
        print(f"\nCards to review:")
        for c in errors:
            print(f"  [{c['module']}] {c['question'][:60]}...")

    # Save progress
    table_prog.put_item(Item={
        'user': 'student',
        'session_date': datetime.utcnow().isoformat(),
        'module': module or 'all',
        'correct': correct,
        'total': total,
        'percentage': str(round(percentage, 1))
    })
    print("\nProgress saved in DynamoDB!")

if __name__ == '__main__':
    run_quiz()
```

```bash
# Run the quiz
python3 quiz.py
```

---

## Part 3 — CloudWatch Study Dashboard

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Publish custom progress metrics
aws cloudwatch put-metric-data \
  --namespace "SAA/Studies" \
  --metric-data '[
    {"MetricName": "FlashcardsReviewed", "Value": 10, "Unit": "Count",
     "Dimensions": [{"Name": "Module", "Value": "ec2"}]},
    {"MetricName": "AccuracyPercentage", "Value": 80, "Unit": "Percent",
     "Dimensions": [{"Name": "Module", "Value": "ec2"}]},
    {"MetricName": "DaysStudied", "Value": 1, "Unit": "Count",
     "Dimensions": [{"Name": "Week", "Value": "week-1"}]}
  ]'

# Create visual dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "SAA-C03-Progress" \
  --dashboard-body '{
    "widgets": [
      {
        "type": "metric",
        "x": 0, "y": 0, "width": 12, "height": 6,
        "properties": {
          "title": "Flashcards Reviewed by Module",
          "namespace": "SAA/Studies",
          "metrics": [
            ["SAA/Studies", "FlashcardsReviewed", "Module", "ec2"],
            ["SAA/Studies", "FlashcardsReviewed", "Module", "s3"],
            ["SAA/Studies", "FlashcardsReviewed", "Module", "vpc"]
          ],
          "period": 86400,
          "stat": "Sum",
          "view": "bar"
        }
      },
      {
        "type": "metric",
        "x": 12, "y": 0, "width": 12, "height": 6,
        "properties": {
          "title": "Accuracy Rate by Module (%)",
          "namespace": "SAA/Studies",
          "metrics": [
            ["SAA/Studies", "AccuracyPercentage", "Module", "ec2"],
            ["SAA/Studies", "AccuracyPercentage", "Module", "s3"],
            ["SAA/Studies", "AccuracyPercentage", "Module", "vpc"]
          ],
          "period": 86400,
          "stat": "Average",
          "view": "bar",
          "yAxis": {"left": {"min": 0, "max": 100}}
        }
      },
      {
        "type": "text",
        "x": 0, "y": 6, "width": 24, "height": 3,
        "properties": {
          "markdown": "## SAA-C03 Goals\\n- 80%+ on all practice exams\\n- Complete 6 weeks of study\\n- Review all flashcards 3x"
        }
      }
    ]
  }'

echo "Dashboard created: SAA-C03-Progress"
echo "Access: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=SAA-C03-Progress"
```

---

## Cleanup

```bash
# Delete DynamoDB tables
aws dynamodb delete-table --table-name "$TABLE_FLASH"
aws dynamodb delete-table --table-name "$TABLE_PROGRESS"

# Delete dashboard
aws cloudwatch delete-dashboards --dashboard-names "SAA-C03-Progress"

# Remove local files
rm -f quiz.py
```

---

## What You Learned

- DynamoDB as key-value backend for simple apps — setup in < 1 min with CLI
- Custom CloudWatch metrics (`put-metric-data`) to track anything
- CloudWatch Dashboards via CLI with JSON body — codable, versionable in Git
- Active recall study pattern: exposure → hiding → attempt → feedback
- In the exam: **70%+ on Tutorials Dojo practice exams = high probability of passing SAA-C03**
