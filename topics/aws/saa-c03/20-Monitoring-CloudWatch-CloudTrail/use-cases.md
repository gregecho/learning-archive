# Real Use Cases — Monitoring: CloudWatch, CloudTrail and Config (Module 14)

## Case 1 — Full Stack Observability for Critical Application

**Context:** Payment platform needs 360-degree monitoring — infrastructure, application, and business — with proactive alerts and executive dashboards. SLA of 99.95% availability.

**Requirements:**
- Alerts in < 5 minutes for any degradation
- Correlate application errors with infrastructure metrics
- Real-time dashboard for NOC (Network Operations Center)
- Automated post-mortem after each incident

**Architecture:**
```
INFRASTRUCTURE LAYER:
EC2/ECS → CloudWatch Agent → CW Metrics
  (CPU, mem, disk, active connections)

APPLICATION LAYER:
Lambda/ECS → CloudWatch Logs
           → Embedded Metrics Format (metrics from logs)
           → X-Ray (distributed tracing)

BUSINESS LAYER:
Lambda → PutMetricData → CW Custom Metrics
  (orders/min, transaction value, approval rate)

ALERTS:
CW Alarms (composite) → SNS → PagerDuty + Slack + Email
  └── Composite Alarm: CPU > 80% AND Latency > 2s AND Error Rate > 5%

DASHBOARDS:
CloudWatch Dashboard (NOC — technical metrics)
QuickSight (executives — business metrics)

POST-MORTEM:
CloudTrail → S3 → Athena (who did what during the incident)
X-Ray Service Map (where latency first appeared)
CloudWatch Logs Insights (query logs from the incident period)
```

**Composite Alarm (does not trigger without co-occurrence of conditions):**
```
ALARM IF:
  (CPUAlarm = ALARM)
  AND (LatencyAlarm = ALARM)
  → Avoids isolated false positives
```

---

## Case 2 — Security and Compliance Auditing with CloudTrail

**Context:** Healthcare company (HIPAA) needs to track all user and service actions on patient data. Annual external audit requires evidence of 365 days of immutable logs.

**Requirements:**
- Log 100% of AWS API actions
- Immutable logs (cannot be altered or deleted)
- Real-time alerts for high-risk actions (delete EC2, modify IAM)
- Log queries for investigations: "who deleted the S3 bucket on Friday?"

**Architecture:**
```
SOURCE:
CloudTrail (multi-region trail enabled)
├── Management Events (control actions — always enabled)
├── Data Events (S3 GetObject/PutObject for PHI buckets)
└── Insights Events (unusual API activity)

IMMUTABLE STORAGE:
CloudTrail → S3 (cloudtrail-logs-hipaa)
               └── Object Lock (COMPLIANCE mode, 365 days)
               └── SSE-KMS (encryption with CMK)
               └── MFA Delete enabled

ANALYSIS:
S3 (CloudTrail logs) → Athena (investigation queries)

REAL-TIME ALERTS:
CloudTrail → CloudWatch Logs → CW Metric Filters
  ├── Filter: "DeleteBucket" → CW Alarm → SNS → PagerDuty
  ├── Filter: "CreateUser" or "AttachUserPolicy" → Alarm
  └── Filter: "ConsoleLoginFailures" > 5/min → Alarm

ATHENA QUERY EXAMPLE (investigation):
SELECT eventtime, useridentity.arn, sourceIPAddress, requestParameters
FROM cloudtrail_logs
WHERE eventname = 'DeleteBucket'
  AND DATE(eventtime) = '2024-01-15'
ORDER BY eventtime DESC;
```

---

## Case 3 — EC2 Governance with AWS Config + Systems Manager

**Context:** Company with 500 EC2 instances across multiple accounts needs to ensure all instances follow security standards: no direct public IP, patches applied, approved AMI, required tags.

**Requirements:**
- Automatically detect non-compliant instances
- Automatically remediate when possible (e.g., apply patch)
- Monthly compliance report for CISO
- Prevent creation of non-compliant resources (preventive)

**Architecture:**
```
AWS Config (enabled in all accounts via Organizations)
  Managed Rules:
  ├── ec2-no-amazon-key-pair (no key pair = SSH hardcoded)
  ├── ec2-instance-no-public-ip (no direct public IP)
  ├── approved-amis-by-id (only internal catalog AMIs)
  ├── required-tags (Environment, Owner, CostCenter)
  └── ec2-managedinstance-patch-compliance-status-check

  NON-COMPLIANT:
  Config → EventBridge → Lambda (automatic remediation)
    ├── Missing tag → Lambda adds default tag
    └── Outdated patch → SSM Automation (patch group)

  SSM Patch Manager:
  ├── Patch Baseline (automatic approval of critical patches in 7 days)
  ├── Maintenance Window (window: Sundays 2am-6am)
  └── Patch Group by tag: Environment=Production

REPORT:
AWS Config → Conformance Pack → S3 (compliance report)
Security Hub (aggregates findings from Config + GuardDuty + Inspector)
```

---

## Case 4 — Threat Detection with GuardDuty + Security Hub

**Context:** Startup attacked by crypto mining on compromised EC2 instances. They need a proactive system that detects and automatically responds to threats.

**Requirements:**
- Detect anomalous behavior (exfiltration, mining, C2 communication)
- Automatic response in < 1 minute (isolate compromised instance)
- Centralize findings from multiple security sources
- Notify security team immediately

**Architecture:**
```
DETECTION:
GuardDuty (analyzes VPC Flow Logs + DNS Logs + CloudTrail)
  High-severity findings:
  ├── CryptoCurrency:EC2/BitcoinTool.B (communication to mining pool)
  ├── Backdoor:EC2/Spambot (spam sending)
  ├── Trojan:EC2/BlackholeTraffic (connection to malicious domain)
  └── UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B (suspicious login)

AUTOMATIC RESPONSE:
GuardDuty Finding → EventBridge Rule (severity >= HIGH)
       │
       ▼
  Lambda (incident-responder)
  ├── EC2: RemoveFromLoadBalancer (removes from traffic)
  ├── EC2: CreateSecurityGroup (blocks all inbound/outbound)
  ├── EC2: ModifyInstanceAttribute (isolates in quarantine SG)
  ├── IAM: DetachUserPolicies (if IAM user compromised)
  └── SNS → PagerDuty (alerts security team)

CENTRALIZATION:
Security Hub (aggregates GuardDuty + Config + Inspector + Macie)
     └── Standardized findings (ASFF format)
     └── Executive dashboard (compliance score per account)
```

---

## Case 5 — Request Tracing with X-Ray in Microservices

**Context:** E-commerce platform with 12 microservices notices that some purchases take 8 seconds (target: < 2s). No visibility into which service is causing the slowness.

**Requirements:**
- Identify exact bottleneck (which service, which call)
- View dependencies between services
- Alert when p99 latency > 3s
- Correlate with errors (which slow requests also have errors)

**Architecture:**
```
API Gateway (X-Ray enabled)
     │ X-Ray Trace ID propagated in headers
     ▼
Lambda order-service (X-Ray SDK)
  Segments/Subsegments:
  ├── DynamoDB GetItem (products) — 15ms
  ├── DynamoDB PutItem (order) — 12ms
  ├── HTTP call → payment-service — 6,800ms ⚠️ BOTTLENECK
  └── SNS Publish — 8ms

payment-service (ECS/Lambda with X-Ray)
  ├── HTTP call → fraud-checker — 200ms
  ├── HTTP call → external-card-processor — 6,400ms ← ROOT CAUSE
  └── DynamoDB PutItem — 10ms

X-Ray Service Map:
  → Graphical visualization of all dependencies
  → Average latency per connection highlighted

CloudWatch Insights (correlation):
  filter @duration > 5000
  | stats avg(@duration), count(*) by service
```

**Discovery:** `external-card-processor` with 6s timeout without retry configured and without circuit breaker. Solution: cache results + reduced timeout + local fallback.

---
