# Use Cases - AWS Organizations, Governance and Costs

## Case 1: Rapidly growing company

Scenario:
- 40 AWS accounts in 6 months
- independent teams per product
- need for common guardrails

Architecture:
- AWS Control Tower for landing zone
- OUs by environment (Sandbox, Dev, Prod)
- SCP blocking CloudTrail deactivation and usage outside allowed regions
- Identity Center for federated access

## Case 2: FinOps with chargeback

Scenario:
- executive leadership wants cost per product and per squad

Architecture:
- Mandatory tags (Owner, CostCenter, Product, Environment)
- CUR in S3
- Athena + QuickSight for chargeback dashboards
- Budgets per account and per tag

## Case 3: Compute cost reduction

Scenario:
- high spending on EC2 and Fargate

Architecture:
- Savings Plans for stable base
- Spot for batch and stateless workers
- autoscaling with limits
- rightsizing with Compute Optimizer

## Case 4: Security governance

Scenario:
- auditing requires immutable trails

Architecture:
- central log account
- CloudTrail org trail
- log bucket with Object Lock
- SCP blocks to prevent trail modification

---
