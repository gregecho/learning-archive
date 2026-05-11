# Flashcards - Disaster Recovery and Continuity

1. What does RTO mean?
- Maximum time to restore the service.

2. What does RPO mean?
- Maximum data loss window.

3. Does Multi-AZ cover regional disaster?
- No.

4. Lowest cost DR strategy?
- Backup and Restore.

5. Strategy with minimal components active in a second region?
- Pilot Light.

6. Strategy with a reduced environment always active?
- Warm Standby.

7. Lowest RTO/RPO in general?
- Active/Active multi-region.

8. AWS server DR service?
- AWS Elastic Disaster Recovery.

9. Object protection against accidental deletion?
- S3 Versioning.

10. Object replication between regions?
- S3 CRR.

11. Managed DNS failover?
- Route 53 with health checks.

12. RDS Multi-AZ is for?
- Regional high availability, not multi-region DR.

13. DynamoDB for global DR?
- Global Tables.

14. What should be tested periodically in DR?
- Failover and failback runbook.

15. Exam phrase: "regional disaster"?
- Requires multi-region design.

---
