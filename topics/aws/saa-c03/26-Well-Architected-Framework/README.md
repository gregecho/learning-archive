# Module 26 — AWS Well-Architected Framework

## The 6 Pillars

```
1. Operational Excellence    → Operate and improve systems continuously
2. Security                  → Protect data, systems and assets
3. Reliability               → Recover from failures, meet demand
4. Performance Efficiency    → Use computing resources efficiently
5. Cost Optimization         → Avoid unnecessary costs
6. Sustainability            → Minimize environmental impact
```

---

## 1. Operational Excellence

**Objective**: Execute and monitor systems to deliver value and continuously improve.

### Design Principles
- **Perform operations as code** (IaC: CloudFormation, CDK, Terraform)
- **Make frequent, small, reversible changes** (granular deploy, feature flags)
- **Refine operations procedures frequently** (runbooks, updated playbooks)
- **Anticipate failure** (game days, chaos engineering)
- **Learn from all operational failures** (blameless post-mortems)

### Key Services
- AWS CloudFormation, AWS CDK (IaC)
- AWS Config (configuration compliance)
- AWS CloudTrail (auditing)
- Amazon CloudWatch (monitoring)
- AWS Systems Manager (centralized operations)
- AWS X-Ray (observability)

---

## 2. Security

**Objective**: Protect information, systems and assets while delivering value.

### Design Principles
- **Implement a strong identity foundation** (MFA, least privilege, IAM roles)
- **Enable traceability** (CloudTrail, Config, access logging)
- **Apply security at all layers** (VPC, SG, NACL, WAF, CDN)
- **Automate security best practices** (Security Hub, GuardDuty, Macie)
- **Protect data in transit and at rest** (TLS, KMS)
- **Keep people away from data** (programmatic access, no human touch)
- **Prepare for security events** (incident response runbooks, Security Hub)

### Key Services
- **Identity**: IAM, AWS SSO/IAM Identity Center, Organizations, SCPs
- **Detection**: GuardDuty, Macie, SecurityHub, Inspector, Config
- **Infrastructure Security**: VPC, SG, WAF, Shield, Network Firewall, Firewall Manager
- **Data Protection**: KMS, CloudHSM, ACM, Secrets Manager
- **Incident Response**: CloudTrail, AWS IR Playbooks

---

## 3. Reliability

**Objective**: Recover from infrastructure or service interruptions and scale to meet demand.

### Design Principles
- **Automatically recover from failures** (Auto Scaling, Health Checks, CloudWatch Alarms)
- **Test recovery procedures** (Game Days, DR exercises)
- **Scale horizontally** to increase availability (many small instances)
- **Stop guessing capacity** (Auto Scaling + CloudWatch)
- **Manage change through automation** (CloudFormation, CodePipeline)

### Availability Goals vs Architecture

| Availability | Downtime/year | Minimum Architecture |
|---|---|---|
| 99% | ~3.65 days | Single AZ backup + restore |
| 99.9% | ~8.7 hours | Multi-AZ, warm standby |
| 99.99% | ~52 minutes | Multi-AZ + Multi-Region active-active or active-passive |
| 99.999% | ~5 minutes | Multi-Region active-active |

### RTO and RPO
- **RPO** (Recovery Point Objective): how much data can I lose? → backup frequency
- **RTO** (Recovery Time Objective): how long can I be offline? → DR strategy

### DR Strategies

```
Cost        Strategy              RTO/RPO
Lowest ───── Backup & Restore ─────── Hours/Hours
       │     Pilot Light ────────── 10-15 min / Min
       │     Warm Standby ─────────  Min / Seconds
Highest ──── Multi-site Active-Active  Seconds / Zero
```

---

## 4. Performance Efficiency

**Objective**: Use computing resources efficiently to meet system requirements.

### Design Principles
- **Democratize advanced technologies** (use managed services instead of managing infra)
- **Go global in minutes** (CloudFront, Global Accelerator, multi-region)  
- **Use serverless architectures** (Lambda, Fargate, DynamoDB)
- **Experiment more often** (A/B testing, blue/green)
- **Use the right technology for each task** (don't use generic solutions)

### Resource Types
- **Compute**: EC2 (right types), Lambda (serverless), Fargate, Graviton2/3 (ARM, better cost/performance)
- **Storage**: EBS gp3 (independent IOPS), S3 (S3 Intelligent-Tiering for variable access)
- **Database**: RDS (relational), DynamoDB (NoSQL key-value), ElastiCache (cache), Aurora (managed MySQL/PostgreSQL)
- **Network**: CloudFront (CDN), Global Accelerator, VPC Endpoints, placement groups

---

## 5. Cost Optimization

**Objective**: Avoid unnecessary costs.

### Design Principles
- **Implement Cloud Financial Management** (tagging, budgets, Cost Explorer)
- **Adopt a consumption model** (pay for what you use; shut down non-prod environments)
- **Measure overall efficiency** (cost per unit of work)
- **Stop spending on undifferentiated heavy lifting** (use managed services)
- **Analyze and attribute expenditure** (cost allocation tags, AWS Cost Allocation Tags)

### EC2 Purchase Models
| Model | Discount | Commitment |
|---|---|---|
| On-Demand | 0% (base) | None |
| Reserved (1 year) | ~40% | 1 year |
| Reserved (3 years) | ~60% | 3 years |
| Savings Plans Compute | up to 66% | 1 or 3 years ($$/hour) |
| Savings Plans EC2 | up to 72% | 1 or 3 years (family/region) |
| Spot | up to 90% | Interruptible |

**Cost Tools:**
- **AWS Cost Explorer**: spend analysis and forecasting
- **AWS Budgets**: alerts when spending exceeds threshold
- **Cost Allocation Tags**: track costs by project/team/environment
- **Compute Optimizer**: recommends ideal instance type (rightsizing)
- **Trusted Advisor**: identify underutilized resources

---

## 6. Sustainability

**Objective**: Minimize the environmental impact of cloud workloads.

### Design Principles
- **Understand your impact** (Customer Carbon Footprint Tool)
- **Establish sustainability goals** (CO2 emission reduction)
- **Maximize utilization** (right-sizing, avoid idle resources)
- **Anticipate and adopt more efficient hardware** (Graviton3, latest generation instances)
- **Use managed services** (share infrastructure with other customers)
- **Reduce downstream impact** (compression, caching, fewer transfers)

---

## AWS Well-Architected Tool (WAT)

Free tool to review workloads against the 6 pillars:
1. Define the workload (technologies, environment)
2. Answer questions about each pillar
3. WAT generates risk report (High/Medium Risk Items)
4. Create Improvement Plan
5. Track risk resolution over time

**AWS Well-Architected Partner Program**: certified partners who conduct formal reviews

---

## Exam Tips

- WAF questions are frequent in SAA-C03 — memorize the 6 pillars and key principles
- **Reliability != Availability**: Reliability = ability to recover from failures; Availability = % uptime
- **Pilot Light**: minimum critical components always running on AWS (replicated database); others supported by ready AMIs
- **Warm Standby**: scaled-down version running on AWS; after DR, scales to full capacity
- Multi-site Active-Active: highest cost, but RTO/RPO near zero
- WAT does not charge for use; Well-Architected partners may charge for consulting services
- Sustainability: Graviton3, Serverless (Lambda/Fargate) and managed services are sustainable patterns
- For Cost Optimization: Compute Optimizer = rightsizing; Cost Explorer = analysis over time; Budgets = proactive alerts
- Security "shift left": apply security early in the development cycle, not just before deployment
- "Least privilege" is a security principle: each IAM entity has only the minimum necessary permissions
