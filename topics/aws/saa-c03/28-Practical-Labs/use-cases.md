# Real-World Use Cases — Practical Labs (Module 28)

## Case 1 — Debug: Lambda Cannot Access RDS

**Context:** Development team deployed a Lambda that should write data to RDS MySQL inside a private VPC. Lambda works locally but returns timeout in production.

**Step-by-Step Diagnosis:**
```
SYMPTOM: Lambda invocation timeout (no explicit connection error)

STEP 1 — Check Lambda VpcConfig:
aws lambda get-function-configuration \
  --function-name MyFunction \
  --query 'VpcConfig'

Expected result:
{
  "SubnetIds": ["subnet-aaa", "subnet-bbb"],
  "SecurityGroupIds": ["sg-lambda"],
  "VpcId": "vpc-xxx"
}
If SubnetIds empty → Lambda is not in VPC → Add VpcConfig

STEP 2 — Check subnet type (must be PRIVATE):
aws ec2 describe-subnets \
  --subnet-ids subnet-aaa \
  --query 'Subnets[*].[SubnetId,MapPublicIpOnLaunch,AvailabilityZone]'

If MapPublicIpOnLaunch=True → public subnet → use private subnet

STEP 3 — Check Security Groups:
Lambda SG: allows outbound to port 3306 to RDS SG?
aws ec2 describe-security-groups --group-ids sg-lambda
→ Check: Outbound rule: TCP 3306 → sg-rds (or CIDR)

RDS SG: allows inbound from Lambda SG?
aws ec2 describe-security-groups --group-ids sg-rds  
→ Check: Inbound rule: TCP 3306 → sg-lambda

STEP 4 — Check Lambda IAM Role:
aws lambda get-function-configuration \
  --function-name MyFunction --query 'Role'
→ Role must have: AWSLambdaVPCAccessExecutionRole (to create ENI)

STEP 5 — Check Lambda timeout (must be > connection time):
aws lambda get-function-configuration \
  --function-name MyFunction --query 'Timeout'
→ Default is 3s. RDS cold connection can take 1-2s. Increase to 30s.

APPLIED SOLUTION:
1. Lambda was in PUBLIC subnet (no access to private RDS)
2. Fix: move Lambda to private subnets with NAT GW
3. Increase timeout from 3s to 30s
```

---

## Case 2 — Debug: S3 Returning 403 Forbidden

**Context:** ECS application receives 403 when trying to PutObject in an S3 bucket. Works on developer's machine but not on AWS.

**Diagnosis:**
```
STEP 1 — Identify which identity is making the request:
Local machine: uses dev's personal credentials (with full permission)
On ECS: uses task IAM Role (may not have permission)

Check which role the container is using:
curl http://169.254.170.2/v2/credentials  (only from inside ECS container)
→ Returns temporaryCredentials with RoleArn

STEP 2 — Check Task Role:
aws ecs describe-task-definition --task-definition MyTask \
  --query 'taskDefinition.taskRoleArn'
→ If null → no Task Role → no S3 permissions

Fix: create IAM Role for task with:
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject"],
  "Resource": "arn:aws:s3:::my-bucket/*"
}
Assign as taskRoleArn in task definition

STEP 3 — Check Bucket Policy:
aws s3api get-bucket-policy --bucket my-bucket
→ If explicit Deny for the role → fix bucket policy
→ If Condition: aws:SourceVpc → Lambda/ECS must be in correct VPC

STEP 4 — Check Block Public Access:
aws s3api get-public-access-block --bucket my-bucket
→ Not the problem if trying with IAM Role (not public access)

STEP 5 — Check KMS (if bucket uses SSE-KMS):
Does the role have kms:GenerateDataKey and kms:Decrypt on the key?
aws kms list-grants --key-id arn:aws:kms:...:key/xxx

SOLUTION:
Task Role did not exist → create and associate with correct permissions
```

---

## Case 3 — Deploy with Terraform: State Lock and Team Conflict

**Context:** Team A and Team B both run `terraform apply` at the same time. Team B receives state lock error. When unlocking, both had conflicting changes in state.

**Concept and Resolution:**
```
RECOMMENDED CONFIGURATION (S3 Backend + DynamoDB Lock):
# versions.tf
terraform {
  backend "s3" {
    bucket         = "terraform-states-prod"
    key            = "api-service/terraform.tfstate"  
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:..."  # SSE-KMS
    dynamodb_table = "terraform-locks"  # for state locking
  }
}

# DynamoDB table (created manually or with bootstrap script):
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

WHEN STATE GETS LOCKED (apply was interrupted):
terraform force-unlock LOCK_ID
# LOCK_ID is shown in the error message

BEST PRACTICE FOR TEAMS:
1. Each team has its own state file (different keys in S3)
2. Or: use Terraform workspaces
3. Or: use Terraform Cloud/Enterprise (native locking)
4. CI/CD pipeline (GitHub Actions) ensures only 1 apply runs at a time

DEBUG CONFLICT:
terraform state list  (see which resources are in state)
terraform state show aws_instance.web  (see current resource state)
terraform import aws_instance.web i-1234567890  (import existing resource)
```

---

## Case 4 — SAM: Lambda with Dependencies Layer

**Context:** Python Lambda needs pandas library (100 MB) which exceeds the 50 MB zip upload limit. Deploy is failing.

**Solution with SAM Layers:**
```
PROJECT STRUCTURE:
lambda-project/
  template.yaml
  src/
    app.py  (main code)
  layers/
    pandas-layer/
      python/
        requirements.txt  (pandas==2.1.0, numpy==1.26.0)

template.yaml:
Resources:
  PandasLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: pandas-layer
      ContentUri: layers/pandas-layer/
      CompatibleRuntimes:
        - python3.12
    Metadata:
      BuildMethod: python3.12  # SAM build compiles dependencies

  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Runtime: python3.12
      Layers:
        - !Ref PandasLayer
      MemorySize: 512  # pandas needs enough memory
      Timeout: 60

COMMANDS:
sam build  (compiles layer + code)
sam deploy --guided  (first time)

VERIFY:
aws lambda list-layers
aws lambda get-layer-version --layer-name pandas-layer --version-number 1

IMPORTANT LIMIT:
- Code + layers uncompressed: maximum 250 MB
- If pandas still > 250 MB: use Lambda container image (up to 10 GB)
```

---

## Case 5 — Debugging ECS Fargate Task that Stops Immediately

**Context:** ECS Fargate task starts but stops in seconds with STOPPED status. Console shows generic reason. Team doesn't know what's wrong.

**Complete Diagnosis:**
```
STEP 1 — Check stoppedReason:
aws ecs describe-tasks \
  --cluster my-cluster \
  --tasks arn:aws:ecs:...:task/TASK_ID \
  --query 'tasks[0].{stoppedReason:stoppedReason,status:lastStatus,containers:containers[*].{name:name,reason:reason,exitCode:exitCode}}'

COMMON CAUSES + SOLUTIONS:

A) "CannotPullContainerError: ... no such host"
   → ECR is in private VPC without endpoint
   Solution: Create VPC Endpoint for ECR (ecr.api, ecr.dkr, s3)
   OR: Use public subnet with NAT GW

B) "CannotPullContainerError: 403 Forbidden"  
   → Task Execution Role does not have ECR permission
   Solution: Add AmazonECRReadOnly to Task Execution Role

C) exitCode: 1, reason: "Essential container exited"
   → App crashed. Check logs in CloudWatch:
   aws logs tail /ecs/my-task --follow
   Check: environment variables, Secrets Manager secrets

D) "OutOfMemoryError: Container killed"
   → memoryReservation too low
   Solution: Increase memory in task definition

E) "ResourceInitializationError: unable to pull secrets"
   → Secrets Manager or SSM Parameter Store inaccessible
   Solution: VPC Endpoint for secretsmanager or route to internet

STEP 2 — Check detailed logs:
aws logs describe-log-groups | grep ecs
aws logs get-log-events \
  --log-group-name /ecs/my-task \
  --log-stream-name ecs/container-name/TASK_ID

STEP 3 — Test locally:
docker run -e DATABASE_URL=... -e SECRET=... my-image:latest
→ Reproducing error locally is much faster
```
