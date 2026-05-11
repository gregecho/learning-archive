# Questions - Disaster Recovery and Continuity

## 1)
A company requires an RTO of minutes and an RPO of seconds for a global application. Which strategy is most suitable?

A. Backup and Restore
B. Pilot Light
C. Warm Standby
D. Multi-Site Active/Active

Answer: D
Reason: lowest RTO/RPO, despite higher cost.

## 2)
The application runs in a single region with RDS Multi-AZ. What risk remains?

A. Instance failure
B. AZ failure
C. Regional disaster
D. Disk failure

Answer: C
Reason: Multi-AZ does not cover total region loss.

## 3)
Which service simplifies continuous server replication for DR with few application changes?

A. AWS Backup
B. AWS Elastic Disaster Recovery
C. AWS DataSync
D. CloudEndure Migration

Answer: B
Reason: specific service for server DR.

## 4)
For critical S3 objects, which combination increases resilience and recovery of accidentally deleted versions?

A. S3 Standard + Glacier
B. Versioning + CRR
C. Intelligent-Tiering + MFA
D. Transfer Acceleration + ACL

Answer: B
Reason: versioning protects against logical deletes and CRR protects against regional failure.

## 5)
On the exam, the phrase "least operational overhead" normally favors:

A. Self-managed solution on EC2
B. Manual restore process
C. Managed services with automation
D. Third-party tools without integration

Answer: C
Reason: AWS favors simplified operation when explicitly stated.

---
