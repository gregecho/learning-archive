# Cheatsheet - Disaster Recovery and Continuity

## Quick decision map

| Requirement | Best pattern | Exam note |
|---|---|---|
| Lowest cost, accepts hours of downtime | Backup and Restore | Focus on snapshots, backups, and automated restore |
| RTO of minutes with controlled cost | Pilot Light | Database and data replicated, compute spins up on disaster |
| Low downtime with simple operation | Warm Standby | Reduced environment always active in second region |
| Near-zero downtime and data loss | Active/Active | Uses global routing and near real-time replicated data |

## Key services

- Route 53: failover, health checks, latency routing
- AWS Backup: centralized backup, vault lock, cross-account
- Elastic Disaster Recovery: continuous server replication
- S3: versioning, CRR, lifecycle, object lock
- RDS/Aurora: automatic backups, snapshots, global database
- DynamoDB: PITR, global tables

## Common pitfalls

- confusing high availability (multi-AZ) with regional DR
- ignoring cross-region replication cost
- choosing complex architecture without business need
- forgetting to test failover/failback runbooks

## Exam trigger phrases

- "regional disaster" => multi-region
- "least operational overhead" => managed service
- "recover quickly" => warm standby or active/active
- "cost-effective" => backup and restore or pilot light

---
