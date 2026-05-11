# Cheatsheet — Practical Labs (Module 28)

## AWS CLI Commands — Quick Reference

### Lambda
```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler app.lambda_handler \
  --zip-file fileb://function.zip

# Invoke (synchronous)
aws lambda invoke --function-name my-function output.json

# Invoke (asynchronous)
aws lambda invoke --function-name my-function \
  --invocation-type Event output.json

# View recent logs
aws logs tail /aws/lambda/my-function --follow
```

### S3
```bash
# Create bucket
aws s3api create-bucket --bucket my-bucket --region us-east-1

# Upload
aws s3 cp file.txt s3://my-bucket/

# Sync directory
aws s3 sync ./local/ s3://my-bucket/prefix/

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Block public access
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### EC2 / Auto Scaling
```bash
# List running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]" \
  --output table

# Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --min-size 1 --max-size 5 --desired-capacity 2 \
  --launch-template LaunchTemplateId=lt-xxx,Version='$Latest' \
  --vpc-zone-identifier "subnet-aaa,subnet-bbb"
```

### CloudWatch
```bash
# Create CPU > 80% alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "High-CPU" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=AutoScalingGroupName,Value=my-asg \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:alerts

# Publish custom metric
aws cloudwatch put-metric-data \
  --namespace "MyApp/Performance" \
  --metric-name "OrdersPerSecond" \
  --value 42 --unit Count
```

### DynamoDB
```bash
# Create table
aws dynamodb create-table \
  --table-name Orders \
  --attribute-definitions AttributeName=orderId,AttributeType=S \
  --key-schema AttributeName=orderId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Insert item
aws dynamodb put-item \
  --table-name Orders \
  --item '{"orderId": {"S": "001"}, "status": {"S": "pending"}}'
```

---

## Terraform — Common Resources

### Project Structure
```
project/
  main.tf          # main resources
  variables.tf     # variable declarations
  outputs.tf       # outputs
  terraform.tfvars # variable values
  versions.tf      # required_providers
```

### Version Block (standard)
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

### Most Common Resources on the Exam

| Terraform Resource | AWS Service |
|------------------|-------------|
| `aws_vpc` + `aws_subnet` | VPC / Subnets |
| `aws_security_group` | Security Groups |
| `aws_instance` | EC2 |
| `aws_lambda_function` | Lambda |
| `aws_s3_bucket` + `aws_s3_bucket_versioning` | S3 |
| `aws_dynamodb_table` | DynamoDB |
| `aws_db_instance` | RDS |
| `aws_elasticache_cluster` | ElastiCache |
| `aws_ecs_cluster` + `aws_ecs_service` | ECS |
| `aws_iam_role` + `aws_iam_role_policy_attachment` | IAM |
| `aws_cloudwatch_metric_alarm` | CloudWatch |

---

## Terraform — Essential Commands

| Command | What it does |
|---------|-----------|
| `terraform init` | Initializes providers, downloads plugins |
| `terraform validate` | Validates HCL syntax |
| `terraform plan` | Preview changes without applying |
| `terraform plan -out=tfplan` | Save plan for later apply |
| `terraform apply` | Apply changes (asks for confirmation) |
| `terraform apply -auto-approve` | Apply without confirmation |
| `terraform apply tfplan` | Apply saved plan |
| `terraform destroy` | Destroy all infrastructure |
| `terraform state list` | List resources in state |
| `terraform state show aws_instance.web` | Details of specific resource |
| `terraform output` | Display defined outputs |
| `terraform fmt` | Format HCL files |
| `terraform graph` | Generate dependency graph |

---

## SAM — Essential Commands

```bash
# Initialize SAM project
sam init

# Build locally
sam build

# Test locally
sam local invoke FunctionName
sam local start-api  # API GW locally on port 3000

# Deploy (guided)
sam deploy --guided

# Deploy with saved parameters
sam deploy

# View logs
sam logs -n FunctionName --stack-name my-stack --tail

# Delete stack
sam delete --stack-name my-stack
```

---

## Debug — Checklist by Problem

### Lambda cannot access RDS
```
1. Lambda and RDS in the same VPC? (Lambda needs VpcConfig)
2. Lambda Security Group allows outbound to port 5432/3306?
3. RDS Security Group allows inbound from Lambda SG?
4. Lambda has private subnets (not public)?
5. Private subnets have NAT Gateway for internet (if needed)?
6. Lambda IAM Role has basic permission (AWSLambdaVPCAccessExecutionRole)?
7. Lambda timeout is sufficient (DB connection may take time)?
```

### S3 returning 403 Forbidden
```
1. Bucket Policy blocking? (check aws s3api get-bucket-policy)
2. Block Public Access active and public ACL trying to be used?
3. IAM Policy for user/role has s3:GetObject?
4. Object exists? (aws s3 ls s3://bucket/key)
5. Bucket in a different region than client expects?
6. KMS key: user has decrypt permission on the key?
7. VPC Endpoint policy blocking? (if access via VPC Gateway Endpoint)
```

### ECS Task won't start (STOPPED)
```
1. Check stoppedReason: aws ecs describe-tasks --cluster X --tasks Y
2. Common causes:
   - CannotPullContainerError: private ECR without IAM or VPC endpoint
   - OutOfMemory: insufficient memory defined in task definition
   - ResourceInitializationError: exec role missing
3. CloudWatch Logs: /ecs/<task-family> — check application errors
4. Task Role has necessary permissions (e.g., s3:GetObject)?
5. ECS Security Group allows outbound to RDS/external services?
```

---

## Cleanup Order in Terraform (`terraform destroy`)

Dependencies that can cause errors if deleted in wrong order:
```
1. ECS Services (before Cluster)
2. ALB / Target Groups (before subnets/SGs)
3. RDS / ElastiCache (before subnet group and SGs)
4. Lambda (may have ENIs in VPC)
5. NAT Gateway (before EIP can be released)
6. Subnets (before VPC)
7. VPC (last — everything inside it must be removed first)
```

> Generally `terraform destroy` resolves in order by dependencies. Problems occur with resources created outside Terraform.

---

## IAM — Simulate Policy (permission debugging)

```bash
# Simulate if action is allowed
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT:role/my-role \
  --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::my-bucket/*
  
# Expected result: "EvalDecision": "allowed"
```

---

## Cost Estimate — Typical Lab

| Resource | Estimated Cost (2h lab) |
|---------|------------------------|
| EC2 t3.micro | ~$0.01 |
| NAT Gateway | ~$0.09/h + $0.045/GB |
| RDS db.t3.micro Multi-AZ | ~$0.06/h |
| Lambda (1M req) | Free Tier |
| S3 (< 5GB) | Free Tier |
| ECS Fargate (0.25vCPU/0.5GB) | ~$0.01/h |

> **Tip:** Always destroy resources at the end. NAT Gateway is charged per hour even without traffic.

---

## Exam Tips

| Clue in the Question | Expected Answer |
|-----------------|------------------|
| "test Lambda locally before deploy" | SAM local invoke / sam local start-api |
| "infrastructure as code, reproducible" | Terraform or CloudFormation |
| "Lambda needs RDS in private VPC" | Lambda VpcConfig + RDS SG opened |
| "visualize changes before applying" | terraform plan |
| "Lambda cannot access internet in VPC" | Missing NAT Gateway in private subnet |
| "store secrets for Lambda to access" | Secrets Manager (not environment variables) |
| "serverless deploy with simplified YAML" | SAM (template.yaml) |
| "shared infrastructure state across teams" | Terraform state in S3 + DynamoDB lock |
| "debug error 403 S3" | Check bucket policy + Block Public Access + IAM |
| "ECS task stops right after starting" | Check stoppedReason + CloudWatch Logs /ecs/ |
