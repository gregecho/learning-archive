# Use Cases — IAM and Security

## Case 1: Secure Cross-Account Access with MFA for Critical Operations

**Context:**  
A company has a production AWS account (`prod-account`) and a DevOps tools account (`devops-account`). Engineers work in `devops-account` and need to perform deployments in `prod-account`. Destructive operations (deleting ECR images, snapshots) must require MFA.

**Requirements:**
- Engineers in devops-account assume a role in prod-account
- Destructive operations require MFA
- Only the "Engineering" OU of the organization can assume the role

**Architecture:**

```
devops-account (Engineers)              prod-account
┌─────────────────────┐                ┌──────────────────────────────┐
│ IAM User: eng-user  │                │ IAM Role: DevOpsDeployRole    │
│  └── Policy:        │  AssumeRole    │  ├── Trust Policy:            │
│       sts:AssumeRole│───────────────▶│  │  Allow: devops-account     │
│       (with MFA)    │                │  │  Condition: MFA + OrgID    │
└─────────────────────┘                │  └── Permission Policy:       │
                                       │       - ecs:*                 │
                                       │       - ecr:*                 │
                                       │       - ec2:DescribeInstances │
                                       │       - Deny: DeleteX w/o MFA │
                                       └──────────────────────────────┘
```

**Role Trust Policy (prod-account):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
    "Action": "sts:AssumeRole",
    "Condition": {
      "Bool": {"aws:MultiFactorAuthPresent": "true"},
      "StringEquals": {"aws:PrincipalOrgID": "o-xxxxxxxxxx"}
    }
  }]
}
```

**Permission Policy with destructive Deny without MFA:**
```json
{
  "Statement": [{
    "Effect": "Deny",
    "Action": ["ecr:DeleteRepository", "ec2:DeleteSnapshot", "rds:DeleteDBInstance"],
    "Resource": "*",
    "Condition": {
      "BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}
    }
  }]
}
```

**Tested concepts:** cross-account role assumption, Trust Policy, MFA condition, PrincipalOrgID, explicit deny

---

## Case 2: KMS with Envelope Encryption for Sensitive Data in S3

**Context:**  
A fintech needs to encrypt customer files in S3 with a customer-managed CMK, ensure that only the specific application can decrypt (not all devs), and have audit logs of who accessed the key.

**Architecture:**

```
                    ┌──────────────────────────────────┐
EC2 (app-role)      │  KMS Customer-Managed CMK         │
  │                 │  ╔══════════════════════════════╗ │
  ├─GenerateDataKey▶│  ║ Key Policy:                  ║ │
  │◀── data key ────│  ║ - Root account: admin        ║ │
  │                 │  ║ - key-admin-role: manage      ║ │
  │  Encrypt data   │  ║ - app-role: kms:GenerateKey  ║ │
  │  with plaintext │  ║              kms:Decrypt      ║ │
  │  data key       │  ║ - DENY: kms:Decrypt           ║ │
  │                 │  ║   if NOT app-role             ║ │
  ├─Store to S3────▶│  ╚══════════════════════════════╝ │
  │  {              └──────────────────────────────────┘
  │   encrypted_data,                 │
  │   encrypted_data_key              │ CloudTrail
  │  }                                ▼
  └─────────────────────────  Audit logs:
                              - Who called kms:Decrypt
                              - From which EC2 (via ARN)
                              - Source IP
```

**Design decision:** Why CMK and not SSE-S3?
- SSE-S3: AWS manages the key → no control over who decrypts
- CMK: key policy defines exactly which roles can use it → principle of least privilege
- Annual automatic rotation can be enabled
- CloudTrail records every use of the CMK (GenerateDataKey, Decrypt)

**Tested concepts:** Customer-managed CMK, key policy, envelope encryption, auditing via CloudTrail

---

## Case 3: Secrets Manager for Automatic RDS Credential Rotation

**Context:**  
A Node.js application on EC2 accesses an RDS PostgreSQL database. The security policy requires password rotation every 30 days without application downtime.

**Architecture:**

```
EC2 (app-role)                                  Secrets Manager
   │                                           ┌──────────────────────┐
   │ GetSecretValue(SecretId)                  │  /app/prod/rds-master │
   ├─────────────────────────────────────────▶ │  {                   │
   │◀── {username, password, host, port}────── │   "username": "app", │
   │                                           │   "password": "xxxx" │
   │                                           │   "host": "db.xxx",  │
   │                                           │   "port": 5432       │
   │                                           │  }                   │
    (Application NEVER stores password locally) └────────┬─────────────┘
                                                         │ Rotation (30d)
                                               ┌─────────▼─────────────┐
                                               │ Lambda (rotation fn)  │
                                               │  1. createSecret       │
                                               │  2. setSecret (new pw) │
                                               │  3. testSecret (verify)│
                                               │  4. finishSecret       │
                                               └───────────────────────┘
                                                         │
                                               ┌─────────▼─────────────┐
                                               │  RDS PostgreSQL        │
                                               │  ALTER USER app        │
                                               │  PASSWORD 'new_pw'     │
                                               └───────────────────────┘
```

**IAM for the EC2 instance:**
```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:us-east-1:123456789:secret:/app/prod/rds-master*",
  "Condition": {
    "StringEquals": {"aws:RequestedRegion": "us-east-1"}
  }
}
```

**Tested concepts:** Secrets Manager, automatic rotation, instance profile, GetSecretValue, ResourceARN with wildcard

---

## Case 4: Permission Boundary for Delegating Role Creation

**Context:**  
A company wants to allow the DevOps team to create IAM roles for applications, but without them being able to create a role with more permissions than they themselves have (privilege escalation).

**Solution:**

```
Admin (SysOps)
  └── Creates Permission Boundary Policy (max-app-boundary)
        Allows only: ec2:Describe*, s3:Get*, s3:Put*, sqs:*, cloudwatch:*
        Denies: iam:*, kms:*, ec2:RunInstances

  └── Creates Policy for DevOps with condition:
        Allow: iam:CreateRole, iam:AttachRolePolicy
        Condition: iam:PermissionsBoundary = arn:...max-app-boundary

DevOps Team
  └── Can create roles ONLY IF:
        - Attaches the max-app-boundary boundary
        - The final role is limited by the boundary
        - Even if DevOps tries to grant AdministratorAccess,
          the boundary limits the effective result
```

**DevOps team policy:**
```json
{
  "Effect": "Allow",
  "Action": ["iam:CreateRole", "iam:AttachRolePolicy", "iam:PutRolePolicy"],
  "Resource": "arn:aws:iam::*:role/app-*",
  "Condition": {
    "StringEquals": {
      "iam:PermissionsBoundary": "arn:aws:iam::123456789:policy/max-app-boundary"
    }
  }
}
```

**Tested concepts:** Permission Boundary, privilege escalation prevention, delegated administration

---

## Case 5: S3 Access Restricted to VPC Endpoint Only

**Context:**  
A company wants to ensure that confidential data in S3 is only accessed from within the corporate VPC, blocking any external access (including direct access with valid credentials over the internet).

**Bucket Policy:**
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": [
    "arn:aws:s3:::company-confidential",
    "arn:aws:s3:::company-confidential/*"
  ],
  "Condition": {
    "StringNotEquals": {
      "aws:SourceVpce": "vpce-0123456789abcdef"
    }
  }
}
```

```
Internet                   Private VPC
   │                          │
   │ ❌ DENY (no SourceVpce)  │ ✅ ALLOW (SourceVpce match)
   │                          │
   ×                         EC2       S3 Gateway Endpoint
            (Access blocked)  │         │
                              │◀────────┘
                         VPC Routing → S3 without internet gateway
```

**Tested concepts:** resource-based policy, aws:SourceVpce, VPC Gateway Endpoint for S3, zero-trust

