# Use Cases - Disaster Recovery and Continuity

## Case 1: E-commerce with seasonal peak

Scenario:
- 99.95% availability
- RTO less than 15 minutes
- RPO less than 5 minutes

Recommended architecture:
- Warm Standby in a second region
- Aurora Global Database
- S3 with CRR
- Route 53 failover with health checks

Why it works:
- meets low RTO/RPO without the extreme cost of active/active

## Case 2: Internal ERP with low budget

Scenario:
- can be unavailable for up to 4 hours
- accepts loss of up to 1 hour of data

Recommended architecture:
- Backup and Restore
- AWS Backup with daily policies and retention
- cross-region EBS and RDS snapshots

Why it works:
- lowest cost for a less restrictive business requirement

## Case 3: Payment platform

Scenario:
- near-zero unavailability
- compliance and audit trail

Recommended architecture:
- Active/Active multi-region
- DynamoDB Global Tables
- API Gateway + Lambda in two regions
- Route 53 latency/failover

Why it works:
- reduces impact of regional failure and improves global latency

## Case 4: Data center migration to AWS

Scenario:
- quickly recover legacy VMs
- few application changes

Recommended architecture:
- AWS Elastic Disaster Recovery
- continuous replication on-premises -> AWS
- cutover and failback runbook

Why it works:
- accelerates DR strategy without immediate refactoring

---
