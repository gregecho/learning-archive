# Use Cases — Introduction SAA-C03

## Case 1 — SaaS Platform Starting an Architectural Review

### Scenario
A B2B SaaS already runs on AWS, but the team realized they know how to operate services without being able to justify architectural decisions. Leadership wants to prepare two architects for the SAA-C03 and, at the same time, review the current platform design.

### Reasoning Architecture

```text
Business -> Requirements -> Constraints -> Service Choice -> Trade-off -> Operation
   |           |             |               |                  |          |
   +-----------+-------------+---------------+------------------+----------+
```

### Justified Technical Decisions
- Study should start with core services like IAM, VPC, EC2, S3, RDS, and Route 53, because they appear in a large portion of scenarios.
- The group needs to review not just services, but patterns: HA, DR, decoupling, and total cost.
- The best way to internalize this is to combine theory, questions, and real cases.

### Trade-offs Considered
- Studying by isolated service is fast, but generates little context.
- Studying by scenario is slower, but brings the candidate closer to the real exam format.

## Case 2 — E-commerce with Doubt Between Robustness and Simplicity

### Scenario
An online store wants to grow before Black Friday. The technical team proposes several highly sophisticated solutions, but management wants to know which approach is appropriate without inflating cost and operations. The study goal is to learn to distinguish the necessary from the excessive.

### Reasoning Architecture

```text
Users -> ALB -> ASG EC2 -> Aurora Multi-AZ
              |         |
              |         +-> CloudWatch
              |
              +-> CloudFront -> S3 static
```

### Justified Technical Decisions
- ALB and ASG address elasticity with less effort than manually managing multiple instances.
- Aurora Multi-AZ handles regional continuity without requiring multi-region from the start.
- CloudFront reduces latency and offloads static content.

### Trade-offs Considered
- Active-active multi-region would be more resilient, but may be overkill if the real requirement is only regional HA.
- Dedicated instances can offer isolation, but increase cost without explicit need.

## Case 3 — Data Startup with Tight Budget

### Scenario
A startup needs to process application events with controlled cost. The SAA-C03 exam would use this context to evaluate whether the candidate understands when to prioritize managed services and on-demand billing.

### Reasoning Architecture

```text
Application -> EventBridge -> Lambda -> DynamoDB
                          |
                          +-> CloudWatch Logs
```

### Justified Technical Decisions
- Lambda reduces idle time and patching for variable workloads.
- EventBridge facilitates event-driven integration with low coupling.
- DynamoDB fits well when access is predictable by key and scale is horizontal.

### Trade-offs Considered
- EC2 can offer more control, but requires constant administration.
- A relational database may be better in complex transactional scenarios, but here the access pattern favors NoSQL.

## Case 4 — Regulated Company Focused on Governance

### Scenario
A financial organization needs traceability, least privilege, and controlled encryption keys. It wants the exam preparation to reinforce real best practices for secure architecture.

### Reasoning Architecture

```text
Users -> IAM Identity Center -> AWS Accounts
                       |
                       +-> IAM Roles / SCPs
                       +-> KMS
                       +-> CloudTrail
```

### Justified Technical Decisions
- IAM Identity Center simplifies centralized access.
- SCPs help limit what accounts can do at the organizational level.
- KMS and CloudTrail appear as pillars of encryption and auditing.

### Trade-offs Considered
- More centralized governance reduces risk, but requires careful permission design.
- Overly broad policies speed up the short term and harm compliance.

