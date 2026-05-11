# Module 28 — Practical Labs

## About This Module

This module consolidates the main AWS labs for practical SAA-C03 study. Each lab includes AWS CLI commands and equivalent Terraform code to reinforce hands-on learning.

> **Total estimated lab cost**: < $5 (always run cleanup after each lab)

---

## Lab 1: Serverless API with Lambda + DynamoDB + API Gateway

**Objective**: Create a complete serverless API with CRUD on DynamoDB.

**Architecture:**
```
API Gateway HTTP API → Lambda → DynamoDB
```

**CLI — Step by step:**
```bash
# 1. Create DynamoDB table
aws dynamodb create-table \
  --table-name Products \
  --attribute-definitions AttributeName=productId,AttributeType=S \
  --key-schema AttributeName=productId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# 2. Create IAM role for Lambda
aws iam create-role \
  --role-name lambda-products-role \
  --assume-role-policy-document file://lambda-trust-policy.json

aws iam attach-role-policy \
  --role-name lambda-products-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# 3. Deploy Lambda function
zip function.zip index.js
aws lambda create-function \
  --function-name products-api \
  --runtime nodejs20.x \
  --handler index.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-products-role

# 4. Create API Gateway HTTP API
aws apigatewayv2 create-api \
  --name products-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:ACCOUNT_ID:function:products-api

# Cleanup
aws lambda delete-function --function-name products-api
aws dynamodb delete-table --table-name Products
aws apigatewayv2 delete-api --api-id API_ID
```

**Equivalent Terraform:**
```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = "us-east-1" }

resource "aws_dynamodb_table" "products" {
  name         = "Products"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "productId"
  attribute { name = "productId"; type = "S" }
}

resource "aws_iam_role" "lambda" {
  name               = "lambda-products-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy_attachment" "dynamodb" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "index.js"
  output_path = "function.zip"
}

resource "aws_lambda_function" "api" {
  function_name    = "products-api"
  filename         = "function.zip"
  handler          = "index.handler"
  runtime          = "nodejs20.x"
  role             = aws_iam_role.lambda.arn
  source_code_hash = data.archive_file.lambda.output_base64sha256
}
```

---

## Lab 2: VPC with Public and Private Subnets

**Objective**: Create a complete VPC with public and private subnets, NAT Gateway, bastion host.

```bash
# 1. Create VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=lab-vpc}]' \
  --query Vpc.VpcId --output text)

# 2. Create subnets (two AZs)
PUB_SUB_1=$(aws ec2 create-subnet --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=pub-1a}]' \
  --query Subnet.SubnetId --output text)

PRIV_SUB_1=$(aws ec2 create-subnet --vpc-id $VPC_ID \
  --cidr-block 10.0.11.0/24 --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=priv-1a}]' \
  --query Subnet.SubnetId --output text)

# 3. Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text)
aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID

# 4. Public route table
PUB_RT=$(aws ec2 create-route-table --vpc-id $VPC_ID --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PUB_RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 associate-route-table --route-table-id $PUB_RT --subnet-id $PUB_SUB_1

# 5. NAT Gateway (for private subnet)
EIP=$(aws ec2 allocate-address --domain vpc --query AllocationId --output text)
NAT_ID=$(aws ec2 create-nat-gateway --subnet-id $PUB_SUB_1 \
  --allocation-id $EIP --query NatGateway.NatGatewayId --output text)
# Wait for NAT to be available
aws ec2 wait nat-gateway-available --filter Name=nat-gateway-id,Values=$NAT_ID

# 6. Private route table (via NAT)
PRIV_RT=$(aws ec2 create-route-table --vpc-id $VPC_ID --query RouteTable.RouteTableId --output text)
aws ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT_ID
aws ec2 associate-route-table --route-table-id $PRIV_RT --subnet-id $PRIV_SUB_1

echo "VPC created: $VPC_ID"
```

---

## Lab 3: S3 with Versioning, Lifecycle, and Replication

```bash
# 1. Create buckets
aws s3api create-bucket --bucket my-primary-bucket-$(date +%s) --region us-east-1
aws s3api create-bucket --bucket my-replica-bucket-$(date +%s) \
  --create-bucket-configuration LocationConstraint=us-west-2 --region us-west-2

# 2. Enable versioning on both buckets
aws s3api put-bucket-versioning \
  --bucket my-primary-bucket \
  --versioning-configuration Status=Enabled

# 3. Lifecycle policy (move to IA after 30d, Glacier after 90d, delete after 365d)
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-primary-bucket \
  --lifecycle-configuration file://lifecycle.json

# lifecycle.json:
# {
#   "Rules": [{
#     "ID": "transition-rule",
#     "Status": "Enabled",
#     "Filter": {},
#     "Transitions": [
#       {"Days": 30, "StorageClass": "STANDARD_IA"},
#       {"Days": 90, "StorageClass": "GLACIER"}
#     ],
#     "Expiration": {"Days": 365}
#   }]
# }

# 4. Cross-region replication (CRR)
aws s3api put-bucket-replication \
  --bucket my-primary-bucket \
  --replication-configuration file://replication.json
```

---

## Lab 4: CloudWatch Alarm + Auto Scaling

```bash
# 1. Create Launch Template
aws ec2 create-launch-template \
  --launch-template-name web-template \
  --launch-template-data '{
    "ImageId": "ami-0c02fb55956c7d316",
    "InstanceType": "t3.micro",
    "SecurityGroupIds": ["sg-xxx"]
  }'

# 2. Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-template,Version='$Latest' \
  --min-size 1 --max-size 5 --desired-capacity 2 \
  --vpc-zone-identifier "subnet-aaa,subnet-bbb"

# 3. Create scaling policy
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name web-asg \
  --policy-name cpu-scale-out \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 70.0
  }'

# Cleanup
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name web-asg --force-delete
```

---

## Lab 5: RDS Multi-AZ with Snapshot and Restore

```bash
# 1. Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name lab-db-subnet \
  --db-subnet-group-description "Lab DB subnets" \
  --subnet-ids subnet-aaa subnet-bbb

# 2. Create Multi-AZ RDS MySQL instance
aws rds create-db-instance \
  --db-instance-identifier lab-rds \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password "MyPassword123!" \
  --allocated-storage 20 \
  --multi-az \
  --db-subnet-group-name lab-db-subnet \
  --no-publicly-accessible

# 3. Wait for availability
aws rds wait db-instance-available --db-instance-identifier lab-rds

# 4. Create snapshot
aws rds create-db-snapshot \
  --db-instance-identifier lab-rds \
  --db-snapshot-identifier lab-rds-snap-$(date +%Y%m%d)

# 5. Restore from snapshot (to new endpoint)
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier lab-rds-restored \
  --db-snapshot-identifier lab-rds-snap-YYYYMMDD

# Cleanup
aws rds delete-db-instance --db-instance-identifier lab-rds --skip-final-snapshot
```

---

## Essential CLI Command Reference

```bash
# EC2
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 start-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx

# IAM
aws iam list-roles --query 'Roles[*].RoleName'
aws iam get-role --role-name ROLE_NAME
aws sts get-caller-identity  # shows current account/user/role

# S3
aws s3 ls s3://my-bucket --recursive
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./folder s3://my-bucket/
aws s3api get-bucket-policy --bucket my-bucket

# Lambda
aws lambda list-functions
aws lambda invoke --function-name my-function --payload '{"key":"value"}' output.json
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip

# DynamoDB
aws dynamodb scan --table-name Products --max-items 10
aws dynamodb put-item --table-name Products \
  --item '{"productId": {"S": "p001"}, "name": {"S": "Test Product"}}'
aws dynamodb get-item --table-name Products \
  --key '{"productId": {"S": "p001"}}'
```

---

## Lab Tips

1. **Always clean up resources** after the lab to avoid unnecessary costs
2. **Use tags** on all created resources (e.g., `Project=lab`, `Environment=test`)
3. **Terraform destroy** is more reliable than manually deleting resources one by one
4. Use `aws configure` to set up credentials or set environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
5. To check lab costs: AWS Cost Explorer → Last 7 days → filter by service
