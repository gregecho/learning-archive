# Practical Lab — Diagnosis and Debugging: Broken Environments (Module 28)

> **Region:** us-east-1 | **Estimated cost:** ~$0.02  
> **Prerequisites:** AWS CLI configured, Docker (optional), Python 3.8+

---

## Objective

Practice diagnosing common problems in AWS environments: Lambda timeout in VPC, S3 with 403 error, DynamoDB throttling, and ECS task that stops immediately.

---

## Part 1 — Lambda Timeout in VPC (Classic Problem)

```bash
# Create VPC without NAT Gateway (common cause of Lambda timeout → internet)
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 10.20.0.0/16 \
  --query 'Vpc.VpcId' --output text)
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames

SUBNET_PRIV=$(aws ec2 create-subnet \
  --vpc-id "$VPC_ID" \
  --cidr-block 10.20.1.0/24 \
  --availability-zone us-east-1a \
  --query 'Subnet.SubnetId' --output text)

SG_ID=$(aws ec2 create-security-group \
  --group-name "lab-debug-sg" \
  --description "Lab debugging" \
  --vpc-id "$VPC_ID" \
  --query 'GroupId' --output text)

# IAM Role for Lambda
LAMBDA_ROLE=$(aws iam create-role \
  --role-name "lab-debug-lambda-role" \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"}}]
  }' \
  --query 'Role.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-debug-lambda-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"

sleep 10  # propagate IAM

# Create Lambda INSIDE VPC without NAT — will timeout when trying to call external APIs
zip -j /tmp/lambda_debug.zip - << 'PYTHON'
import urllib.request
import json

def handler(event, context):
    print("Trying to access external API...")
    try:
        # This will timeout in Lambda in VPC without NAT Gateway
        req = urllib.request.urlopen("https://httpbin.org/get", timeout=5)
        data = json.loads(req.read())
        print(f"Success: {data}")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        raise e
    return {"status": "ok"}
PYTHON

aws lambda create-function \
  --function-name "lab-debug-vpc-timeout" \
  --runtime python3.12 \
  --role "$LAMBDA_ROLE" \
  --handler lambda_function.handler \
  --zip-file fileb:///tmp/lambda_debug.zip \
  --timeout 15 \
  --vpc-config "SubnetIds=${SUBNET_PRIV},SecurityGroupIds=${SG_ID}"

# Invoke to reproduce the problem
echo "Invoking Lambda (will timeout)..."
aws lambda invoke \
  --function-name "lab-debug-vpc-timeout" \
  --payload '{}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/debug_output.json
cat /tmp/debug_output.json

# DIAGNOSIS: Check logs to confirm the problem
sleep 5
aws logs filter-log-events \
  --log-group-name "/aws/lambda/lab-debug-vpc-timeout" \
  --filter-pattern "ERROR" \
  --query 'events[*].message' \
  --output text

echo ""
echo "=== SOLUTION ==="
echo "Lambda in private VPC without NAT Gateway cannot access the internet."
echo "Solutions:"
echo "  1. Add NAT Gateway in public subnet + route table"
echo "  2. Use VPC Endpoints for AWS services (S3, DynamoDB, SQS)"
echo "  3. Remove Lambda from VPC if it doesn't need private resources"
```

---

## Part 2 — S3 403 Forbidden: Diagnosis

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_403="lab-debug-403-${ACCOUNT_ID}"

# Create bucket with Block Public Access enabled
aws s3api create-bucket --bucket "$BUCKET_403"
aws s3api put-public-access-block \
  --bucket "$BUCKET_403" \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Upload test object
echo "Secret diagnostic content" > /tmp/test_403.txt
aws s3 cp /tmp/test_403.txt "s3://${BUCKET_403}/test_403.txt"

# RESTRICTIVE Bucket Policy — simulates access denied
aws s3api put-bucket-policy \
  --bucket "$BUCKET_403" \
  --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
      \"Sid\": \"DenyEveryone\",
      \"Effect\": \"Deny\",
      \"Principal\": \"*\",
      \"Action\": \"s3:GetObject\",
      \"Resource\": \"arn:aws:s3:::${BUCKET_403}/*\",
      \"Condition\": {
        \"StringNotEquals\": {
          \"aws:PrincipalAccount\": \"999999999999\"
        }
      }
    }]
  }"

# Try to access — will give 403
echo "Trying to access object (expected: 403)..."
aws s3 cp "s3://${BUCKET_403}/test_403.txt" /tmp/download_403.txt 2>&1 || true

echo ""
echo "=== 403 S3 DIAGNOSIS ==="
echo "Checklist:"

# 1. Block Public Access
echo "1. Block Public Access:"
aws s3api get-public-access-block --bucket "$BUCKET_403" 2>/dev/null

# 2. Bucket Policy
echo "2. Bucket Policy:"
aws s3api get-bucket-policy --bucket "$BUCKET_403" 2>/dev/null | python3 -m json.tool 2>/dev/null

# 3. Object ACL
echo "3. Object ACL:"
aws s3api get-object-acl --bucket "$BUCKET_403" --key "test_403.txt" 2>/dev/null

# 4. Encryption (needs kms:Decrypt permission?)
echo "4. Object encryption:"
aws s3api head-object --bucket "$BUCKET_403" --key "test_403.txt" \
  --query '[ServerSideEncryption, SSEKMSKeyId]' 2>/dev/null

# FIX: adjust policy to allow current account
aws s3api put-bucket-policy \
  --bucket "$BUCKET_403" \
  --policy "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
      \"Sid\": \"AllowCurrentAccount\",
      \"Effect\": \"Allow\",
      \"Principal\": {\"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\"},
      \"Action\": \"s3:GetObject\",
      \"Resource\": \"arn:aws:s3:::${BUCKET_403}/*\"
    }]
  }"

echo "Policy fixed. Trying access again..."
aws s3 cp "s3://${BUCKET_403}/test_403.txt" /tmp/download_403_ok.txt && cat /tmp/download_403_ok.txt
```

---

## Part 3 — DynamoDB Throttling

```bash
# Create table with minimum capacity
TABLE="lab-debug-throttle"
aws dynamodb create-table \
  --table-name "$TABLE" \
  --attribute-definitions "AttributeName=pk,AttributeType=S" \
  --key-schema "AttributeName=pk,KeyType=HASH" \
  --billing-mode PROVISIONED \
  --provisioned-throughput "ReadCapacityUnits=1,WriteCapacityUnits=1"

aws dynamodb wait table-exists --table-name "$TABLE"

# Python load script (causes throttle)
cat > /tmp/dynamo_load.py << 'PYTHON'
import boto3
from botocore.exceptions import ClientError
import time
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
TABLE = 'lab-debug-throttle'

throttle_errors = 0
success = 0

print("Sending 50 fast writes (WCU=1, will throttle)...")
for i in range(50):
    try:
        dynamodb.put_item(
            TableName=TABLE,
            Item={'pk': {'S': f'item-{i}'}, 'value': {'N': str(i)}}
        )
        success += 1
    except ClientError as e:
        if e.response['Error']['Code'] in ['ProvisionedThroughputExceededException', 'RequestLimitExceeded']:
            throttle_errors += 1
        else:
            raise

print(f"Results: {success} successes, {throttle_errors} throttles")

# Check throttle metrics
print("\nTo see throttle in CloudWatch:")
print("aws cloudwatch get-metric-statistics \\")
print("  --namespace AWS/DynamoDB \\")
print("  --metric-name WriteThrottleEvents \\")
print("  --dimensions Name=TableName,Value=lab-debug-throttle \\")
print("  --start-time $(date -d '-5 minutes' --utc +%FT%TZ) \\")
print("  --end-time $(date --utc +%FT%TZ) \\")
print("  --period 60 --statistics Sum")
PYTHON

python3 /tmp/dynamo_load.py

echo ""
echo "=== DYNAMODB THROTTLE SOLUTIONS ==="
echo "1. Increase provisioned WCU/RCU"
echo "2. Enable Auto Scaling (recommended)"
echo "3. Switch to PAY_PER_REQUEST (on-demand)"
echo "4. Implement exponential backoff in client"
echo "5. Use DAX for repeated reads"

# Demonstrate: switch to on-demand
aws dynamodb update-table \
  --table-name "$TABLE" \
  --billing-mode PAY_PER_REQUEST
echo "Table migrated to PAY_PER_REQUEST."
```

---

## Part 4 — ECS Task Stopped: Diagnosis

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name "lab-debug-cluster"

# IAM Role for ECS Task Execution
EXEC_ROLE=$(aws iam create-role \
  --role-name "lab-ecs-exec-role" \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"ecs-tasks.amazonaws.com"}}]
  }' \
  --query 'Role.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-ecs-exec-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"

# Register task with nonexistent image (will fail with EssentialTaskExited)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecs register-task-definition \
  --family "lab-debug-task" \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --cpu "256" \
  --memory "512" \
  --execution-role-arn "$EXEC_ROLE" \
  --container-definitions "[{
    \"name\": \"app\",
    \"image\": \"${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/does-not-exist:latest\",
    \"essential\": true,
    \"logConfiguration\": {
      \"logDriver\": \"awslogs\",
      \"options\": {
        \"awslogs-group\": \"/ecs/lab-debug\",
        \"awslogs-region\": \"us-east-1\",
        \"awslogs-stream-prefix\": \"ecs\"
      }
    }
  }]"

echo ""
echo "=== ECS TASK STOPPED DIAGNOSIS ==="
echo ""
echo "Common stoppedReason causes:"
echo ""
echo "  CannotPullContainerError:"
echo "    - Image does not exist in ECR"
echo "    - No access to ECR (IAM or VPC Endpoint)"
echo "    - Task in private subnet without NAT"
echo ""
echo "  EssentialTaskExited:"
echo "    - Container exited with non-zero code"
echo "    - Invalid entrypoint command"
echo "    - Out of Memory (increase memory limit)"
echo ""
echo "  ResourceInitializationError:"
echo "    - Secrets Manager/Parameter Store inaccessible"
echo "    - VPC Endpoint missing for secrets"
echo ""
echo "Diagnosis commands:"
echo "aws ecs describe-tasks --cluster <cluster> --tasks <task-arn>"
echo "  → look at: stoppedReason, containers[0].reason, exitCode"
echo ""
echo "aws logs get-log-events --log-group-name /ecs/<task> --log-stream-name <stream>"
echo "  → container logs before dying"
echo ""
echo "aws ecs describe-task-definition --task-definition <name>"
echo "  → check image, environment, secrets"
```

---

## Cleanup

```bash
# Delete DynamoDB resources
aws dynamodb delete-table --table-name "$TABLE"

# Delete ECS resources
aws ecs delete-cluster --cluster "lab-debug-cluster"
aws iam detach-role-policy \
  --role-name "lab-ecs-exec-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
aws iam delete-role --role-name "lab-ecs-exec-role"

# Delete Lambda and VPC
aws lambda delete-function --function-name "lab-debug-vpc-timeout"
aws iam detach-role-policy \
  --role-name "lab-debug-lambda-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
aws iam delete-role --role-name "lab-debug-lambda-role"

# Delete Security Group, Subnet, and VPC
aws ec2 delete-security-group --group-id "$SG_ID"
aws ec2 delete-subnet --subnet-id "$SUBNET_PRIV"
aws ec2 delete-vpc --vpc-id "$VPC_ID"

# Delete S3 resources
aws s3 rm "s3://${BUCKET_403}" --recursive
aws s3api delete-bucket --bucket "$BUCKET_403"

# Temporary files
rm -f /tmp/lambda_debug.zip /tmp/test_403.txt /tmp/download_403.txt \
      /tmp/download_403_ok.txt /tmp/dynamo_load.py /tmp/debug_output.json
```

---

## What You Learned

- **Lambda + VPC timeout:** private subnet without NAT = no internet; use VPC Endpoints for AWS APIs
- **S3 403 checklist:** Block Public Access → Bucket Policy → Object ACL → KMS permissions → IAM Policy
- **DynamoDB throttle:** WCU/RCU exceeded → CloudWatch logs `WriteThrottleEvents`; solution: on-demand or Auto Scaling
- **ECS stoppedReason:** primary source of diagnosis; always check `exitCode` and container CloudWatch Logs
- **Debugging mindset:** reproduce → confirm in logs → identify root cause → apply smallest change → validate
