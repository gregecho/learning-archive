# 22 Disaster Recovery and Continuity

## Module objectives

- master RTO and RPO and map each DR strategy to the business requirement
- differentiate Backup and Restore, Pilot Light, Warm Standby, and Multi-Site Active/Active
- select AWS services for continuity: AWS Backup, Elastic Disaster Recovery, Route 53, Aurora Global Database, DynamoDB Global Tables, and S3 CRR
- answer exam questions balancing resilience, cost, and operational complexity

## Fundamental concepts

Disaster recovery in SAA-C03 is not just about backup. The exam covers architectural design that continues to operate when there is an AZ, region, managed service, or human error failure.

- RTO (Recovery Time Objective): maximum acceptable time to restore the service.
- RPO (Recovery Point Objective): maximum acceptable data loss in terms of time.

The lower the RTO and RPO, the higher the cost and complexity tend to be.

## DR Strategies

1. Backup and Restore
- lowest cost
- slowest restoration
- high RTO, moderate/high RPO
- ideal for non-critical workloads

2. Pilot Light
- minimal critical components stay active in the secondary region
- application and capacity scale only during a disaster
- medium RTO, low/medium RPO

3. Warm Standby
- reduced environment always active in another region
- fast scale-up during a disaster
- low RTO, low RPO

4. Multi-Site Active/Active
- two active regions serving traffic
- near-immediate failover
- very low RTO and RPO
- highest cost and more complex operation

## Most tested services and patterns

- Route 53 Failover + Health Checks for redirection between regions.
- AWS Elastic Disaster Recovery for continuous server replication and fast cutover.
- AWS Backup for centralized backup policy and cross-account vaults.
- S3 Versioning + CRR for objects and regional resilience.
- RDS/Aurora: snapshots, cross-region read replicas, and Aurora Global Database.
- DynamoDB: PITR and Global Tables for low latency and continuity.
- Cross-region EBS snapshots for EC2 restoration.

## Exam tips

- Multi-AZ does not solve regional disaster; for that, the answer needs multi-region.
- If the question highlights "lowest cost", Backup and Restore or Pilot Light tends to win.
- If it asks for "minimal downtime", Warm Standby or Active/Active is generally better.
- If it says "least operational effort", prefer managed services and native automation.
- If it asks to preserve DNS during failover, think Route 53 with health checks.

## Related links

- [Cheatsheet](./cheatsheet.md)
- [Use cases](./use-cases.md)
- [Questions](./questions.md)
- [Flashcards](./flashcards.md)
- [Lab](./lab.md)
- [Official links](./links.md)

---
