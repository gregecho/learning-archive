# Cheatsheet — Module 26: Well-Architected Framework

## The 6 Pillars — Summary

| Pillar | Focus | Key Principle |
|---|---|---|
| **Operational Excellence** | Operate and improve | IaC, small and reversible changes |
| **Security** | Protect | Identity as foundation, encrypt everything |
| **Reliability** | Recover from failures | Design for failure, horizontal scaling |
| **Performance Efficiency** | Use resources well | Serverless, managed services |
| **Cost Optimization** | Avoid waste | Pay-per-use, eliminate idleness |
| **Sustainability** | Environmental impact | Graviton, serverless, high utilization |

---

## Disaster Recovery Strategies — Comparison

| Strategy | RPO | RTO | Cost | How it Works |
|---|---|---|---|---|
| **Backup & Restore** | Hours | Hours | $ | Periodic backups; restore when needed |
| **Pilot Light** | Minutes | 10-30 min | $$ | Minimum core running; scale on DR |
| **Warm Standby** | Seconds/Minutes | Minutes | $$$ | Scaled-down version always active |
| **Active-Active** | Zero | Seconds | $$$$ | Multi-region with active traffic in both |

**RPO** = Recovery Point Objective = maximum data loss  
**RTO** = Recovery Time Objective = maximum downtime

---

## Availability Table

| SLA | Downtime/Year | Downtime/Month | Typical Architecture |
|---|---|---|---|
| **99%** | ~87.6 hours | ~7.3 hours | Single AZ, no redundancy |
| **99.9%** | ~8.76 hours | ~43.8 minutes | Basic Multi-AZ |
| **99.99%** | ~52.6 minutes | ~4.4 minutes | Multi-AZ + Auto Scaling |
| **99.999%** | ~5.26 minutes | ~26 seconds | Active-Active, full redundancy |

---

## EC2 Pricing Models — Comparison

| Model | Discount vs On-Demand | Commitment | Best For |
|---|---|---|---|
| **On-Demand** | — | None | Unpredictable workloads, testing |
| **Savings Plans (Compute)** | Up to 66% | $ per hour (1 or 3 years) | Any EC2/Fargate/Lambda, flexible |
| **Savings Plans (EC2)** | Up to 72% | Family + region (1 or 3 years) | Specific family, higher discount |
| **Reserved (Standard)** | Up to 72% | Specific (type+region+OS) | Stable and predictable workload |
| **Reserved (Convertible)** | Up to 54% | Can change type/OS | Stable workload, more flexibility |
| **Spot** | Up to 90% | None (interruptible!) | Batch, fault-tolerant, dev/test |
| **Dedicated Host** | Varies | Per hour or 1/3 years | BYOL licenses, regulatory compliance |

---

## Well-Architected Pillars — AWS Tools

| Pillar | Associated AWS Tools |
|---|---|
| **Operational Excellence** | CloudFormation, CodePipeline, CloudWatch, Systems Manager |
| **Security** | IAM, KMS, CloudTrail, GuardDuty, Config, Shield, WAF, Cognito |
| **Reliability** | ELB + ASG, Route 53, RDS Multi-AZ, Aurora, S3, Backup |
| **Performance Efficiency** | CloudFront, ElastiCache, Kinesis, Lambda, DynamoDB, EMR |
| **Cost Optimization** | Cost Explorer, Budgets, Trusted Advisor, Compute Optimizer, S3 Intelligent-Tiering |
| **Sustainability** | Graviton, Serverless, Compute Optimizer |

---

## Pillars — Design Principles Summary

### Operational Excellence
- Perform operations as code (IaC)
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Learn from all operational failures

### Security
- Implement a strong identity foundation
- Enable traceability
- Apply security at all layers
- Protect data in transit and at rest
- Keep people away from data

### Reliability
- Test recovery procedures regularly
- Scale horizontally
- Stop guessing capacity
- Manage change through automation
- Design for failure

### Performance Efficiency
- Democratize advanced technologies
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy

### Cost Optimization
- Implement cloud financial management
- Adopt a consumption model
- Measure overall efficiency
- Stop spending on undifferentiated heavy lifting
- Analyze and attribute expenditure

### Sustainability
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Use managed services
- Reduce downstream impact

---

## Well-Architected Tool — Process

```
1. CREATE Workload → name, region, type
2. ANSWER questions by pillar (each pillar: ~10-20 questions)
3. VIEW results: High Risk Issues (HRI) and Medium Risk Issues (MRI)
4. CREATE Improvement Plan → prioritize and assign items
5. REVIEW periodically (every 6-12 months or after major changes)
```

---

## Exam Tips — Well-Architected

| Clue in the Question | Relevant Pillar | Typical Answer |
|---|---|---|
| "Application without downtime during deploys" | Reliability | Blue/Green Deploy, Rolling Update |
| "Reduce cost of always-on EC2" | Cost Optimization | Reserved or Savings Plans |
| "Dev environment on 8h per day" | Cost Optimization | Scheduled On/Off via Lambda+EventBridge |
| "Access to audit data" | Security | CloudTrail + S3 + Object Lock |
| "Detect and fix configuration drift" | Operational Excellence | AWS Config + SSM Remediation |
| "Instance stopped responding, recover same IP" | Reliability | EC2 Recovery Alarm (StatusCheckFailed_System) |
| "Lower carbon in architecture" | Sustainability | Graviton, Lambda, managed scheduling |
| "Review architecture against best practices" | All pillars | AWS Well-Architected Tool (WAT) |
| "RTO < 1 minute multi-region" | Reliability | Active-Active + Aurora Global Database |
| "RTO of hours acceptable for DR" | Reliability | Backup & Restore strategy |
