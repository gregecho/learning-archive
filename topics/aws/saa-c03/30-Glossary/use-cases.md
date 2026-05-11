# Real Use Cases — Glossary in Practice (Module 20)

## Case 1 — When "RTO" and "RPO" Determine the Architecture

**Context:** Exam question defines RTO and RPO as constraints. Candidate needs to know which DR strategy to choose based on these values.

**Application Scenarios:**
```
SCENARIO A: RPO = 0, RTO < 30s
(zero data loss, near-instant recovery)
→ Architecture: Active-Active Multi-Region
→ Aurora Global Database (sync lag < 1s ≈ RPO≈0)  
→ Route 53 Latency Routing (automatic failover ≈ 60s) 
→ Cost: $$$$

SCENARIO B: RPO ≤ 15min, RTO ≤ 1h
→ Architecture: Warm Standby
→ Aurora Global Database (read replica standby ready)
→ Auto Scaling: min = 1, max = 20 (scale when needed)
→ Cost: $$$

SCENARIO C: RPO ≤ 1h, RTO ≤ 4h  
→ Architecture: Pilot Light
→ RDS automatic backup (snapshots) + fast restore
→ EC2 AMIs ready, starts when needed
→ Cost: $$

SCENARIO D: RPO ≤ 24h, RTO can be days
→ Architecture: Backup & Restore
→ S3 + Glacier for backups
→ Manual restore scripts
→ Cost: $

MNEMONIC:
RPO = "how much data can I LOSE?" (looks to the past)
RTO = "how long can I be DOWN?" (looks to the future)
```

---

## Case 2 — Distinguishing "Durability" from "Availability"

**Context:** Question intentionally confuses the two terms.

**Difference in Practice:**
```
SCENARIO: S3 Standard
Durability: 99.999999999% (11 nines)
  → Probability of LOSING an object: 0.000000001% per year
  → In 10 million objects, expect to lose < 1 object in 10,000 years
  → "Will my data always exist?"

Availability: 99.99% 
  → Allowed downtime: ~52 min/year
  → "Can I access my data right now?"

ANALOGY:
Bank vault: high DURABILITY (money doesn't vanish)
            AVAILABILITY: may be closed on holidays

TRICK QUESTION:
"Which S3 class offers the lowest durability?"
→ S3 One Zone-IA: 99.999999999% (same durability!)
  Difference: only 1 AZ → lower AVAILABILITY if AZ fails
  Durability does not change (data replicated in 1 AZ)

ANSWER: "One Zone-IA has lower AVAILABILITY (not durability)"
```

---

## Case 3 — Applying the "Principle of Least Privilege" in IAM

**Context:** Question asks for the minimum IAM policy for a specific case.

**Scenario:** Lambda needs to read from 1 specific DynamoDB table and write logs to CloudWatch.

**Policy Analysis:**
```
WRONG — Excessive permission:
{
  "Effect": "Allow",
  "Action": "dynamodb:*",
  "Resource": "*"
}
→ DynamoDB:* = full access to ANY table
→ Violation of the Principle of Least Privilege

WRONG — More specific but still broad:
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem", "dynamodb:Scan", "dynamodb:Query"],
  "Resource": "*"  // ← still "*"
}
→ Allows reading from ALL tables

CORRECT — Minimum necessary:
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem", "dynamodb:Query"],
  "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/MyTable"
}

For CloudWatch Logs (created automatically by Lambda if role has it):
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:us-east-1:123456789:log-group:/aws/lambda/MyFunction:*"
}

NOTE: AWSLambdaBasicExecutionRole already includes basic logs — managed policy can be used
      For DynamoDB: always specify the specific table ARN
```

---

## Case 4 — CIDR and VPC Subnets in Practice

**Context:** VPC questions often ask to calculate available IPs or identify CIDR conflicts.

**Exercises:**
```
EXERCISE 1: How many usable IPs in a /24?
IPv4 /24 = 256 total addresses
AWS reserves 5 (network, GW, DNS+2, broadcast)
256 - 5 = 251 usable IPs

EXERCISE 2: Subnets for HA in 2 AZs with VPC 10.0.0.0/16:
VPC: 10.0.0.0/16 (65,536 addresses)
Subnet plan:
  Public AZ-a:  10.0.1.0/24 (251 usable)
  Public AZ-b:  10.0.2.0/24 (251 usable)
  Private AZ-a: 10.0.10.0/24 (251 usable)
  Private AZ-b: 10.0.11.0/24 (251 usable)
  DB AZ-a:      10.0.20.0/24 (251 usable)
  DB AZ-b:      10.0.21.0/24 (251 usable)

EXERCISE 3: VPC Peering — CIDR conflict:
VPC A: 10.0.0.0/16
VPC B: 10.0.0.0/24  ← CONFLICT! /24 is within /16
→ VPC Peering does NOT work with overlapping CIDRs
Solution: use distinct CIDRs (e.g., VPC B: 172.16.0.0/16)

EXAM TRAP:
/28 = smallest subnet allowed on AWS
/28 = 16 total addresses, 16 - 5 = 11 usable
```

---

## Case 5 — Shared Responsibility Model in Real Scenarios

**Context:** Question identifies who is responsible for security issues.

**Scenarios and Responsibilities:**
```
SCENARIO 1: EC2 with Windows Server was infected by ransomware
  CLIENT responsibility:
  ✓ Windows Server patches (client)
  ✓ Antivirus installed on the OS (client)
  ✓ Security Group configured correctly (client)
  AWS responsibility:
  ✓ Isolated hypervisor (AWS)
  ✓ Physical hardware (AWS)
  → CLIENT is responsible for OS infection

SCENARIO 2: Physical disk failure on the server hosting EC2
  → AWS is responsible (physical hardware)
  → AWS replaces hardware, EC2 migrates automatically (Live Migration)
  → Data on EBS is preserved (replicated within the AZ)

SCENARIO 3: S3 bucket with accidentally public data
  → CLIENT configured incorrect permission
  → AWS provided tools (Block Public Access, Macie, Config)
  → Client chose not to use them → CLIENT responsibility

SCENARIO 4: RDS MySQL with outdated OS
  → AWS manages RDS OS → AWS is responsible for OS patches
  → Client manages: data, database users, settings

SCENARIO 5: Lambda with code vulnerable to SQL Injection
  → CLIENT wrote the code → CLIENT is responsible
  → AWS provides the (secure) execution platform
  → CODE security = developer's responsibility

MNEMONIC RULE:
AWS = "of the cloud" (hardware, physical network, hypervisor, managed services OS)
Client = "in the cloud" (EC2 OS, code, data, IAM config, virtual network)
```
