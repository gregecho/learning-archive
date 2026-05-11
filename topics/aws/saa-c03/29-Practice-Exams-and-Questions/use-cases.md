# Real-World Use Cases — Practice Exams and Questions (Module 29)

## Case 1 — Analyzing a Difficult High Availability Question

**Context:** An exam question asks for the highest availability architecture for a relational database with a requirement of automatic failover < 30 seconds, with zero data loss.

**Simulated Question:**
> A company needs a MySQL relational database with RTO < 30 seconds and RPO = 0 (zero data loss). Which configuration meets these requirements?
> A) RDS MySQL with two Read Replicas in different AZs
> B) RDS MySQL Multi-AZ with synchronous replica in a separate AZ
> C) RDS MySQL with daily automatic backup enabled
> D) EC2 MySQL with Lambda failover script

**Analysis of Why Each Option Is Right or Wrong:**
```
A) ❌ Read Replicas are ASYNCHRONOUS → may have lag (RPO ≠ 0)
      Read Replicas do not do automatic failover for writes
      Read Replicas = scale reads, not HA

B) ✅ CORRECT:
   Multi-AZ = SYNCHRONOUS replica → RPO = 0 (no data loss)
   Automatic failover: 15-30 seconds
   DNS endpoint changes automatically to standby
   
C) ❌ Daily backup = RPO of up to 24h (nowhere near 0)
      Restore from backup takes hours (RTO very high)

D) ❌ Manual management = complexity, possible human error
      EC2 MySQL = you manage OS, patches, HA
      Lambda failover = additional latency and possible failure

KEYWORD IDENTIFIED: "automatic failover" + "no data loss"
→ Multi-AZ RDS (synchronous = RPO 0, automatic = RTO < 30s)
```

---

## Case 2 — Trick Question: Multi-AZ vs Read Replica

**Context:** An exam question mixes both concepts to confuse candidates.

**Simulated Question:**
> An e-commerce application has slowness in report queries that impact customer transactions. The DBA identifies that heavy analytical queries run on the same database that processes orders. What is the simplest solution?
> A) Enable RDS Multi-AZ on the existing database
> B) Create a Read Replica and direct analytical queries to it
> C) Migrate to Aurora Serverless
> D) Add ElastiCache in front of RDS

**Analysis:**
```
A) ❌ Multi-AZ = HA/failover, does not improve performance
      The Multi-AZ replica is STANDBY (does not accept reads)
      Enabling Multi-AZ does not solve the load problem

B) ✅ CORRECT:
   Read Replica = asynchronous copy for reading
   Direct analytical queries to Read Replica endpoint
   Primary database stays dedicated only to transactions (writes)
   
C) ⚠️ Works but is a bigger change (data migration, cost)
      "Simplest" points to Read Replica
      
D) ⚠️ ElastiCache helps for repeated/identical queries
      Analytical queries are generally unique (ad hoc)
      Does not solve complex queries that always change

LESSON: "performance problem" + "heavy read queries" → Read Replica
       "failover/availability" → Multi-AZ
```

---

## Case 3 — Analyzing a Cost-Efficiency Question

**Context:** Question asks for S3 storage choice based on a specific access pattern.

**Simulated Question:**
> A company stores application logs in S3. Logs from the current month are accessed daily for debugging. Logs older than 30 days are rarely accessed but need to be available within minutes when needed. Logs older than 1 year can have retrieval of hours. Which S3 class combination is most economical?
> A) All in S3 Standard
> B) S3 Standard for 30 days, then Glacier Deep Archive
> C) S3 Standard for 30 days, Standard-IA for 30-365 days, then Glacier Flexible Retrieval
> D) S3 Intelligent-Tiering for all objects

**Analysis:**
```
Requirements mapping:
- 0-30 days: frequent access, daily debugging → S3 Standard
- 30-365 days: rarely accessed, available "in minutes" → Standard-IA
  (NOT Glacier — Glacier takes hours for Flexible or 12h for Deep Archive)
- > 1 year: retrieval can take hours → Glacier Flexible (1-5h) ✓

A) ❌ Very high cost, everything in Standard even old files
B) ❌ After 30 days goes to Deep Archive (12h retrieval)
      But the 30-365 day requirement asks for "available in minutes"!
C) ✅ CORRECT — perfect mapping by period
D) ⚠️ Works automatically but:
      Monitoring fee per object ($0.0025/1000 objects)
      For many small objects: may be more expensive than C
      "Most economical" → C is more optimized when pattern is known

LESSON: Glacier = hours (not minutes). Standard-IA = milliseconds (lower cost)
```

---

## Case 4 — Security Question: Which Service for Which Threat

**Context:** Security questions often confuse GuardDuty, WAF, Shield, Macie, and Inspector.

**Simulated Question:**
> A company detected that its S3 bucket with customer data contains exposed PII and credit card numbers without encryption. Which AWS service identifies and alerts on this sensitive data?
> A) AWS GuardDuty
> B) Amazon Macie
> C) AWS WAF
> D) AWS Config

**Analysis:**
```
A) ❌ GuardDuty = detects THREATS (anomalous behavior, mining, exfiltration)
      Analyzes: VPC Flow Logs, CloudTrail, DNS
      Does NOT analyze DATA CONTENT in S3
      
B) ✅ CORRECT — Amazon Macie:
   Uses ML to discover sensitive data in S3
   Identifies: PII (name, email), PCI (credit cards), credentials
   Generates findings: "S3BucketEncryptionDisabled" + "SensitiveData:S3Object/PII"
   
C) ❌ WAF = HTTP web request filter (SQLi, XSS)
      Does NOT analyze stored object content
      
D) ❌ AWS Config = RESOURCE configuration compliance
      Checks if bucket has encryption enabled (configuration)
      Does NOT check object CONTENT

SECURITY SERVICE MAPPING:
├── Sensitive data in S3 → Macie
├── Threats and anomalous behavior → GuardDuty
├── HTTP web attacks → WAF
├── DDoS → Shield
├── Resource misconfiguration → Config
├── Vulnerabilities in EC2/containers → Inspector
└── Findings centralization → Security Hub
```

---

## Case 5 — Simulating Exam Day Review Strategy

**Context:** Candidate has 65 questions and 130 minutes. How to manage time and marked questions.

**Execution Simulation:**
```
QUESTION 1-20 (40 min — ~2 min/question):
Q1: I know the answer → answer immediately (45s)
Q5: Doubt between A and C → mark it, choose C (what seems best), flag "review"
Q12: Very long, many details → mark it, skip to next (save time)
Q15: I know with certainty → 30s

QUESTION 21-65 (continuing...):
Q33: Word "multi-AZ" + "performance" → Red flag (Multi-AZ vs Read Replica trap)
     Read carefully → it's about reading → Read Replica → answer
Q47: Question about NAT Gateway cost → I know NAT GW is charged per hour
     Answer with confidence
Q55: 3 services I've never seen combined → mark it, choose by eliminating wrong ones

REVIEW (marked questions — 30 min):
Q5 (doubt A vs C): Reread the question, identify "synchronous" → Multi-AZ → changed to B
Q12 (long): Now calmly, read → Kinesis vs SQS question, identify "replay"
             → Kinesis. Answer.
Q55 (unknown services): 2 options remaining, choose the one with managed services
                         → Principle: "managed > self-managed" in AWS

LESSONS FROM THE SIMULATION:
1. Long questions: read the LAST paragraph first (usually has the key constraint)
2. Questions with lists: eliminate clearly wrong ones
3. "Minimum cost" → Spot/Reserved/Serverless/S3-IA/Glacier
4. "Minimum operational" → Managed services (RDS > EC2+MySQL)
5. "Maximum availability" → Multi-AZ + Multi-Region + Auto Scaling
6. Never spend > 3 minutes on a question — mark it and move on
```
