# Reference Links — EC2 Compute

## Official AWS Documentation

### EC2 Fundamentals
- [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/) — Complete EC2 guide
- [Instance Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html) — All types and families
- [EC2 Instance Type Explorer](https://aws.amazon.com/ec2/instance-explorer/) — Interactive type comparison

### Purchasing Options
- [On-Demand Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html)
- [Reserved Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html) — Standard and Convertible
- [Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) — Complete Spot guide
- [Spot Fleet](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html) — Configure Spot Fleet
- [Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/) — Compute vs EC2 Instance Savings Plans
- [Dedicated Hosts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html) — BYO-L and compliance

### Instance Metadata and User Data
- [Instance Metadata (IMDS)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) — IMDSv1 vs IMDSv2
- [Transitioning to Using Instance Metadata Service Version 2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) — Migrate to IMDSv2
- [User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) — Initialization scripts

### AMIs
- [Amazon Machine Images](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) — Create, share, copy
- [Copying an AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html) — Cross-region copy

### EBS
- [EBS Volume Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html) — Detailed comparison gp2/gp3/io1/io2/st1/sc1
- [EBS-Optimized Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html) — Instances with dedicated I/O
- [Amazon EBS io2 Block Express](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/provisioned-iops.html) — Up to 256K IOPS
- [Migrating gp2 to gp3](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/modify-volume-type.html) — gp2 to gp3 migration without downtime

### Placement Groups
- [Placement Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) — Cluster, Spread, Partition

### EC2 Lifecycle
- [Instance Lifecycle](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html) — States and transitions
- [Hibernate Your Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html) — Hibernate requirements and limitations

---

## Calculators and Comparisons

- [AWS Pricing Calculator](https://calculator.aws/pricing/2/home) — Compare On-Demand vs RI vs Spot costs
- [EC2 Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) — Interruption rate by type
- [EC2 Instance Comparison](https://instances.vantage.sh/) — Excellent unofficial tool for comparing types

---

## Whitepapers

- [Compute Pillar — Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/) — Performance efficiency pillar
- [Amazon EC2 Spot Best Practices](https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-leveraging-ec2-spot-instances/) — Cost optimization whitepaper with Spot
- [Running Containerized Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/running-containerized-microservices/) — Includes EC2 launch types

---

## FAQs for the Exam

- [EC2 FAQ](https://aws.amazon.com/ec2/faqs/)
- [Reserved Instances FAQ](https://aws.amazon.com/ec2/pricing/reserved-instances/faq/)
- [Spot Instances FAQ](https://aws.amazon.com/ec2/spot/faqs/)

---

## Key SAA-C03 Concepts in This Module

| Concept | Exam Frequency |
|---|---|
| Spot for fault-tolerant batch | High |
| gp3 vs gp2 (gp3 more flexible and cheaper) | High |
| io2 Block Express for >64K IOPS | High |
| Cluster PG for HPC/low latency | High |
| Mandatory IMDSv2 (HttpTokens: required) | Medium |
| Dedicated Host for BYO-L (Oracle, SQL Server) | High |
| Hibernate to preserve RAM state | Medium |
| Partition PG for HDFS/Cassandra/Kafka | Medium |
| Compute Savings Plans vs EC2 Instance SP | Medium |
| st1 for sequential throughput (not boot) | High |

---
