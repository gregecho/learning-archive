# 23 AWS Organizations, Governance and Costs

## Module objectives

- design multi-account environments with centralized security and governance
- apply SCPs, tagging, and access control by Organizational Unit
- master cost services in the context of architecture: Budgets, Cost Explorer, CUR, Savings Plans, and RI
- answer SAA-C03 scenarios that ask for cost reduction with minimal operational overhead

## Fundamental concepts

In SAA-C03, governance and cost appear alongside security and operations. The central idea is to structure accounts to reduce risk, improve financial visibility, and apply guardrails without blocking teams.

## Recommended multi-account architecture

- Management account only for governance and billing
- OUs separated by environment and criticality (Sandbox, Dev, Prod, Security)
- Dedicated accounts for logs and security
- Central human access via IAM Identity Center

## Key services and practices

- AWS Organizations: account hierarchy and consolidated billing
- SCP: defines permission ceiling per OU/account
- AWS Control Tower: multi-account baseline with guardrails
- AWS Budgets: proactive alerts by spending or usage limits
- Cost Explorer: trend analysis and recommendations
- Cost and Usage Report (CUR): detailed base for chargeback/showback
- Savings Plans and Reserved Instances: commitment to reduce compute cost
- Cost Allocation Tags: track cost by team/product/environment

## Exam tips

- SCP does not grant permissions; it only restricts.
- "Least operational overhead" in multi-account points to Control Tower and Identity Center.
- For granular cost visibility at scale, CUR + Athena is a recurring alternative.
- For stable workloads, RI/Savings Plans is usually the optimization answer.
- Spot is best for interruption-tolerant workloads.

## Anti-patterns

- using a single account for everything
- using root user day-to-day
- no mandatory tagging standard
- no cost limits/alerts per environment
- no segregation of log and security accounts

## Related links

- [Cheatsheet](./cheatsheet.md)
- [Use cases](./use-cases.md)
- [Questions](./questions.md)
- [Flashcards](./flashcards.md)
- [Lab](./lab.md)
- [Official links](./links.md)

---
