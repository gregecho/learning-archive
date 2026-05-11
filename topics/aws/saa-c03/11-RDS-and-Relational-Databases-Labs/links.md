# Links and Resources — RDS and Relational Databases (Module 06)

## Official AWS Documentation

- [Amazon RDS — Official Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon Aurora — Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
- [RDS Multi-AZ — Configuration](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- [RDS Read Replicas — Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
- [RDS Automated Backups and Snapshots](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
- [RDS Parameter Groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html)
- [RDS Performance Insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html)
- [Amazon ElastiCache — Documentation](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)
- [Amazon Redshift — Documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)
- [RDS Proxy — Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)

## FAQs

- [Amazon RDS FAQ](https://aws.amazon.com/rds/faqs/)
- [Amazon Aurora FAQ](https://aws.amazon.com/rds/aurora/faqs/)
- [Amazon ElastiCache FAQ](https://aws.amazon.com/elasticache/faqs/)

## Whitepapers

- [Running MySQL on AWS](https://docs.aws.amazon.com/whitepapers/latest/best-practices-for-wordpress-on-aws/best-practices-for-wordpress-on-aws.html)
- [AWS Database Migration Best Practices](https://docs.aws.amazon.com/whitepapers/latest/database-migration/database-migration.html)

## AWS Blog Articles

- [Amazon Aurora vs RDS: Which one should you use?](https://aws.amazon.com/blogs/database/is-amazon-rds-for-mysql-a-better-choice-than-amazon-aurora-mysql-compatible-edition/)
- [RDS Proxy: Connection pooling for serverless](https://aws.amazon.com/blogs/compute/using-amazon-rds-proxy-with-aws-lambda/)
- [ElastiCache caching strategies](https://aws.amazon.com/blogs/database/work-with-caching-strategies-in-elasticache/)

## Study Tools

- [Tutorials Dojo — Amazon RDS Cheat Sheet](https://tutorialsdojo.com/amazon-relational-database-service-amazon-rds/)
- [Tutorials Dojo — Amazon Aurora Cheat Sheet](https://tutorialsdojo.com/amazon-aurora/)

## Multi-AZ vs Read Replica Comparison

| Criterion | Multi-AZ | Read Replica |
|---------|----------|-------------|
| Purpose | HA/DR | Performance (reads) |
| Synchronization | Synchronous | Asynchronous |
| Active reads? | No (standby) | Yes |
| Auto failover? | Yes | No |
| Cross-region? | No (same Multi-AZ) | Yes |
| Promotable? | No | Yes (independent) |
| Failover downtime | ~1-2 min | N/A |
