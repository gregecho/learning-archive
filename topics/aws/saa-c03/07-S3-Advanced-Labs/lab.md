# Hands-on Lab — S3: Versioning, Lifecycle, Replication and Events (Module 08)

> **Region:** us-east-1 | **Estimated cost:** ~$0.01 (minimal storage, < 1h)  
> **Prerequisites:** AWS CLI configured, Python 3.8+

---

## Objective

Practice advanced S3: object versioning, lifecycle policies, CRR, presigned URLs, and event notifications with Lambda.

---

## Part 1 — Versioning and Lifecycle

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_MAIN="lab-s3-lab-${ACCOUNT_ID}"
BUCKET_REPLICA="lab-s3-replica-${ACCOUNT_ID}"

# Create buckets
aws s3api create-bucket --bucket "$BUCKET_MAIN"

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket "$BUCKET_MAIN" \
  --versioning-configuration Status=Enabled

# Enable default encryption
aws s3api put-bucket-encryption \
  --bucket "$BUCKET_MAIN" \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }'

# Create multiple versions of the same object
for i in 1 2 3; do
  echo "Version ${i} of the file — $(date)" > /tmp/config.txt
  aws s3 cp /tmp/config.txt "s3://${BUCKET_MAIN}/config.txt"
  sleep 1
done

# List versions
aws s3api list-object-versions \
  --bucket "$BUCKET_MAIN" \
  --prefix "config.txt" \
  --query 'Versions[*].[VersionId, LastModified, IsLatest]' \
  --output table

# Retrieve specific version
FIRST_VERSION=$(aws s3api list-object-versions \
  --bucket "$BUCKET_MAIN" \
  --prefix "config.txt" \
  --query 'Versions[-1].VersionId' --output text)

aws s3api get-object \
  --bucket "$BUCKET_MAIN" \
  --key "config.txt" \
  --version-id "$FIRST_VERSION" \
  /tmp/config_v1.txt

echo "Oldest version contents:"
cat /tmp/config_v1.txt

# Lifecycle Policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket "$BUCKET_MAIN" \
  --lifecycle-configuration '{
    "Rules": [
      {
        "ID": "move-to-ia-30-days",
        "Status": "Enabled",
        "Filter": {"Prefix": "logs/"},
        "Transitions": [
          {"Days": 30, "StorageClass": "STANDARD_IA"},
          {"Days": 90, "StorageClass": "GLACIER"}
        ],
        "Expiration": {"Days": 365}
      },
      {
        "ID": "clean-old-versions",
        "Status": "Enabled",
        "Filter": {"Prefix": ""},
        "NoncurrentVersionTransitions": [
          {"NoncurrentDays": 30, "StorageClass": "STANDARD_IA"}
        ],
        "NoncurrentVersionExpiration": {"NoncurrentDays": 90},
        "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}
      }
    ]
  }'

echo "Lifecycle configured!"
```

---

## Part 2 — Presigned URLs

```bash
# Create private file for presigned URL demo
echo "Confidential document with temporary access" > /tmp/private_document.txt
aws s3 cp /tmp/private_document.txt "s3://${BUCKET_MAIN}/private/document.txt"

# Verify the object is private
aws s3api get-object-acl \
  --bucket "$BUCKET_MAIN" \
  --key "private/document.txt" \
  --query 'Grants[*].[Permission, Grantee.Type]' \
  --output table

# Generate presigned URL (valid for 60 seconds)
PRESIGNED_URL=$(aws s3 presign \
  "s3://${BUCKET_MAIN}/private/document.txt" \
  --expires-in 60)

echo "Presigned URL (60s):"
echo "$PRESIGNED_URL" | head -c 100
echo "..."

# Use the URL to download
curl -s "$PRESIGNED_URL" -o /tmp/download_presigned.txt
echo "Download via presigned URL:"
cat /tmp/download_presigned.txt

# Presigned URL for UPLOAD (PUT)
PRESIGNED_PUT=$(aws s3 presign \
  "s3://${BUCKET_MAIN}/uploads/user_file.txt" \
  --expires-in 300)

echo "Presigned PUT URL generated (simulating client upload)"
# curl -X PUT "$PRESIGNED_PUT" -T /tmp/config.txt  # uncomment to test
```

---

## Part 3 — S3 Event Notification with Lambda

```bash
# IAM Role for Lambda
LAMBDA_ROLE_ARN=$(aws iam create-role \
  --role-name "lab-s3-event-lambda-role" \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"}}]}' \
  --query 'Role.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-s3-event-lambda-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"

sleep 10

# Lambda that processes new objects
zip -j /tmp/s3_event_handler.zip - << 'PYTHON'
import json

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key    = record['s3']['object']['key']
        size   = record['s3']['object']['size']
        event_name = record['eventName']
        print(f"[S3 EVENT] {event_name}: s3://{bucket}/{key} ({size} bytes)")
    return {'statusCode': 200}
PYTHON

FUNC_ARN=$(aws lambda create-function \
  --function-name "lab-s3-event-processor" \
  --runtime python3.12 \
  --role "$LAMBDA_ROLE_ARN" \
  --handler s3_event_handler.handler \
  --zip-file fileb:///tmp/s3_event_handler.zip \
  --query 'FunctionArn' --output text)

# Permission for S3 to invoke Lambda
aws lambda add-permission \
  --function-name "lab-s3-event-processor" \
  --principal s3.amazonaws.com \
  --action lambda:InvokeFunction \
  --statement-id "s3-invoke" \
  --source-arn "arn:aws:s3:::${BUCKET_MAIN}" \
  --source-account "$ACCOUNT_ID"

# Configure S3 notification
aws s3api put-bucket-notification-configuration \
  --bucket "$BUCKET_MAIN" \
  --notification-configuration "{
    \"LambdaFunctionConfigurations\": [{
      \"LambdaFunctionArn\": \"${FUNC_ARN}\",
      \"Events\": [\"s3:ObjectCreated:*\"],
      \"Filter\": {
        \"Key\": {
          \"FilterRules\": [{\"Name\": \"prefix\", \"Value\": \"uploads/\"}]
        }
      }
    }]
  }"

# Upload to trigger event
echo "Test file $(date)" > /tmp/novo_upload.txt
aws s3 cp /tmp/novo_upload.txt "s3://${BUCKET_MAIN}/uploads/new_file.txt"

sleep 15

# Check Lambda logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/lab-s3-event-processor" \
  --filter-pattern "S3 EVENT" \
  --query 'events[*].message' \
  --output text
```

---

## Cleanup

```bash
# Delete Lambda
aws lambda delete-function --function-name "lab-s3-event-processor"
aws iam detach-role-policy \
  --role-name "lab-s3-event-lambda-role" \
  --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
aws iam delete-role --role-name "lab-s3-event-lambda-role"

# Delete all S3 object versions
python3 << PYTHON
import boto3
s3 = boto3.client('s3', region_name='us-east-1')
bucket = "$BUCKET_MAIN"
paginator = s3.get_paginator('list_object_versions')
for page in paginator.paginate(Bucket=bucket):
    for obj_type in ['Versions', 'DeleteMarkers']:
        for item in page.get(obj_type, []):
            s3.delete_object(Bucket=bucket, Key=item['Key'], VersionId=item['VersionId'])
print("All objects and versions deleted")
PYTHON

aws s3api delete-bucket --bucket "$BUCKET_MAIN"

# Remove local files
rm -f /tmp/config.txt /tmp/config_v1.txt /tmp/private_document.txt \
      /tmp/download_presigned.txt /tmp/novo_upload.txt /tmp/s3_event_handler.zip
```

---

## What You Learned

- **Versioning:** once enabled, never "disabled" — only "suspended"; every version stored is billed
- **Delete marker:** deleting a versioned object creates a Delete Marker (the object does not actually vanish)
- **Lifecycle transitions:** STANDARD → STANDARD_IA (min 30 days) → GLACIER (min 90 days)
- **Presigned URL:** allows temporary access without credentials; expires at the defined time; audited via CloudTrail
- **S3 Events:** push pattern (S3 → Lambda/SNS/SQS); ideal for file processing pipelines
- **CRR:** cross-region replication requires versioning on both buckets and an IAM role with s3:ReplicateObject
