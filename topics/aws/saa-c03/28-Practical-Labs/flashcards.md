# Flashcards — Module 28: Practical Labs

> **Format:** Q = Question | A = Answer  
> **Total:** 25 flashcards

---

**Q:** How to create a Lambda Function with DynamoDB permission via CLI?  
**A:**
```bash
# 1. Create IAM Role
aws iam create-role --role-name LambdaDynamoRole \
  --assume-role-policy-document file://trust-lambda.json

# 2. Attach policy
aws iam attach-role-policy --role-name LambdaDynamoRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# 3. Deploy Lambda
aws lambda create-function --function-name MyFunc \
  --runtime python3.12 --role arn:aws:iam::ACCOUNT:role/LambdaDynamoRole \
  --handler lambda_function.lambda_handler --zip-file fileb://function.zip
```

---

**Q:** How to create a VPC with public and private subnet via Terraform?  
**A:**
```hcl
resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }
resource "aws_subnet" "public" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true; availability_zone = "us-east-1a"
}
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id; cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}
resource "aws_internet_gateway" "igw" { vpc_id = aws_vpc.main.id }
```

---

**Q:** How to check if an EC2 in private subnet has internet connectivity?  
**A:** The private instance needs a **NAT Gateway** in the public subnet with route in the private subnet: `0.0.0.0/0 → NAT GW`. To test: `curl -I https://aws.amazon.com` (inside the instance via SSM Session Manager). Without NAT GW: timeout. With NAT GW + correct route: HTTP 200.

---

**Q:** What is the AWS CLI command to upload a file to S3 with SSE-KMS encryption?  
**A:**
```bash
aws s3 cp file.txt s3://my-bucket/file.txt \
  --sse aws:kms \
  --sse-kms-key-id arn:aws:kms:us-east-1:123456:key/key-id
```
Verify:
```bash
aws s3api head-object --bucket my-bucket --key file.txt \
  --query 'ServerSideEncryption'
```

---

**Q:** How to test an API Gateway + Lambda locally before deploy?  
**A:**
```bash
# Install SAM CLI
pip install aws-sam-cli

# Invoke Lambda locally
sam local invoke "FunctionName" -e events/event.json

# Bring up local API (port 3000)
sam local start-api

# Test
curl -X POST http://localhost:3000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

**Q:** Which Terraform command previews changes before applying?  
**A:**
```bash
terraform plan -out=tfplan    # shows changes + saves plan
terraform show tfplan         # view the saved plan
terraform apply tfplan        # apply exactly the saved plan
```
The `-out=tfplan` ensures that `apply` applies exactly what was reviewed in `plan`, with no surprises from state changes between plan and apply.

---

**Q:** How to configure Auto Scaling Group to scale based on CPU via CLI?  
**A:**
```bash
# Create scaling policy
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name MyASG \
  --policy-name cpu-scale-out \
  --scaling-adjustment 1 \
  --adjustment-type ChangeInCapacity

# Create CloudWatch Alarm that triggers the policy
aws cloudwatch put-metric-alarm \
  --alarm-name High-CPU \
  --metric-name CPUUtilization --namespace AWS/EC2 \
  --threshold 70 --comparison-operator GreaterThanThreshold \
  --statistic Average --period 300 --evaluation-periods 2 \
  --alarm-actions arn:aws:autoscaling:...policy/cpu-scale-out
```

---

**Q:** How to enable versioning on S3 and list versions of an object?  
**A:**
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# List versions of an object
aws s3api list-object-versions \
  --bucket my-bucket --prefix file.txt \
  --query 'Versions[*].[VersionId,LastModified,IsLatest]'

# Restore specific version
aws s3api copy-object --bucket my-bucket \
  --copy-source "my-bucket/file.txt?versionId=abc123" \
  --key file.txt
```

---

**Q:** How to create a Multi-AZ RDS instance with Terraform?  
**A:**
```hcl
resource "aws_db_instance" "main" {
  identifier        = "prod-db"
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = "db.t3.medium"
  allocated_storage = 20
  username          = "admin"
  password          = var.db_password
  multi_az          = true
  skip_final_snapshot = false
  final_snapshot_identifier = "prod-db-final"
  backup_retention_period = 7
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
}
```

---

**Q:** How to check Lambda function logs in CloudWatch via CLI?  
**A:**
```bash
# List log streams (invocations)
aws logs describe-log-streams \
  --log-group-name /aws/lambda/MyFunction \
  --order-by LastEventTime --descending --max-items 5

# View last invocation logs
aws logs get-log-events \
  --log-group-name /aws/lambda/MyFunction \
  --log-stream-name "2024/01/01/[$LATEST]abc123" \
  --query 'events[*].message'
```

---

**Q:** How to create a DynamoDB table with GSI via Terraform?  
**A:**
```hcl
resource "aws_dynamodb_table" "orders" {
  name         = "Orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "orderId"
  range_key    = "createdAt"
  attribute { name = "orderId"   type = "S" }
  attribute { name = "createdAt" type = "S" }
  attribute { name = "userId"    type = "S" }

  global_secondary_index {
    name            = "UserIdIndex"
    hash_key        = "userId"
    range_key       = "createdAt"
    projection_type = "ALL"
  }
}
```

---

**Q:** How to configure CORS on API Gateway via Terraform?  
**A:**
```hcl
resource "aws_api_gateway_method" "options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}
resource "aws_api_gateway_integration" "options" {
  http_method = aws_api_gateway_method.options.http_method
  type        = "MOCK"
  request_templates = { "application/json" = "{\"statusCode\": 200}" }
}
# + method_response e integration_response with CORS headers
```

---

**Q:** How to create a CloudWatch Alarm to monitor Lambda errors and send to SNS?  
**A:**
```bash
# Create SNS topic
aws sns create-topic --name lambda-errors-alert

# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "LambdaErrors-MyFunction" \
  --metric-name Errors --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=MyFunction \
  --statistic Sum --period 60 \
  --threshold 5 --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:lambda-errors-alert
```

---

**Q:** How to perform Terraform resource cleanup to avoid costs?  
**A:**
```bash
# Destroy all resources from state
terraform destroy

# Check what will be destroyed beforehand
terraform plan -destroy

# Force deletion of S3 bucket with objects (force_destroy=true in .tf)
# or via CLI:
aws s3 rm s3://my-bucket --recursive
aws s3api delete-bucket --bucket my-bucket

# Check remaining resources in account
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Environment,Values=lab
```

---

**Q:** How to diagnose why a Lambda cannot access an RDS instance in VPC?  
**A:** Checklist: (1) Lambda has VPC config with private subnet? (2) Lambda Security Group has outbound on port 3306? (3) RDS Security Group has inbound on port 3306 **from Lambda SG** (not CIDR)? (4) Lambda subnets route to NAT GW (to call AWS APIs)? (5) RDS is in the same VPC as Lambda? (6) RDS endpoint is correct (not IP)?

---

**Q:** How to create an ECS Fargate Service with Terraform?  
**A:**
```hcl
resource "aws_ecs_service" "app" {
  name            = "my-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.private.id]
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8080
  }
}
```

---

**Q:** How to use AWS CLI to test an IAM Policy without applying it?  
**A:**
```bash
# Simulate if an action is allowed for the principal
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT:role/MyRole \
  --action-names "s3:GetObject" \
  --resource-arns "arn:aws:s3:::my-bucket/*"

# Result: allowed/denied + which policy blocked
# Also useful: iam simulate-custom-policy to test JSON policy directly
```

---

**Q:** How to deploy a Lambda application with SAM and create API Gateway automatically?  
**A:**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.12
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```
```bash
sam build && sam deploy --guided
```

---

**Q:** What is the CLI command to list running EC2 instances per region?  
**A:**
```bash
# Running instances in default region
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# All regions (bash script)
for region in $(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text); do
  echo "Region: $region"
  aws ec2 describe-instances --region $region --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].InstanceId' --output text
done
```

---

**Q:** How to configure S3 Lifecycle Policy for Glacier transition via CLI?  
**A:**
```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "move-to-glacier",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }]
  }'
```

---

**Q:** How to debug a 403 Forbidden error in S3?  
**A:** Checklist: (1) Bucket Policy blocking? `aws s3api get-bucket-policy --bucket bucket`. (2) Block Public Access enabled? `aws s3api get-public-access-block --bucket bucket`. (3) IAM Policy for role/user has `s3:GetObject`? `aws iam simulate-principal-policy`. (4) Object ACL? `aws s3api get-object-acl --bucket bucket --key key`. (5) KMS key: does role have `kms:Decrypt`?

---

**Q:** What is the command to manually scale an ECS Service?  
**A:**
```bash
# Increase desired count to 5
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --desired-count 5

# Check deploy
aws ecs describe-services \
  --cluster my-cluster \
  --services my-service \
  --query 'services[0].[runningCount,desiredCount,deployments]'
```

---

**Q:** How to configure CloudFront with S3 origin using OAC (Origin Access Control)?  
**A:**
```hcl
resource "aws_cloudfront_origin_access_control" "oac" {
  name = "my-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior = "always"
  signing_protocol = "sigv4"
}
# In CloudFront distribution: origin with origin_access_control_id = oac.id
# Bucket Policy: allow only cloudfront.amazonaws.com with condition
# "aws:SourceArn": "arn:aws:cloudfront::ACCOUNT:distribution/DISTID"
```

---

**Q:** How to estimate cost of resources provisioned by Terraform?  
**A:** Option 1: **Infracost** (open-source tool): `infracost breakdown --path .` — shows estimated monthly cost per Terraform resource. Option 2: **AWS Pricing Calculator** (manual). Option 3: **Terraform Cloud** has integrated cost estimation. Option 4: after `terraform apply`, check AWS Cost Explorer with project tags.

---

**Q:** How to create a Secret in Secrets Manager and retrieve it with Lambda?  
**A:**
```bash
# Create secret
aws secretsmanager create-secret \
  --name prod/db/credentials \
  --secret-string '{"username":"admin","password":"supersecret"}'
```
```python
# Lambda Python
import boto3, json
def lambda_handler(event, context):
    sm = boto3.client('secretsmanager')
    secret = sm.get_secret_value(SecretId='prod/db/credentials')
    creds = json.loads(secret['SecretString'])
    # use creds['username'] and creds['password']
```
Lambda Role needs `secretsmanager:GetSecretValue`.
