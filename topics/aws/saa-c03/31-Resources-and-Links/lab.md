# Hands-On Lab — Resources and Links: Complete AWS Environment Setup (Module 21)

> **Estimated cost:** ~$0 (local configurations and account verifications)  
> **Prerequisites:** AWS CLI already installed; Python 3.8+

---

## Objective

Set up a professional AWS work environment: multiple CLI profiles, productive aliases, Terraform version management tool, and credential security best practices.

---

## Part 1 — AWS CLI: Multiple Profiles

```bash
# Check version and current configuration
aws --version
aws configure list-profiles

# Configure dev profile (least privilege for development)
aws configure --profile dev
# Fill in: Access Key ID, Secret, region us-east-1, output json

# Configure prod profile (more restricted access, MFA required)
aws configure --profile prod

# Configure profile using SSO (recommended for organizations)
aws configure sso --profile sso-dev
# Fill in: SSO start URL, SSO region, account ID, role name

# Use specific profile
export AWS_PROFILE=dev
aws sts get-caller-identity

# Useful aliases in ~/.bashrc or ~/.zshrc
cat >> ~/.bashrc << 'ALIASES'
# AWS Profile shortcuts
alias aws-dev='export AWS_PROFILE=dev && echo "Using profile: dev"'
alias aws-prod='export AWS_PROFILE=prod && echo "Using profile: prod"'
alias aws-who='aws sts get-caller-identity'
alias aws-region='aws ec2 describe-availability-zones --query "AvailabilityZones[0].RegionName" --output text'

# Quick investigation aliases
alias s3ls='aws s3 ls'
alias ec2ls='aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key=='\''Name'\''].Value|[0]]" --output table'
alias lambdals='aws lambda list-functions --query "Functions[*].[FunctionName, Runtime, LastModified]" --output table'
ALIASES

source ~/.bashrc
```

---

## Part 2 — Secure Credential Management

```bash
# NEVER store keys in code. Check for keys in the repository:
# (Install git-secrets to prevent accidental commits)
# https://github.com/awslabs/git-secrets

# Access Key Rotation — best practices
echo "=== Check for old keys (>90 days) ==="
aws iam list-access-keys \
  --query 'AccessKeyMetadata[*].[AccessKeyId, Status, CreateDate]' \
  --output table

# Create new key and delete the old one
NEW_KEY=$(aws iam create-access-key \
  --query 'AccessKey.[AccessKeyId, SecretAccessKey]' \
  --output text)
echo "New key created (configure in ~/.aws/credentials before deleting the old one)"

# Check account password policies
aws iam get-account-password-policy 2>/dev/null || echo "No password policy configured"

# Configure secure password policy
aws iam update-account-password-policy \
  --minimum-password-length 14 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 5

echo "Password policy configured!"

# Check users without MFA
aws iam list-users --query 'Users[*].UserName' --output text | \
  tr '\t' '\n' | \
  while read USER; do
    MFA=$(aws iam list-mfa-devices --user-name "$USER" --query 'MFADevices' --output text)
    if [ -z "$MFA" ]; then
      echo "ALERT: User without MFA: $USER"
    fi
  done
```

---

## Part 3 — tfenv: Manage Terraform Versions

```bash
# Install tfenv (Linux/macOS)
git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv
export PATH="$HOME/.tfenv/bin:$PATH"
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc

# List available versions
tfenv list-remote | head -10

# Install specific version (used in the course)
tfenv install 1.7.5
tfenv use 1.7.5
terraform --version

# Pin version per project (.terraform-version file)
echo "1.7.5" > .terraform-version
echo "Terraform pinned to version 1.7.5 for this directory"

# For Windows: use winget or chocolatey
# winget install Hashicorp.Terraform
# choco install terraform --version=1.7.5
```

---

## Part 4 — AWS CLI Output Formats and JMESPath Queries

```bash
# Mastering JMESPath is essential for the exam (and for working with AWS CLI)

# Filter running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId, InstanceType, PrivateIpAddress]' \
  --output table

# Useful JMESPath functions
# sort_by — sort by field
aws s3api list-buckets \
  --query 'sort_by(Buckets, &CreationDate)[*].[Name, CreationDate]' \
  --output table

# contains — filter by text
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?contains(GroupName, `lab`)].[ GroupId, GroupName]' \
  --output table

# length — count results
aws s3api list-buckets --query 'length(Buckets)' --output text

# max_by/min_by — extremes
aws ec2 describe-instances \
  --query 'max_by(Reservations[*].Instances[], &LaunchTime).[InstanceId, LaunchTime]' \
  --output table

# Output in different formats
aws iam list-users --output json   # Full JSON
aws iam list-users --output table  # ASCII table (easy to read)
aws iam list-users --output text   # Plain text (good for scripts)
aws iam list-users --output yaml   # YAML (human-friendly)
```

---

## Part 5 — Account Audit Script

```python
# account_audit.py — Quick security and cost checks
import boto3
import json
from datetime import datetime, timedelta, timezone

def check_account():
    iam = boto3.client('iam')
    sts = boto3.client('sts')
    s3  = boto3.client('s3')
    ce  = boto3.client('ce', region_name='us-east-1')

    identity = sts.get_caller_identity()
    print(f"\n=== Account Audit: {identity['Account']} ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 1. Check root without MFA
    acct_summary = iam.get_account_summary()['SummaryMap']
    root_mfa = acct_summary.get('AccountMFAEnabled', 0)
    status_mfa = "OK" if root_mfa else "ALERT: MFA not enabled on root account!"
    print(f"\n1. Root account MFA: {status_mfa}")

    # 2. Old Access Keys
    print("\n2. Access Keys (IAM users):")
    users = iam.list_users()['Users']
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        for key in keys:
            created = key['CreateDate']
            age = (datetime.now(timezone.utc) - created).days
            flag = "ALERT: >90 days" if age > 90 else "ok"
            print(f"   {user['UserName']}: key {key['AccessKeyId'][:8]}... ({age} days) [{flag}]")

    # 3. Public S3 Buckets
    print("\n3. S3 Buckets with potential public access:")
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        try:
            pab = s3.get_public_access_block(Bucket=bucket['Name'])['PublicAccessBlockConfiguration']
            if not all(pab.values()):
                print(f"   CHECK: {bucket['Name']} — some Block Public Access disabled")
        except Exception:
            print(f"   CHECK: {bucket['Name']} — no Block Public Access configuration")

    # 4. Cost last 30 days
    print("\n4. Cost last 30 days (top 3 services):")
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    try:
        cost = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        services = cost['ResultsByTime'][0]['Groups']
        top3 = sorted(services, key=lambda x: float(x['Metrics']['BlendedCost']['Amount']), reverse=True)[:3]
        for s in top3:
            print(f"   {s['Keys'][0]}: ${float(s['Metrics']['BlendedCost']['Amount']):.2f}")
    except Exception as e:
        print(f"   No access to Cost Explorer: {e}")

    print("\n=== Audit completed ===")

if __name__ == '__main__':
    check_account()
```

```bash
pip3 install boto3
python3 account_audit.py
```

---

## Part 6 — Final Exam Preparation

```bash
# Check if all key services are configured in your account
echo "=== Pre-exam checklist ==="

check() {
  echo -n "Checking $1... "
  if eval "$2" > /dev/null 2>&1; then
    echo "OK"
  else
    echo "not available (not critical for lab)"
  fi
}

check "EC2" "aws ec2 describe-availability-zones"
check "S3" "aws s3 ls"
check "IAM" "aws iam list-users"
check "Lambda" "aws lambda list-functions"
check "DynamoDB" "aws dynamodb list-tables"
check "RDS" "aws rds describe-db-instances"
check "VPC" "aws ec2 describe-vpcs"
check "CloudWatch" "aws cloudwatch list-metrics --namespace AWS/EC2"
check "Cost Explorer" "aws ce list-cost-category-definitions"

echo ""
echo "=== Study Resources (last 48h before exam) ==="
echo "1. Review cheatsheet.md from each module"
echo "2. Focus on modules with <70% on Tutorials Dojo practice exam"
echo "3. Do not study new content — consolidate what you already know"
echo "4. Sleep well, eat properly, arrive 30min early"
echo "5. Read ALL options before choosing — eliminate the absurd ones"
```

---

## Cleanup

```bash
rm -f account_audit.py
echo "Nothing to destroy — no cloud resources created in this lab."
```

---

## What You Learned

- AWS CLI `--profile` + `AWS_PROFILE`: work with multiple accounts securely
- JMESPath queries: `sort_by`, `contains`, `length`, `max_by` — essential for automation
- **Never** hardcode credentials: use roles, profiles, SSO, or AWS Vault
- Password policy + MFA + key rotation = more secure account
- `simulate-principal-policy` + `account_audit.py` = debugging and proactive governance
- Before the exam: consolidate > study new; sleep and nutrition impact cognitive performance
