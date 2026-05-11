# Hands-On Lab — Advanced IAM: Roles, SCPs and STS (Module 09)

> **Region:** us-east-1 | **Estimated cost:** ~$0 (IAM and STS are free)  
> **Prerequisites:** AWS CLI configured

---

## Objective

Practice advanced IAM: create roles with trust policies, SCPs in Organizations, cross-account AssumeRole, and use the Policy Simulator to validate permissions.

---

## Part 1 — IAM Roles: Trust Policy and Permission Policy

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 1. Role for EC2 to access S3 and DynamoDB
EC2_ROLE_ARN=$(aws iam create-role \
  --role-name "lab-ec2-app-role" \
  --description "Role for EC2 application — S3 and DynamoDB access" \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }' \
  --query 'Role.Arn' --output text)

# Create customer managed policy with least privilege
APP_POLICY_ARN=$(aws iam create-policy \
  --policy-name "lab-app-policy" \
  --description "Minimum required access for e-commerce app" \
  --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Sid\": \"S3ReadWrite\",
        \"Effect\": \"Allow\",
        \"Action\": [\"s3:GetObject\", \"s3:PutObject\", \"s3:DeleteObject\", \"s3:ListBucket\"],
        \"Resource\": [
          \"arn:aws:s3:::app-data-${ACCOUNT_ID}\",
          \"arn:aws:s3:::app-data-${ACCOUNT_ID}/*\"
        ]
      },
      {
        \"Sid\": \"DynamoDBCRUD\",
        \"Effect\": \"Allow\",
        \"Action\": [
          \"dynamodb:GetItem\", \"dynamodb:PutItem\", \"dynamodb:UpdateItem\",
          \"dynamodb:DeleteItem\", \"dynamodb:Query\", \"dynamodb:BatchWriteItem\"
        ],
        \"Resource\": \"arn:aws:dynamodb:us-east-1:${ACCOUNT_ID}:table/orders\"
      },
      {
        \"Sid\": \"WriteLogs\",
        \"Effect\": \"Allow\",
        \"Action\": [\"logs:CreateLogGroup\", \"logs:CreateLogStream\", \"logs:PutLogEvents\"],
        \"Resource\": \"arn:aws:logs:us-east-1:${ACCOUNT_ID}:log-group:/app/*\"
      }
    ]
  }" \
  --query 'Policy.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-ec2-app-role" \
  --policy-arn "$APP_POLICY_ARN"

# Create Instance Profile for EC2
aws iam create-instance-profile --instance-profile-name "lab-ec2-app-profile"
aws iam add-role-to-instance-profile \
  --instance-profile-name "lab-ec2-app-profile" \
  --role-name "lab-ec2-app-role"

echo "Instance Profile created: lab-ec2-app-profile"

# 2. Cross-account role (for CI/CD in another account to assume)
CICD_ROLE_ARN=$(aws iam create-role \
  --role-name "lab-cicd-deploy-role" \
  --description "Role assumed by CI/CD pipeline for deployment" \
  --assume-role-policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [{
      \"Effect\": \"Allow\",
      \"Principal\": {
        \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\"
      },
      \"Action\": \"sts:AssumeRole\",
      \"Condition\": {
        \"StringEquals\": {\"sts:ExternalId\": \"pipeline-secret-xyz\"},
        \"Bool\": {\"aws:MultiFactorAuthPresent\": \"false\"}
      }
    }]
  }" \
  --query 'Role.Arn' --output text)

aws iam attach-role-policy \
  --role-name "lab-cicd-deploy-role" \
  --policy-arn "arn:aws:iam::aws:policy/AmazonECS_FullAccess"

echo "CICD Deploy Role: $CICD_ROLE_ARN"
```

---

## Part 2 — STS AssumeRole

```bash
# Assume the CI/CD role with ExternalId
CREDS=$(aws sts assume-role \
  --role-arn "$CICD_ROLE_ARN" \
  --role-session-name "pipeline-deploy-session" \
  --external-id "pipeline-secret-xyz" \
  --duration-seconds 900 \
  --query 'Credentials' --output json)

AK=$(echo "$CREDS" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c['AccessKeyId'])")
SK=$(echo "$CREDS" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c['SecretAccessKey'])")
ST=$(echo "$CREDS" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c['SessionToken'])")
EXP=$(echo "$CREDS" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c['Expiration'])")

echo "Temporary credentials (expire at: $EXP)"

# Verify that the identity has changed
AWS_ACCESS_KEY_ID="$AK" \
AWS_SECRET_ACCESS_KEY="$SK" \
AWS_SESSION_TOKEN="$ST" \
aws sts get-caller-identity

# STS GetCallerIdentity without assuming a role (who am I now)
aws sts get-caller-identity

# STS with session tags (for ABAC)
CREDS_TAGGED=$(aws sts assume-role \
  --role-arn "$CICD_ROLE_ARN" \
  --role-session-name "session-with-tags" \
  --external-id "pipeline-secret-xyz" \
  --tags '[
    {"Key": "Environment", "Value": "staging"},
    {"Key": "Team", "Value": "backend"},
    {"Key": "Project", "Value": "ecommerce"}
  ]' \
  --query 'Credentials.AccessKeyId' --output text)

echo "Session with tags: $CREDS_TAGGED"
```

---

## Part 3 — Policy Simulator

```bash
# Simulate EC2 role permissions
echo "=== EC2 role permission simulation ==="

aws iam simulate-principal-policy \
  --policy-source-arn "arn:aws:iam::${ACCOUNT_ID}:role/lab-ec2-app-role" \
  --action-names \
    "s3:GetObject" \
    "s3:PutObject" \
    "s3:DeleteBucket" \
    "dynamodb:PutItem" \
    "dynamodb:CreateTable" \
    "ec2:RunInstances" \
    "iam:CreateRole" \
    "logs:PutLogEvents" \
  --resource-arns "arn:aws:s3:::app-data-${ACCOUNT_ID}/*" \
  --query 'EvaluationResults[*].[EvalActionName, EvalDecision]' \
  --output table

# Simulate with context conditions
echo ""
echo "=== Simulation with MFA context ==="
aws iam simulate-principal-policy \
  --policy-source-arn "arn:aws:iam::${ACCOUNT_ID}:role/lab-ec2-app-role" \
  --action-names "iam:DeleteRole" \
  --resource-arns "*" \
  --context-entries '[{
    "ContextKeyName": "aws:MultiFactorAuthPresent",
    "ContextKeyValues": ["true"],
    "ContextKeyType": "boolean"
  }]' \
  --query 'EvaluationResults[0].[EvalActionName, EvalDecision]' \
  --output table
```

---

## Part 4 — Common IAM Conditions

```bash
# Policy with advanced conditions for study
cat << 'JSON'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyOutsideBusinessHours",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "*",
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": ["203.0.113.0/24", "198.51.100.0/24"]
        }
      }
    },
    {
      "Sid": "RequireMFAForIAM",
      "Effect": "Deny",
      "Action": ["iam:*", "sts:*"],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    },
    {
      "Sid": "ForceHTTPS",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
JSON

echo ""
echo "=== Most commonly used conditions on the exam ==="
echo "aws:SourceIp          — source IP restriction"
echo "aws:SourceVpc         — source VPC restriction"
echo "aws:RequestedRegion   — request region"
echo "aws:SecureTransport   — enforce HTTPS"
echo "aws:MultiFactorAuthPresent — requires MFA"
echo "sts:ExternalId        — cross-account partners (confused deputy)"
echo "aws:PrincipalTag/X    — ABAC: identity tag"
echo "aws:ResourceTag/X     — ABAC: resource tag"
echo "s3:prefix             — S3 object prefix"
echo "ec2:InstanceType      — limit instance types"
```

---

## Cleanup

```bash
# Remove instance profile
aws iam remove-role-from-instance-profile \
  --instance-profile-name "lab-ec2-app-profile" \
  --role-name "lab-ec2-app-role"
aws iam delete-instance-profile --instance-profile-name "lab-ec2-app-profile"

# Detach policies and delete roles
aws iam detach-role-policy \
  --role-name "lab-ec2-app-role" \
  --policy-arn "$APP_POLICY_ARN"
aws iam delete-policy --policy-arn "$APP_POLICY_ARN"
aws iam delete-role --role-name "lab-ec2-app-role"

aws iam detach-role-policy \
  --role-name "lab-cicd-deploy-role" \
  --policy-arn "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
aws iam delete-role --role-name "lab-cicd-deploy-role"
```

---

## What You Learned

- **Trust Policy:** who CAN assume the role (Principal); **Permission Policy:** what the role CAN do
- **ExternalId:** protection against confused deputy attack in cross-account roles
- **Instance Profile:** required wrapper to attach an IAM Role to EC2
- **Session Tags:** passed in AssumeRole; used in ABAC policies with `aws:PrincipalTag`
- **STS duration:** max 12h for human roles; default 1h for service roles
- **simulate-principal-policy:** the only safe way to test permissions without making real calls

---
