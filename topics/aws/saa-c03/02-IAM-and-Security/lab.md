# Lab — IAM and Security

> **Region:** us-east-1  
> **Estimated cost:** ~$1–3/month (KMS CMK) + EC2 time if used  
> **Prerequisite:** AWS CLI configured, Terraform >= 1.5

## Lab Objectives
1. Create a Customer-Managed CMK in KMS with a custom key policy
2. Create a cross-account role with MFA condition and PrincipalOrgID
3. Store and rotate a credential in Secrets Manager
4. Use Parameter Store with SecureString encrypted with a custom CMK

---

## Part 1: CMK in KMS via AWS CLI

```bash
# Variables
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"

# Create CMK with description
KEY_ID=$(aws kms create-key \
  --description "CMK for IAM and Security lab" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS \
  --region $REGION \
  --query KeyMetadata.KeyId --output text)

echo "CMK created: $KEY_ID"

# Create friendly alias
aws kms create-alias \
  --alias-name alias/lab-iam-security \
  --target-key-id $KEY_ID \
  --region $REGION

# Enable automatic annual rotation
aws kms enable-key-rotation \
  --key-id $KEY_ID \
  --region $REGION

# Test encryption
echo "sensitive data" | base64 | aws kms encrypt \
  --key-id alias/lab-iam-security \
  --plaintext fileb:///dev/stdin \
  --output text \
  --query CiphertextBlob \
  --region $REGION > /tmp/encrypted.b64

echo "Encrypted data: $(cat /tmp/encrypted.b64)"

# Decrypt
aws kms decrypt \
  --ciphertext-blob fileb://<(base64 -d /tmp/encrypted.b64) \
  --output text \
  --query Plaintext \
  --region $REGION | base64 -d
```

---

## Part 2: Terraform — CMK + Cross-Account Role + Secrets Manager

```hcl
# main.tf

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
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ──────────────────────────────────────────────────────
# 1. Customer-Managed KMS Key
# ──────────────────────────────────────────────────────

data "aws_iam_policy_document" "kms_key_policy" {
  # Root account: full administration (recover always)
  statement {
    sid    = "EnableRootAdmin"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  # AWS services (Secrets Manager, SSM) can use the key
  statement {
    sid    = "AllowAWSServices"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["secretsmanager.amazonaws.com", "ssm.amazonaws.com"]
    }
    actions = [
      "kms:GenerateDataKey*",
      "kms:Decrypt",
      "kms:Encrypt",
    ]
    resources = ["*"]
  }

  # App role: encrypt/decrypt only, no key administration
  statement {
    sid    = "AllowAppRole"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.app_role.arn]
    }
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
      "kms:DescribeKey",
    ]
    resources = ["*"]
  }
}

resource "aws_kms_key" "lab_cmk" {
  description             = "CMK for IAM and Security SAA-C03 lab"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.kms_key_policy.json
}

resource "aws_kms_alias" "lab_cmk_alias" {
  name          = "alias/saa-lab-iam-security"
  target_key_id = aws_kms_key.lab_cmk.key_id
}

# ──────────────────────────────────────────────────────
# 2. IAM Role for Application (with permission boundary)
# ──────────────────────────────────────────────────────

resource "aws_iam_policy" "app_boundary" {
  name        = "AppPermissionBoundary"
  description = "Maximum permission limit for application roles"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:Get*", "s3:Put*", "s3:List*"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:us-east-1:${data.aws_caller_identity.current.account_id}:secret:/app/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.lab_cmk.arn
      }
    ]
  })
}

resource "aws_iam_role" "app_role" {
  name                 = "saa-lab-app-role"
  permissions_boundary = aws_iam_policy.app_boundary.arn

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "app_profile" {
  name = "saa-lab-app-profile"
  role = aws_iam_role.app_role.name
}

# ──────────────────────────────────────────────────────
# 3. Secrets Manager — Secret encrypted with CMK
# ──────────────────────────────────────────────────────

resource "aws_secretsmanager_secret" "db_secret" {
  name                    = "/app/prod/db-credentials"
  description             = "Production database credentials"
  kms_key_id              = aws_kms_key.lab_cmk.arn
  recovery_window_in_days = 7

  tags = {
    Environment = "lab"
    Module      = "02-IAM-e-Seguranca"
  }
}

resource "aws_secretsmanager_secret_version" "db_secret_v1" {
  secret_id = aws_secretsmanager_secret.db_secret.id
  secret_string = jsonencode({
    username = "app_user"
    password = "TemporaryPassword123!"
    host     = "rds-endpoint.us-east-1.rds.amazonaws.com"
    port     = 5432
    dbname   = "appdb"
  })
}

# ──────────────────────────────────────────────────────
# 4. Parameter Store — SecureString with custom CMK
# ──────────────────────────────────────────────────────

resource "aws_ssm_parameter" "app_config" {
  name   = "/app/prod/api-key"
  type   = "SecureString"
  value  = "my-temporary-api-key-for-lab"
  key_id = aws_kms_key.lab_cmk.arn

  tags = {
    Environment = "lab"
    Module      = "02-IAM-e-Seguranca"
  }
}

# ──────────────────────────────────────────────────────
# Outputs
# ──────────────────────────────────────────────────────

output "cmk_key_id" {
  value       = aws_kms_key.lab_cmk.key_id
  description = "ID of the created CMK"
}

output "cmk_arn" {
  value       = aws_kms_key.lab_cmk.arn
  description = "ARN of the CMK"
}

output "app_role_arn" {
  value       = aws_iam_role.app_role.arn
  description = "ARN of the application role"
}

output "secret_arn" {
  value       = aws_secretsmanager_secret.db_secret.arn
  description = "ARN of the secret in Secrets Manager"
}
```

---

## Part 3: Testing and Validation

```bash
# Check key rotation status
aws kms get-key-rotation-status \
  --key-id alias/saa-lab-iam-security \
  --region us-east-1

# List secret versions
aws secretsmanager describe-secret \
  --secret-id /app/prod/db-credentials \
  --region us-east-1

# Get the secret (simulates what the application does)
aws secretsmanager get-secret-value \
  --secret-id /app/prod/db-credentials \
  --region us-east-1 \
  --query SecretString --output text | python3 -m json.tool

# Get SSM parameter
aws ssm get-parameter \
  --name /app/prod/api-key \
  --with-decryption \
  --region us-east-1 \
  --query Parameter.Value --output text

# See who used the CMK (last 24h via CloudTrail)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=Decrypt \
  --start-time $(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ) \
  --region us-east-1 \
  --query 'Events[].{User:Username,Time:EventTime,Source:EventSource}' \
  --output table
```

---

## Cleanup (important to avoid costs)

```bash
# Terraform destroy
terraform destroy -auto-approve

# Or manually via CLI:

# Schedule CMK deletion (minimum 7 days, not immediate)
aws kms schedule-key-deletion \
  --key-id $(aws kms describe-key --key-id alias/saa-lab-iam-security \
    --query KeyMetadata.KeyId --output text) \
  --pending-window-in-days 7 \
  --region us-east-1

# Delete secret (recovery_window_in_days=0 for immediate deletion)
aws secretsmanager delete-secret \
  --secret-id /app/prod/db-credentials \
  --force-delete-without-recovery \
  --region us-east-1

# Delete SSM parameter
aws ssm delete-parameter \
  --name /app/prod/api-key \
  --region us-east-1

echo "Cleanup complete. CMK will be deleted in 7 days."
```

---

## Review Points

- [ ] Why does the KMS key policy include the root account as administrator?
- [ ] What happens if you delete the key policy and the root account is not listed?
- [ ] What is the difference between `kms:Encrypt` and `kms:GenerateDataKey*`?
- [ ] Why is the Permission Boundary not sufficient on its own? What else is needed?
- [ ] In which scenario is `aws:PrincipalOrgID` more efficient than listing account IDs?

