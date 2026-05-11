# Cheatsheet - AWS Organizations, Governance and Costs

## Quick map

| Need | Service/Pattern | Exam tip |
|---|---|---|
| Permission guardrail across multiple accounts | SCP | Remember: does not grant, only restricts |
| Provision standard landing zone | Control Tower | Lower overhead for multi-account |
| Centralized user access | IAM Identity Center | Avoids IAM users in each account |
| Alert on budget overrun | AWS Budgets | Alerts before the bill closes |
| Detailed spending analysis | CUR + Athena | Granular view by service/tag |
| Reduce predictable compute cost | Savings Plans / RI | Usage commitment reduces price |

## Cost optimization

- rightsizing of EC2 and RDS
- shutdown of non-production environments
- appropriate storage classes (S3 lifecycle)
- use Spot in stateless workloads
- review cross-AZ/region transfers

## Trigger phrases

- "across multiple AWS accounts" => Organizations/Control Tower
- "prevent specific actions" => SCP
- "cost visibility by team" => Cost Allocation Tags + CUR
- "predictable usage" => RI/Savings Plans
- "variable workload" => Savings Plans or on-demand + autoscaling

---
