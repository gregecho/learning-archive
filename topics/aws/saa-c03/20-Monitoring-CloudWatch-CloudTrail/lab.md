# Hands-On Lab — Monitoring: CloudWatch + CloudTrail + Config (Module 14)

> **Region:** us-east-1 | **Estimated cost:** < $0.50 (CloudWatch first 10 alarms free; CloudTrail first 90 days Event History free)
> **Prerequisites:** AWS CLI configured, Terraform >= 1.5

---

## Objective

Implement a complete observability stack: custom metrics, alarms, CloudTrail with critical action alerts, and a Config rule.

---

## Part 1 — CloudWatch: Custom Metrics and Alarms

```bash
# Publish custom metric (simulate app counting orders)
aws cloudwatch put-metric-data \
  --namespace "MyApp/Orders" \
  --metric-data '[
    {
      "MetricName": "OrdersCreated",
      "Dimensions": [{"Name": "Environment", "Value": "production"}],
      "Value": 42,
      "Unit": "Count"
    },
    {
      "MetricName": "ErrorRate",
      "Dimensions": [{"Name": "Environment", "Value": "production"}],
      "Value": 2.5,
      "Unit": "Percent"
    }
  ]'

# Verify the metric was registered
aws cloudwatch list-metrics \
  --namespace "MyApp/Orders" \
  --query 'Metrics[*].[MetricName, Dimensions[0].Value]' \
  --output table

# Create error rate alarm
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create SNS topic for alerts
SNS_ARN=$(aws sns create-topic \
  --name lab-monitoring-alerts \
  --query 'TopicArn' --output text)

# Subscribe email to topic (replace with your email)
aws sns subscribe \
  --topic-arn "$SNS_ARN" \
  --protocol email \
  --notification-endpoint "your-email@example.com"

echo "Confirm the email subscription before continuing."
echo "SNS Topic ARN: $SNS_ARN"

# Create alarm for error rate > 5%
aws cloudwatch put-metric-alarm \
  --alarm-name "lab-high-error-rate" \
  --alarm-description "Application error rate above 5%" \
  --metric-name "ErrorRate" \
  --namespace "MyApp/Orders" \
  --dimensions Name=Environment,Value=production \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 5.0 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions "$SNS_ARN" \
  --ok-actions "$SNS_ARN" \
  --treat-missing-data notBreaching

# Check alarm state
aws cloudwatch describe-alarms \
  --alarm-names "lab-high-error-rate" \
  --query 'MetricAlarms[*].[AlarmName, StateValue, Threshold]' \
  --output table

# Simulate ALARM (publish value above threshold)
aws cloudwatch put-metric-data \
  --namespace "MyApp/Orders" \
  --metric-data '[
    {
      "MetricName": "ErrorRate",
      "Dimensions": [{"Name": "Environment", "Value": "production"}],
      "Value": 15.0,
      "Unit": "Percent"
    }
  ]'

echo "Wait ~5 minutes and check the alarm state..."
```

---

## Part 2 — CloudWatch Logs: Filters and Queries

```bash
# Create a test Log Group
aws logs create-log-group --log-group-name "/lab/application"
aws logs create-log-stream \
  --log-group-name "/lab/application" \
  --log-stream-name "test-stream"

# Inject simulated logs
TIMESTAMP=$(date +%s%3N)

aws logs put-log-events \
  --log-group-name "/lab/application" \
  --log-stream-name "test-stream" \
  --log-events "[
    {\"timestamp\": ${TIMESTAMP}, \"message\": \"INFO: Order 1001 created successfully\"},
    {\"timestamp\": $((TIMESTAMP + 1000)), \"message\": \"ERROR: Failed to process order 1002 - timeout\"},
    {\"timestamp\": $((TIMESTAMP + 2000)), \"message\": \"INFO: Order 1003 created successfully\"},
    {\"timestamp\": $((TIMESTAMP + 3000)), \"message\": \"ERROR: Connection refused to database\"},
    {\"timestamp\": $((TIMESTAMP + 4000)), \"message\": \"WARN: Abnormal response time: 2500ms\"}
  ]"

# CloudWatch Logs Insights Query
aws logs start-query \
  --log-group-name "/lab/application" \
  --start-time $(($(date +%s) - 3600)) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message
    | filter @message like /ERROR/
    | sort @timestamp desc
    | limit 20'

# Get result (use the queryId returned above)
# aws logs get-query-results --query-id "QUERY_ID_HERE"

# Create Metric Filter (count ERRORs per minute)
aws logs put-metric-filter \
  --log-group-name "/lab/application" \
  --filter-name "CountErrors" \
  --filter-pattern "ERROR" \
  --metric-transformations \
    metricName=ErrorCount,metricNamespace=MyApp/Logs,metricValue=1,defaultValue=0
```

---

## Part 3 — CloudTrail: Auditing with Alerts

```bash
# Create bucket for CloudTrail
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
CT_BUCKET="lab-cloudtrail-${ACCOUNT_ID}"

aws s3api create-bucket --bucket "$CT_BUCKET" --region us-east-1

# Create bucket policy (CloudTrail needs write permission)
cat > cloudtrail_bucket_policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::${CT_BUCKET}"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::${CT_BUCKET}/AWSLogs/${ACCOUNT_ID}/*",
      "Condition": {
        "StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}
      }
    }
  ]
}
EOF

aws s3api put-bucket-policy \
  --bucket "$CT_BUCKET" \
  --policy file://cloudtrail_bucket_policy.json

# Create trail
aws cloudtrail create-trail \
  --name "lab-trail" \
  --s3-bucket-name "$CT_BUCKET" \
  --include-global-service-events \
  --is-multi-region-trail \
  --enable-log-file-validation

# Start logging
aws cloudtrail start-logging --name "lab-trail"

# Check status
aws cloudtrail get-trail-status --name "lab-trail" \
  --query '[IsLogging, LatestDeliveryTime]'

# Create Metric Filter in CloudWatch to detect DeleteBucket
aws logs create-log-group --log-group-name "CloudTrailLogs"

aws cloudtrail update-trail \
  --name "lab-trail" \
  --cloud-watch-logs-log-group-arn "arn:aws:logs:us-east-1:${ACCOUNT_ID}:log-group:CloudTrailLogs:*" \
  --cloud-watch-logs-role-arn "arn:aws:iam::${ACCOUNT_ID}:role/CloudTrail_CloudWatchLogs_Role"

# Create filter for bucket deletion actions
aws logs put-metric-filter \
  --log-group-name "CloudTrailLogs" \
  --filter-name "DeleteBucketFilter" \
  --filter-pattern '{ ($.eventName = DeleteBucket) }' \
  --metric-transformations \
    metricName=DeleteBucketCount,metricNamespace=CloudTrailMetrics,metricValue=1

# Alarm for bucket deletion
aws cloudwatch put-metric-alarm \
  --alarm-name "lab-s3-bucket-deleted" \
  --metric-name "DeleteBucketCount" \
  --namespace "CloudTrailMetrics" \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions "$SNS_ARN" \
  --treat-missing-data notBreaching
```

---

## Part 4 — AWS Config: Compliance Rule

```bash
# View already available Config rules
aws configservice describe-config-rules \
  --query 'ConfigRules[*].ConfigRuleName' \
  --output table

# Create rule: EC2 instances without public IP
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "lab-ec2-no-public-ip",
    "Description": "Checks if EC2 instances have an associated public IP",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "EC2_INSTANCE_NO_PUBLIC_IP"
    },
    "Scope": {
      "ComplianceResourceTypes": ["AWS::EC2::Instance"]
    }
  }'

# Check compliance status (may take a few minutes)
aws configservice describe-compliance-by-config-rule \
  --config-rule-names "lab-ec2-no-public-ip" \
  --query 'ComplianceByConfigRules[*].[ConfigRuleName,Compliance.ComplianceType]' \
  --output table

# View non-compliant resources
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name "lab-ec2-no-public-ip" \
  --compliance-types "NON_COMPLIANT" \
  --query 'EvaluationResults[*].EvaluationResultIdentifier.EvaluationResultQualifier.[ResourceType,ResourceId]' \
  --output table
```

---

## Cleanup

```bash
# Stop CloudTrail
aws cloudtrail stop-logging --name "lab-trail"
aws cloudtrail delete-trail --name "lab-trail"

# Remove CloudTrail bucket
aws s3 rm "s3://${CT_BUCKET}" --recursive
aws s3api delete-bucket --bucket "$CT_BUCKET"

# Remove alarms
aws cloudwatch delete-alarms \
  --alarm-names "lab-high-error-rate" "lab-s3-bucket-deleted"

# Remove SNS topic
aws sns delete-topic --topic-arn "$SNS_ARN"

# Remove log groups
aws logs delete-log-group --log-group-name "/lab/application"
aws logs delete-log-group --log-group-name "CloudTrailLogs"

# Remove Config rule
aws configservice delete-config-rule --config-rule-name "lab-ec2-no-public-ip"

# Remove temporary file
rm -f cloudtrail_bucket_policy.json
```

---

## What You Learned

- Custom metrics in CloudWatch allow monitoring business KPIs (not just infra)
- Alarms can be composite (Composite Alarms) to avoid false positives
- CloudWatch Logs Insights offers SQL-like queries on logs without ETL
- CloudTrail records ALL API calls — fundamental for auditing
- Metric Filters transform log events into metrics (bridge between logs and alarms)
- Config evaluates compliance continuously — not just when configured

---
