# Practical Lab — Introduction SAA-C03

## 🎯 Objective

Prepare a safe and economical study environment for the upcoming modules, validating account access, default region, AWS account identification, and creation of a minimal governance trail with a budget and support bucket. The lab helps students start their studies with cost discipline and operational visibility.

## 📋 Prerequisites

- AWS CLI configured with a valid profile
- Terraform >= 1.5
- Required IAM permissions: sts:GetCallerIdentity, s3:CreateBucket, s3:PutBucketTagging, budgets:CreateBudget, sns:CreateTopic, sns:Subscribe, iam:PassRole when applicable
- Default region: us-east-1

## 🏗️ Lab Architecture

```text
User
  |
  +-> AWS CLI profile
          |
          +-> STS GetCallerIdentity
          +-> S3 Study Bucket
          +-> AWS Monthly Budget -> SNS Email
```

## 🔧 Step by Step

### Part 1 — Via AWS CLI

```bash
# Confirm the active identity and avoid running labs on the wrong account
aws sts get-caller-identity --profile default --region us-east-1

# Confirm the effective region used by the profile
aws configure get region --profile default

# Create a unique bucket for study artifacts
aws s3api create-bucket \
  --bucket saa-c03-study-artifacts-123456789012 \
  --region us-east-1

# Tag the bucket to facilitate cleanup and cost analysis
aws s3api put-bucket-tagging \
  --bucket saa-c03-study-artifacts-123456789012 \
  --tagging 'TagSet=[{Key=Project,Value=SAA-C03},{Key=Owner,Value=Study},{Key=Environment,Value=Lab}]'

# Create an SNS topic to receive budget alerts
aws sns create-topic \
  --name saa-c03-budget-alerts \
  --region us-east-1

# Replace with the ARN returned by the previous command
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:saa-c03-budget-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com \
  --region us-east-1
```

### Part 2 — Via Terraform

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

variable "alert_email" {
  type        = string
  description = "Email that will receive budget alerts"
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "study_artifacts" {
  bucket = "saa-c03-study-artifacts-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = "SAA-C03"
    Environment = "Lab"
    Owner       = "Study"
  }
}

resource "aws_s3_bucket_versioning" "study_artifacts" {
  bucket = aws_s3_bucket.study_artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_sns_topic" "budget_alerts" {
  name = "saa-c03-budget-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.budget_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_budgets_budget" "monthly" {
  name         = "saa-c03-monthly-budget"
  budget_type  = "COST"
  limit_amount = "10"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["Project$SAA-C03"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_sns_topic_arns  = [aws_sns_topic.budget_alerts.arn]
  }
}
```

## ✅ Validation

```bash
# Validate bucket
aws s3api get-bucket-tagging --bucket saa-c03-study-artifacts-123456789012 --region us-east-1

# Validate SNS subscription
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:us-east-1:123456789012:saa-c03-budget-alerts \
  --region us-east-1

# Validate account identity
aws sts get-caller-identity --region us-east-1
```

## 🧹 Resource Cleanup

```bash
# Remove content and bucket
aws s3 rm s3://saa-c03-study-artifacts-123456789012 --recursive --region us-east-1
aws s3api delete-bucket --bucket saa-c03-study-artifacts-123456789012 --region us-east-1

# Remove SNS topic
aws sns delete-topic \
  --topic-arn arn:aws:sns:us-east-1:123456789012:saa-c03-budget-alerts \
  --region us-east-1

# If you used Terraform
terraform destroy -var="alert_email=your-email@example.com"
```

## 💰 Estimated Cost

If the bucket is practically empty and the SNS topic has low volume, the cost for 1 hour tends to be very close to zero. The most sensitive component is usually AWS Budgets, depending on the account and type of use. In practical terms, this is a very low-cost lab, but it should still be cleaned up at the end.

